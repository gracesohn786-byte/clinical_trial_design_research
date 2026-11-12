PHASE I 3+3 SIMULATION - PYTHON OUTPUT GUIDE

All records are simulated. No PDS patient data are used.
One-scenario methods experiment, not a clinical dose recommendation.

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
phase1_3plus3_results.pkl: Python-native results bundle, replacing R's .rds file.
session_info.txt: Python/platform/package versions and random-number generator.
runtime_summary.csv: Elapsed seconds/minutes; saved separately from the pickle bundle.

INTERPRETATION
PCS = correct selections / all simulated trials. None remains in the denominator.
selected_dose = 0 means no recommendation; zero is never administered.
mcse = Monte Carlo standard error. mc_ci_* are 95% Monte Carlo confidence limits.
Dose-selection intervals are pointwise exact binomial, not simultaneous multinomial.
Intervals quantify simulation error conditional on the scenario, not uncertainty in true DLTs.
Mean-count intervals use a t approximation across simulation replications.
expected_N = mean realized total_n; max_n is a cap, not a required sample size.
stopped_before_max_n is not the same as stopping for unsafe D1.
escalation_halted_for_toxicity can be 1 even when a lower dose is recommended.
Below/above target refers to dose index relative to the closest-to-target benchmark.
This does not establish biological inefficacy/toxicity of these doses.
mean_trial_allocation_proportion averages n_at_dose/N within each trial.
pooled_patient_proportion pools patients, giving larger trials more weight.
Do not replace unvisited-dose missing DLT rates with zero.
The target changes scoring only, not conventional 3+3 decisions.
No baseline covariates, dropout, delayed toxicity, or efficacy outcomes are modeled.
At the top dose, recommendations are restricted to the studied dose grid.

R/PYTHON DIFFERENCES
Statistical rules and CSV column names match the supplied R script.
NumPy PCG64 differs from R's generator: same seed does not give identical datasets.
Record package versions for reproducibility; runtime also depends on the environment.
Runtime includes imports, checks, trials, summaries, exports and printed results.
It stops before creating/saving/printing the timing report itself.

RELOAD RESULTS (only load a pickle you created or otherwise trust)
saved = pd.read_pickle(output_dir / 'phase1_3plus3_results.pkl')
patient_data = saved['patient_data']
runtime_summary = pd.read_csv(output_dir / 'runtime_summary.csv')
For the final-dose CSV, preserve the literal 'None' label with:
pd.read_csv(path, keep_default_na=False, na_values=[''])

REPRODUCE ONE TRIAL
j = 1
replay = simulate_3plus3(j, int(trial_seeds[j-1]), p_true, target, max_n, scenario_id)
pd.DataFrame(replay['cohorts'])

REFERENCES
Lin & Shih (2001): https://doi.org/10.1093/biostatistics/2.2.203
Chen et al. (2018): https://doi.org/10.1016/j.conctc.2018.10.006
