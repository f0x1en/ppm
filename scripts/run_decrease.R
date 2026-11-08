# Run the published DECREASE example model (ext/decrease/DECREASE_model_example/DECREASEmodel.R, GPL-3)
# unmodified on each 8x8 matrix of 192_Combinations_.xlsx, measuring single-agent curves + diagonal (22 points).
# Usage: Rscript scripts/run_decrease.R <first_index> <last_index> <out.csv>
# Needs xgboost 1.7.x (the example uses the pre-3.0 API): R_LIBS=~/R/decrease-lib:~/R/library
args <- commandArgs(TRUE); from <- as.integer(args[1]); to <- as.integer(args[2]); out <- args[3]
root <- normalizePath(".")
ex <- file.path(root, "ext/decrease/DECREASE_model_example")
d <- openxlsx::read.xlsx(file.path(root, "ext/decrease/210_Novel_Anticancer_combinations/192_Combinations_.xlsx"))
ids <- sort(unique(d$PairIndex))[from:to]
res <- list()
for (k in ids) {
  g <- d[d$PairIndex == k, ]
  c1 <- sort(unique(g$Conc1)); c2 <- sort(unique(g$Conc2))
  i1 <- match(g$Conc1, c1); i2 <- match(g$Conc2, c2)
  keep <- i1 == 1 | i2 == 1 | i1 == i2                  # single-agent row/column + diagonal
  tmp <- tempfile("dec"); dir.create(tmp)
  saveRDS(g[keep, c("PairIndex", "Drug1", "Drug2", "Conc1", "Conc2", "Response", "ConcUnit")], file.path(tmp, "annot.RDS"))
  file.copy(file.path(ex, "HelpFunctions.R"), tmp)
  t0 <- Sys.time()
  env <- new.env()
  ok <- tryCatch({ owd <- setwd(tmp); sys.source(file.path(ex, "DECREASEmodel.R"), envir = env); setwd(owd); TRUE },
                 error = function(e) { setwd(root); message("pair ", k, " failed: ", conditionMessage(e)); FALSE })
  if (ok) {
    mo <- env$matr_Out                                   # arranged by Conc1, Conc2 (as in DECREASEmodel.R)
    res[[length(res) + 1]] <- data.frame(PairIndex = k, Conc1 = mo$Conc1, Conc2 = mo$Conc2,
                                         measured = !is.na(mo$Response), pred = env$finalpred_,
                                         seconds = as.numeric(difftime(Sys.time(), t0, units = "secs")))
  }
  unlink(tmp, recursive = TRUE)
}
write.csv(do.call(rbind, res), out, row.names = FALSE)
