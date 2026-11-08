# Run the published DECREASE example model (ext/decrease/DECREASE_model_example/DECREASEmodel.R, GPL-3)
# unmodified on 8x8 matrices of 192_Combinations_.xlsx, measuring single-agent curves + diagonal (22 points).
# Usage: Rscript scripts/run_decrease.R <ids.txt> <out.csv>
#   ids.txt: one PairIndex per line. Results are appended to out.csv after every matrix;
#   matrices already in out.csv are skipped, so the run can be stopped and resumed.
# Needs xgboost 1.7.x (the example uses the pre-3.0 API): R_LIBS=~/R/decrease-lib:~/R/library
args <- commandArgs(TRUE); ids <- as.integer(readLines(args[1])); out <- args[2]
root <- normalizePath(".")
ex <- file.path(root, "ext/decrease/DECREASE_model_example")
d <- openxlsx::read.xlsx(file.path(root, "ext/decrease/210_Novel_Anticancer_combinations/192_Combinations_.xlsx"))
done <- if (file.exists(out)) unique(read.csv(out)$PairIndex) else integer(0)
for (k in setdiff(ids, done)) {
  g <- d[d$PairIndex == k, ]
  c1 <- sort(unique(g$Conc1)); c2 <- sort(unique(g$Conc2))
  i1 <- match(g$Conc1, c1); i2 <- match(g$Conc2, c2)
  keep <- i1 == 1 | i2 == 1 | i1 == i2                  # single-agent row/column + diagonal
  tmp <- tempfile("dec"); dir.create(tmp)
  saveRDS(g[keep, c("PairIndex", "Drug1", "Drug2", "Conc1", "Conc2", "Response", "ConcUnit")], file.path(tmp, "annot.RDS"))
  file.copy(file.path(ex, "HelpFunctions.R"), tmp)
  t0 <- Sys.time(); env <- new.env()
  ok <- tryCatch({ owd <- setwd(tmp); sys.source(file.path(ex, "DECREASEmodel.R"), envir = env); setwd(owd); TRUE },
                 error = function(e) { setwd(root); message("pair ", k, " failed: ", conditionMessage(e)); FALSE })
  if (ok) {
    mo <- env$matr_Out                                   # arranged by Conc1, Conc2 (as in DECREASEmodel.R)
    r <- data.frame(PairIndex = k, Conc1 = mo$Conc1, Conc2 = mo$Conc2, measured = !is.na(mo$Response),
                    pred = env$finalpred_, seconds = as.numeric(difftime(Sys.time(), t0, units = "secs")))
    write.table(r, out, sep = ",", row.names = FALSE, col.names = !file.exists(out), append = file.exists(out))
    message("pair ", k, " done in ", round(r$seconds[1]), " s")
  }
  unlink(tmp, recursive = TRUE)
}
