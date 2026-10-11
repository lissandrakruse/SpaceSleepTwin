# Baseline extraction using the article's pinned dlmoR source (v0.1.1).
# Install that commit first; do not substitute current main silently.
args <- commandArgs(trailingOnly = TRUE)
root <- if (length(args) >= 1) args[[1]] else "data/dlmo_reference/data"
out <- if (length(args) >= 2) args[[2]] else "outputs/dlmo_reference"
dir.create(out, recursive = TRUE, showWarnings = FALSE)
if (!requireNamespace("dlmoR", quietly = TRUE)) stop("Install pinned dlmoR first")
desc <- packageDescription("dlmoR")
expected <- "3f9ff3277b8e9ecbd4ca68e1efeb857ab483d180"
if (is.null(desc$RemoteSha) || desc$RemoteSha != expected) {
  stop("dlmoR must be installed from the recorded article source commit")
}
writeLines(capture.output(sessionInfo()), file.path(out, "sessionInfo.txt"))
files <- sort(list.files(root, pattern = "\\.csv$", recursive = TRUE, full.names = TRUE))
if (!length(files)) stop("No profiles found")
results <- lapply(files, function(file) {
  message("Processing ", basename(file))
  warnings <- character()
  start <- Sys.time()
  result <- tryCatch(withCallingHandlers({
    df <- readr::read_csv(file, show_col_types = FALSE)
    # Treat timestamps as an analysis axis; UTC parsing does not establish
    # original collection timezone or reconstruct shifted clock times.
    df$datetime <- as.POSIXct(df$datetime, tz = "UTC")
    fit <- dlmoR::calculate_dlmo(df, threshold = 2.3, fine_flag = TRUE)
    x <- as.numeric(fit$ip$inflection_point_fine$x)
    if (length(x) != 1 || !is.finite(x)) stop("No finite fine-grid estimate")
    data.frame(cohort = basename(dirname(file)), profile = basename(file),
               status = "estimated", threshold_pg_ml = 2.3,
               fit_axis_hours = x, display_time = as.character(fit$dlmo$fine$time),
               error = "", stringsAsFactors = FALSE)
  }, warning = function(w) {
    warnings <<- c(warnings, conditionMessage(w))
    invokeRestart("muffleWarning")
  }), error = function(e) {
    data.frame(cohort = basename(dirname(file)), profile = basename(file),
               status = "failed", threshold_pg_ml = 2.3,
               fit_axis_hours = NA_real_, display_time = NA_character_,
               error = conditionMessage(e), stringsAsFactors = FALSE)
  })
  result$warnings <- paste(unique(warnings), collapse = " | ")
  result$elapsed_seconds <- as.numeric(difftime(Sys.time(), start, units = "secs"))
  result
})
results <- do.call(rbind, results)
write.csv(results, file.path(out, "baseline_estimates.csv"), row.names = FALSE)
write.csv(as.data.frame(table(results$cohort, results$status)),
          file.path(out, "status_counts.csv"), row.names = FALSE)
if (!any(results$status == "estimated")) stop("All profiles failed; inspect errors")
# Failed profiles remain in the output; do not silently drop them or equate
# successful estimates to independent ground truth or twin validation.
