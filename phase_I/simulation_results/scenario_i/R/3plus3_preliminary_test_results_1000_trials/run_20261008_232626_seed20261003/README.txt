PHASE I 3+3 SIMULATION - OUTPUT GUIDE

All records are simulated. No PDS patient data are used.
This is a hypothetical one-scenario methods experiment, not a clinical dose recommendation.

FILES
patient_data.csv: One row per patient actually enrolled in each simulated trial.
cohort_log.csv: One row per cohort, with cumulative counts and the next decision.
trial_summary.csv: One row per trial; primary selections and secondary measures.
trial_dose_summary.csv: One row per trial-dose pair, INCLUDING unvisited doses.
performance_summary.csv: PCS, other probabilities, means, and Monte Carlo uncertainty.
dose_selection_distribution.csv: Final recommendation probabilities for None and each dose.
dose_allocation_summary.csv: Patient allocation and DLT summaries for each dose.
stopping_summary.csv: Distribution of stopping reasons.
configuration.csv: Prespecified settings and variant conventions.
phase1_3plus3_results.rds: All results together, retaining R types and missing values.
session_info.txt: R version/platform details.

INTERPRETATION
PCS = correct selections / all simulated trials. None is included in the denominator.
selected_dose = 0 means no recommendation; zero is never an administered dose.
mcse = Monte Carlo standard error. mc_ci_* are 95% Monte Carlo confidence limits.
Dose-selection intervals are pointwise, not simultaneous multinomial intervals.
These intervals quantify simulation error conditional on the scenario, not uncertainty in true DLT probabilities.
Mean-count intervals use a t approximation across independent simulation replications.
expected_N = mean realized total_n; max_n is a cap, not a required sample size.
stopped_before_max_n is NOT the same as stopping for unsafe D1.
escalation_halted_for_toxicity can be 1 even when a lower dose is recommended.
Below/above target means dose index below/above the closest-to-target benchmark.
It does not establish biological inefficacy/toxicity of the corresponding dose.
mean_trial_allocation_proportion averages n_at_dose/N within each trial.
pooled_patient_proportion pools patients across trials, so larger trials get more weight.
Do not replace unvisited-dose NA rates with zero.
The target changes scoring only; it does not tune conventional 3+3 dose decisions.
No baseline covariates, dropout, delayed toxicity, or efficacy outcomes are modeled.
At the top dose, the recommendation is restricted to the studied dose grid.

REPRODUCE ONE TRIAL
j <- 1L
replay <- simulate_3plus3(j, trial_seeds[j], p_true, target, max_n, scenario_id)
replay$cohorts

REFERENCES
Lin & Shih (2001): https://doi.org/10.1093/biostatistics/2.2.203
Chen et al. (2018): https://doi.org/10.1016/j.conctc.2018.10.006
