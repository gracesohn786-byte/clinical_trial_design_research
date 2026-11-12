"""Home / project overview."""

from __future__ import annotations

import streamlit as st

from data_loader import (
    COHORT_SIZE,
    MASTER_SEED,
    N_TRIALS_MAIN,
    TARGET_TOXICITY,
    pcs_table,
)

st.title("Phase I dosage selection")
st.caption(
    "Statistical methods across the clinical drug-development lifecycle · "
    "Honors thesis presentation"
)

st.markdown(
    """
This Streamlit app publishes the **Phase I** portion of an interdisciplinary honors
thesis on statistical and data-science methods across clinical trials. The broader
project uses a panitumumab / metastatic colorectal cancer (mCRC) case study to ask
how methods for dose selection, efficacy evaluation, and subgroup generalization
can be integrated across development phases.
"""
)

st.subheader("Overall research question")
st.info(
    "How can statistical and analytical models be integrated across clinical trial "
    "phases to support dosage selection, efficacy evaluation, and generalizing "
    "outcomes across patient subgroups and populations?",
    icon=":material/help:",
)

st.subheader("Phase roadmap")
c1, c2, c3 = st.columns(3, border=True)
with c1:
    st.markdown("**Phase I — Dosage selection**")
    st.success("Complete", icon=":material/check_circle:")
    st.write(
        "Compare the classical **3+3** design with the Bayesian **BOIN** design "
        "under three dose–toxicity scenarios using 10,000 Monte Carlo trials "
        "implemented in both R and Python."
    )
with c2:
    st.markdown("**Phase II — Efficacy / go–no-go**")
    st.warning("In progress", icon=":material/pending:")
    st.write(
        "Fixed-sample objective response rate (ORR) Monte Carlo simulation and "
        "Simon’s two-stage designs (drafted in the written report; not in this app yet)."
    )
with c3:
    st.markdown("**Phase III — Real trial data**")
    st.info("Planned", icon=":material/schedule:")
    st.write(
        "Project Data Sphere trial NCT00339183 (panitumumab + FOLFIRI vs FOLFIRI "
        "in mCRC), with survival and biomarker analyses still to be written up."
    )

st.subheader("Phase I research question")
st.markdown(
    """
How well do **3+3** and **BOIN** identify an appropriate maximum tolerated dose
(MTD) near a target toxicity of 0.25 across different dose–toxicity shapes, and
how do the designs compare on probability of correct selection (PCS), selected-dose
distribution, and simulation runtime in R versus Python?
"""
)

with st.container(horizontal=True):
    st.metric("Target toxicity (ϕ)", f"{TARGET_TOXICITY:.2f}", border=True)
    st.metric("Cohort size", str(COHORT_SIZE), border=True)
    st.metric("Main trials / run", f"{N_TRIALS_MAIN:,}", border=True)
    st.metric("Master seed", str(MASTER_SEED), border=True)

st.subheader("What you will see in this app")
st.markdown(
    """
1. **Simulation settings** — design procedure, PCS definition, three toxicity scenarios, and why BOIN is also run at Nmax = 21.
2. **3+3 & BOIN designs** — escalation rules, overdose control, and final MTD selection.
3. **R vs Python timing** — validation-oriented runtime comparison for the same 10,000-trial jobs.
4. **Simulation results** — PCS and selected-dose distributions by scenario, including the fair Nmax = 21 comparison, plus the preliminary 1,000-trial dry run.
"""
)

# Quick headline KPIs from data
pcs = pcs_table()
if not pcs.empty:
    st.subheader("Headline PCS snapshot (Python, fair comparison)")
    fair = pcs[
        (pcs["language"] == "Python")
        & (
            ((pcs["design"] == "3+3") & (pcs["max_n"] == 30))
            | ((pcs["design"] == "BOIN") & (pcs["max_n"] == 21))
        )
    ]
    cols = st.columns(3, border=True)
    for i, scenario in enumerate(["I", "II", "III"]):
        sub = fair[fair["scenario_key"] == scenario]
        three = sub[sub["design"] == "3+3"]
        boin = sub[sub["design"] == "BOIN"]
        with cols[i]:
            st.markdown(f"**Scenario {scenario}**")
            if not three.empty and not boin.empty:
                t = float(three.iloc[0]["PCS (%)"])
                b = float(boin.iloc[0]["PCS (%)"])
                st.metric("3+3 PCS", f"{t:.1f}%")
                st.metric("BOIN (Nmax=21) PCS", f"{b:.1f}%", delta=f"{b - t:+.1f} pp vs 3+3")
            else:
                st.write("Results unavailable.")

st.caption(
    "Grace Sohn · Bridgewater State University · Mentors: Dr. Wanchunzi Yu & Dr. Haleh Khojasteh"
)
