PHASE I BOIN SIMULATION - OUTPUT GUIDE

All records are simulated. No PDS patient data are used.
Scenario 3 uses true DLT probabilities 0.02, 0.05, 0.10, 0.18, 0.25.
Target DLT probability = 0.25; true target is D5.

BOIN DECISION RULE
phi1 = 0.150000; phi2 = 0.350000
lambda_e = 0.196801; lambda_d = 0.298392
Observed DLT rate <= lambda_e: escalate if possible.
Observed DLT rate >= lambda_d: de-escalate if possible.
Otherwise stay at the current dose.

BAYESIAN OVERDOSE CONTROL
Prior at each dose: Beta(1,1).
Posterior after y DLTs among n patients: Beta(y+1, n-y+1).
Eliminate dose j and all higher doses if Pr(p_j > target | data) > 0.95 and n_j >= 3.
If D1 is eliminated, stop with no dose recommendation.

FINAL MTD SELECTION
Use weighted isotonic regression on observed DLT rates among treated, non-eliminated doses.
Select the admissible dose with isotonic DLT estimate closest to target.

FILES
patient_data.csv: One row per simulated patient.
cohort_log.csv: One row per cohort, including BOIN boundaries and Beta posterior quantities.
trial_summary.csv: One row per trial.
trial_dose_summary.csv: One row per trial-dose pair, including final Beta posterior and isotonic estimates.
performance_summary.csv: PCS and secondary operating characteristics.
dose_selection_distribution.csv: Final recommendation probabilities for None and D1-D5.
dose_allocation_summary.csv: Patient allocation, DLT, and elimination summaries by dose.
posterior_summary_by_dose.csv: Across-trial summaries of final posterior quantities for treated doses.
boundary_summary.csv: BOIN phi1, phi2, lambda_e, and lambda_d.
stopping_summary.csv: Distribution of stopping reasons.
configuration.csv: Prespecified simulation settings.
phase1_boin_results.pkl: Python bundle containing all tables and trial seeds.
runtime_summary.csv: Total elapsed runtime.

INTERPRETATION
PCS = correct final MTD selections / all simulated trials.
None remains in the denominator and counts as an incorrect selection in this scenario.
Posterior overdose probabilities use the Beta(1,1)-Binomial model.
The true toxicity probabilities generate simulated DLTs but are not used by the BOIN dose-decision rule.
Monte Carlo intervals describe simulation uncertainty conditional on the scenario.

RANDOM-NUMBER NOTE
Python uses NumPy PCG64 rather than R's Mersenne-Twister implementation.
The same numeric master seed therefore does not reproduce identical R trials or exact results.
