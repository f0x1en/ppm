# Head-to-head of per-patient dosing rules on virtual tacrolimus patients (liver transplant, first 2 weeks).
# Truth model: Bai et al., Front Pharmacol 2024 (doi 10.3389/fphar.2024.1449535), Table 3, one-compartment oral, no covariates.
# Rules: fixed dose, CURATE.AI linear (proportional) variant, CURATE.AI quadratic, Bayesian MAP (posologyr).
# Usage: Rscript scripts/sim_tacrolimus.R <n_patients> <scenario> <out.csv>   scenario: base | lownoise | drift
suppressMessages(library(posologyr)); rxode2::setRxThreads(1L)
args <- commandArgs(TRUE); N <- as.integer(args[1]); SC <- args[2]; OUT <- args[3]
CL <- 37.6; V <- 1710; KA <- 0.352                        # L/h, L, 1/h (typical values)
OM <- c(CL = 0.666, V = 1.26, KA = 2.36)                 # assumption: reported IIV % read as SD of log-normal
COV_CLV <- 0.226                                         # reported covariance of IIV_CL and IIV_Vc
PROP <- 0.356; ADD <- 0.355                              # residual error, as published
PROP_TRUE <- if (SC == "lownoise") 0.15 else PROP         # lower-noise scenario changes the truth only
DRIFT <- if (SC == "drift") 0.5 else 0                    # log-clearance changes linearly by +-DRIFT over the stay
TAU <- 12; DAYS <- 14; LO <- 8; HI <- 10; TARGET <- 9; START <- 4; GRID <- seq(0.5, 10, 0.5)

prior <- function() {
  ini({
    THETA_Cl <- 37.6; THETA_Vc <- 1710; THETA_Ka <- 0.352
    ETA_Cl + ETA_Vc ~ c(0.443556, 0.226, 1.5876)
    ETA_Ka ~ 5.5696
    add.sd <- 0.355; prop.sd <- 0.356
  })
  model({
    Cl <- THETA_Cl * exp(ETA_Cl); Vc <- THETA_Vc * exp(ETA_Vc); Ka <- THETA_Ka * exp(ETA_Ka)
    K20 <- Cl / Vc; Cc <- centr / Vc
    d/dt(depot) = -Ka * depot
    d/dt(centr) = Ka * depot - K20 * centr
    Cc ~ add(add.sd) + prop(prop.sd)
  })
}
PM <- posologyr:::get_prior_model(prior)   # compile once (internal posologyr helper; same MAP estimates as passing the function)
# analytic trough just before each morning dose (ug/L); dose in mg per administration, BID
trough <- function(doses, cl, v, ka, day) {
  k <- cl / v; ta <- (seq_len(2 * length(doses)) - 1) * TAU; amt <- rep(doses, each = 2) * 1000
  t <- day * 24; dt <- t - ta; m <- dt > 0
  sum(amt[m] * ka / (v * (ka - k)) * (exp(-k * dt[m]) - exp(-ka * dt[m])))
}
rule_fixed <- function(D, O, ...) D[length(D)]
rule_linear <- function(D, O, ...) D[length(D)] * TARGET / O[length(O)]
rule_quad <- function(D, O, ...) {
  if (length(unique(D)) < 3) return(rule_linear(D, O))   # quadratic needs 3 distinct dose-response pairs
  f <- lm(O ~ D + I(D^2)); p <- predict(f, data.frame(D = GRID)); GRID[which.min(abs(p - TARGET))]
}
rule_bayes <- function(D, O, ...) {
  n <- length(O)
  dat <- data.frame(ID = 1, TIME = c((seq_len(2 * n) - 1) * TAU, seq_len(n) * 24 - 1e-6),
                    DV = c(rep(NA, 2 * n), O), AMT = c(rep(D, each = 2) * 1000, rep(0, n)),
                    EVID = c(rep(1, 2 * n), rep(0, n)))
  dat <- dat[order(dat$TIME), ]
  est <- tryCatch(poso_estim_map(dat, PM, return_model = FALSE), error = function(e) NULL)
  if (is.null(est)) return(rule_linear(D, O))
  e <- est$eta; cl <- CL * exp(e[["ETA_Cl"]]); v <- V * exp(e[["ETA_Vc"]]); ka <- KA * exp(e[["ETA_Ka"]])
  pred <- sapply(GRID, function(g) trough(c(D, g), cl, v, ka, n + 1))
  GRID[which.min(abs(pred - TARGET))]
}
RULES <- list(fixed = rule_fixed, linear = rule_linear, quadratic = rule_quad, bayes = rule_bayes)

set.seed(2026)
eta <- MASS::mvrnorm(N, c(0, 0), matrix(c(OM[["CL"]]^2, COV_CLV, COV_CLV, OM[["V"]]^2), 2))
pat <- data.frame(id = seq_len(N), cl = CL * exp(eta[, 1]), v = V * exp(eta[, 2]), ka = KA * exp(rnorm(N, 0, OM[["KA"]])))
noise <- matrix(rnorm(N * DAYS * 2), N)                   # same noise draws for every rule
res <- list()
for (i in seq_len(N)) {
  cls <- pat$cl[i] * exp(DRIFT * seq(-1, 1, length.out = DAYS))
  for (r in names(RULES)) {
    D <- c(); O <- c()
    for (d in seq_len(DAYS)) {
      dose <- if (d <= 3) START else RULES[[r]](D, O)
      dose <- min(max(round(dose * 2) / 2, 0.5), 10); D <- c(D, dose)
      tr <- trough(D, cls[d], pat$v[i], pat$ka[i], d)
      O <- c(O, max(tr * (1 + PROP_TRUE * noise[i, 2 * d - 1]) + ADD * noise[i, 2 * d], 0.1))
    }
    res[[length(res) + 1]] <- data.frame(id = i, rule = r, day = seq_len(DAYS), dose = D, trough = O, scenario = SC)
  }
  if (i %% 10 == 0) message(SC, ": ", i, " / ", N)
}
write.csv(do.call(rbind, res), OUT, row.names = FALSE)
