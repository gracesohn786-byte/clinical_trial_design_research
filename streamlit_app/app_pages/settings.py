"""Phase I research question & simulation settings."""

from __future__ import annotations

import streamlit as st

from charts import toxicity_curve_chart
from data_loader import (
    COHORT_SIZE,
    MASTER_SEED,
    N_TRIALS_MAIN,
    SCENARIOS,
    TARGET_TOXICITY,
)

st.title("Simulation settings")
st.caption("Phase I · Dosage selection")

st.subheader("Research question")
st.markdown(
    """
How well do the **3+3** and **BOIN** designs identify an appropriate dose that
minimizes excess toxicity across different dose–toxicity scenarios, and how do
they compare on correct selection, selected-dose distribution, and (secondarily)
simulation runtime?
"""
)

st.subheader("Design procedure")
st.markdown(
    """
1. Define a dose–toxicity scenario and a target toxicity probability (ϕ = 0.25).
2. Simulate one sequential trial in which the next cohort’s dose depends on prior DLT outcomes.
3. Record the final selected MTD (or **None** if no dose is recommended).
4. Repeat independently for many Monte Carlo replications.
5. Aggregate operating characteristics — especially PCS and the selected-dose distribution.
"""
)

st.subheader("Design comparison measures")
c1, c2 = st.columns(2, border=True)
with c1:
    st.markdown("**Probability of correct selection (PCS)**")
    st.latex(r"\mathrm{PCS} = \frac{\#\{\text{trials selecting the true target dose}\}}{\text{total trials}}")
    st.write(
        "Selecting **None** (no MTD) counts as incorrect and remains in the denominator."
    )
with c2:
    st.markdown("**Selected-dose distribution**")
    st.latex(r"P(\text{select } D_j),\quad j \in \{0,1,\ldots,5\}")
    st.write(
        "Dose level 0 denotes **None**. Together with PCS, this shows whether "
        "errors concentrate below or above the true target."
    )

st.subheader("Dose–toxicity scenarios")
st.markdown(
    f"""
Both designs use the same five-dose ladders, cohort size **{COHORT_SIZE}**, and
target toxicity **ϕ = {TARGET_TOXICITY:.2f}**. The true target dose is the dose
whose DLT probability is closest to ϕ (ties would take the lower dose).
"""
)

cols = st.columns(3, border=True)
for col, key in zip(cols, ["I", "II", "III"]):
    meta = SCENARIOS[key]
    with col:
        st.markdown(f"**{meta['title']}**")
        st.caption(meta["caption"])
        st.write(
            "True DLT rates: "
            + ", ".join(f"D{i}={p:.2f}" for i, p in enumerate(meta["p_true"], start=1))
        )
        st.write(f"True target: **{meta['target_label']}**")
        st.altair_chart(
            toxicity_curve_chart(key, height=200),
            width="stretch",
            alt=f"True DLT rates for {meta['short']}",
        )

st.subheader("Maximum sample size and fairness")
st.warning(
    "At a shared Nmax = 30, BOIN typically enrolls the full sample while 3+3 often "
    "stops earlier (commonly around 16–21 patients). Comparing BOIN at Nmax = 30 "
    "alone therefore overstates its PCS advantage. A second BOIN series uses "
    "**Nmax = 21** for a fairer sample-size match. PCS drops relative to Nmax = 30, "
    "but BOIN still outperforms 3+3 in all three scenarios.",
    icon=":material/balance:",
    title="Why Nmax = 21 matters",
)

st.subheader("Summary of simulation settings")
settings_rows = [
    {"Setting": "Designs", "Value": "3+3 and BOIN"},
    {"Setting": "Monte Carlo trials (main)", "Value": f"{N_TRIALS_MAIN:,}"},
    {"Setting": "Target toxicity ϕ", "Value": f"{TARGET_TOXICITY:.2f}"},
    {"Setting": "Cohort size", "Value": str(COHORT_SIZE)},
    {"Setting": "Number of doses", "Value": "5 (D1–D5)"},
    {"Setting": "Maximum sample size", "Value": "30 (both designs); BOIN also at 21"},
    {"Setting": "Master seed", "Value": str(MASTER_SEED)},
    {"Setting": "Implementations", "Value": "R and Python (independent RNGs)"},
    {"Setting": "Primary outputs", "Value": "PCS and P(select Di), including None"},
]
st.dataframe(settings_rows, hide_index=True, width="stretch", alt="Simulation settings summary")
