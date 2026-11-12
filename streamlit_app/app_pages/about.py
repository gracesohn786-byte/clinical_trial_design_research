"""Methods, reproducibility, and data caveats."""

from __future__ import annotations

import streamlit as st

from data_loader import (
    CAVEATS,
    COHORT_SIZE,
    MASTER_SEED,
    N_TRIALS_MAIN,
    RUN_MANIFEST,
    TARGET_TOXICITY,
)

st.title("Methods & caveats")
st.caption("Phase I · Reproducibility notes for this publication app")

st.subheader("What this app shows")
st.markdown(
    """
This is a **publication-style** presentation of precomputed Phase I Monte Carlo
results. It does **not** re-run the 10,000-trial simulations live. Summary CSVs
under `phase_I/simulation_results/` are the source of truth for PCS, selected-dose
distributions, and runtime.
"""
)

st.subheader("Shared simulation settings")
with st.container(horizontal=True):
    st.metric("Target ϕ", f"{TARGET_TOXICITY:.2f}", border=True)
    st.metric("Cohort size", str(COHORT_SIZE), border=True)
    st.metric("Main replications", f"{N_TRIALS_MAIN:,}", border=True)
    st.metric("Master seed", str(MASTER_SEED), border=True)

st.subheader("Code locations")
st.markdown(
    """
| Language | 3+3 | BOIN |
|----------|-----|------|
| R | `phase_I/R/3+3_simulated_trials/` | `phase_I/R/boin_simulated_trials/` |
| Python | `phase_I/python/3plus3_simulation/` | `phase_I/python/boin_simulation/` |

Summary outputs used by this app live under `phase_I/simulation_results/`.
"""
)

st.subheader("Monte Carlo uncertainty")
st.markdown(
    """
Performance and selection summaries include Monte Carlo standard errors and
pointwise confidence intervals (exact binomial for probability metrics; mean-based
intervals for continuous operating characteristics). Hover tooltips on the charts
expose these quantities where available.
"""
)

st.subheader("Canonical runs included")
manifest_view = [
    {
        "Scenario": e["scenario"],
        "Design": e["design"],
        "Language": e["language"],
        "Nmax": e["max_n"],
        "Trials": e["n_trials"],
        "Preliminary": bool(e.get("preliminary", False)),
    }
    for e in RUN_MANIFEST
]
st.dataframe(manifest_view, hide_index=True, width="stretch", alt="Canonical run manifest")

st.subheader("Known data caveats")
for title, body in CAVEATS:
    st.warning(body, icon=":material/warning:", title=title)

st.markdown(
    """
Additional scope notes:

- Research-plan metrics such as overdose proportion / patients treated at the MTD
  exist in some summary files but are **not** emphasized in the Phase I report
  narrative, so they are omitted from this v1 app.
- Patient-level and cohort-level CSVs are intentionally not loaded (large files).
- Phase II and Phase III content remains outside this app for now.
"""
)

st.subheader("How to run the app")
st.code(
    "streamlit run streamlit_app/app.py",
    language="bash",
)
