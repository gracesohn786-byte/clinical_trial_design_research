"""3+3 and BOIN design explainers + comparison narrative."""

from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from charts import pcs_fairness_chart
from data_loader import (
    BOIN_LAMBDA_D,
    BOIN_LAMBDA_E,
    BOIN_PHI1,
    BOIN_PHI2,
    DESIGN_COLORS,
    TARGET_TOXICITY,
    find_run,
    load_all_selection,
    load_boundary_example,
    pcs_table,
)

st.title("3+3 & BOIN designs")
st.caption("Phase I · Design rules and comparison narrative")

tab_33, tab_boin, tab_compare = st.tabs(
    ["3+3 design", "BOIN design", "Design comparison"],
    on_change="rerun",
    key="design_tabs",
)

if tab_33.open:
    with tab_33:
        st.subheader("Basic workflow")
        st.markdown(
            """
The 3+3 design is a rule-based algorithm that escalates or expands cohorts of
three patients based on observed dose-limiting toxicities (DLTs). Decisions do
**not** use the target toxicity probability ϕ; ϕ is used only later for scoring
correct selection.
"""
        )
        st.markdown(
            """
1. Start at **D1**.
2. Enroll a cohort of 3 at the current dose and observe all DLT outcomes.
3. Escalate, expand, or stop according to the table below.
4. Recommend an MTD only after a dose is confirmed with ≤1 DLT in 6 patients
   (with special rules at the lowest and highest doses).
"""
        )

        st.subheader("Escalation / de-escalation rules")
        rules = [
            {
                "Patients at dose": "3",
                "DLTs": "0",
                "Next step": "Escalate to the next higher dose (or confirm at D5)",
            },
            {
                "Patients at dose": "3",
                "DLTs": "1",
                "Next step": "Expand with 3 more patients at the same dose",
            },
            {
                "Patients at dose": "6",
                "DLTs": "0–1",
                "Next step": "Escalate, or confirm the dose as MTD if already at the top / stopping condition",
            },
            {
                "Patients at dose": "3 or 6",
                "DLTs": "≥2",
                "Next step": "Stop escalation; evaluate the next lower dose",
            },
        ]
        st.dataframe(rules, hide_index=True, width="stretch", alt="3+3 escalation rules")

        st.subheader("Final MTD selection")
        st.markdown(
            """
- A dose is recommendable only after **≤1 DLT in 6** patients.
- If D1 fails this standard, the trial recommends **None**.
- If a lower candidate has only 3 patients when escalation stops, a confirmation
  cohort may be enrolled.
- When sample-size limits interrupt an unresolved decision, the trial also
  recommends **None** (tracked separately in stopping summaries).
"""
        )

if tab_boin.open:
    with tab_boin:
        st.subheader("Design setting")
        st.markdown(
            f"""
BOIN (Bayesian Optimal Interval) uses the target toxicity **ϕ = {TARGET_TOXICITY:.2f}**
to define escalation and de-escalation boundaries. Local defaults used here:

- φ₁ = 0.6 × ϕ = **{BOIN_PHI1:.2f}**
- φ₂ = 1.4 × ϕ = **{BOIN_PHI2:.2f}**
- Escalation boundary λₑ ≈ **{BOIN_LAMBDA_E:.4f}**
- De-escalation boundary λ_d ≈ **{BOIN_LAMBDA_D:.4f}**
"""
        )

        boundary = load_boundary_example()
        if not boundary.empty:
            st.dataframe(
                boundary[[c for c in boundary.columns if c != "scenario"]],
                hide_index=True,
                width="stretch",
                alt="BOIN boundary summary",
            )

        st.subheader("Escalation / stay / de-escalation")
        st.markdown(
            f"""
After each cohort at dose *d*, compute the observed DLT rate \\(\\hat{{p}}_d\\):

- Escalate if \\(\\hat{{p}}_d \\le \\lambda_e\\) (≈ {BOIN_LAMBDA_E:.3f})
- De-escalate if \\(\\hat{{p}}_d \\ge \\lambda_d\\) (≈ {BOIN_LAMBDA_D:.3f})
- Otherwise **stay** at the current dose
"""
        )

        st.subheader("Bayesian overdose control & dose elimination")
        st.markdown(
            r"""
Each dose has an independent **Beta(1,1)** prior. Dose *j* (and all higher doses)
is eliminated if

$$P(p_j > \phi \mid \text{data}) > 0.95 \quad\text{and}\quad n_j \ge 3.$$

If **D1** is eliminated, the trial stops with **no MTD**. Otherwise enrollment
continues until the maximum sample size is reached.
"""
        )

        st.subheader("Final MTD selection")
        st.markdown(
            """
Among treated, non-eliminated doses, BOIN applies **weighted isotonic regression**
to the empirical DLT rates and selects the dose whose adjusted rate is closest to
the target ϕ (documented tie-breaking rules apply).
"""
        )

if tab_compare.open:
    with tab_compare:
        st.subheader("PCS intuition")
        st.markdown(
            """
Across all three scenarios, BOIN achieves a higher probability of correct
selection than 3+3. Part of the Nmax = 30 advantage comes from larger enrollment;
the fairer **Nmax = 21** BOIN runs still beat 3+3, which is the comparison
emphasized in the written report.
"""
        )

        pcs = pcs_table()
        lang = st.segmented_control(
            "Language for fair PCS chart",
            options=["Python", "R"],
            default="Python",
            key="compare_lang",
        )
        if not pcs.empty and lang:
            st.altair_chart(
                pcs_fairness_chart(pcs, language=lang),
                width="stretch",
                alt=f"Fair PCS comparison in {lang}",
            )
            st.caption(
                "3+3 uses Nmax = 30 (its usual stopping behavior rarely fills 30). "
                "BOIN is shown at Nmax = 21 for a fairer sample-size comparison."
            )

        st.subheader("Selected-dose distribution previews")
        st.markdown(
            "Preview bars use **BOIN at Nmax = 21** (fair sample size) versus **3+3**, "
            "matching the report’s comparison figures."
        )
        sel = load_all_selection(include_preliminary=False)
        preview_lang = st.segmented_control(
            "Language for selection previews",
            options=["Python", "R"],
            default="Python",
            key="preview_lang",
        )
        scenario = st.segmented_control(
            "Scenario",
            options=["I", "II", "III"],
            default="I",
            key="preview_scenario",
            format_func=lambda s: f"Scenario {s}",
        )
        if not sel.empty and preview_lang and scenario:
            frames: list[pd.DataFrame] = []
            three_entry = find_run(scenario, "3+3", preview_lang, 30)
            boin_entry = find_run(scenario, "BOIN", preview_lang, 21)
            if three_entry is not None:
                frames.append(sel[sel["run_rel"] == three_entry["run_rel"]])
            if boin_entry is not None:
                frames.append(sel[sel["run_rel"] == boin_entry["run_rel"]])

            if frames:
                plot_df = pd.concat(frames, ignore_index=True).copy()
                plot_df["design_legend"] = plot_df.apply(
                    lambda r: f"{r['design']} (Nmax={int(r['max_n'])})",
                    axis=1,
                )
                dose_order = ["None", "D1", "D2", "D3", "D4", "D5"]
                domain = list(plot_df["design_legend"].unique())
                color_range = [
                    DESIGN_COLORS["3+3"] if d.startswith("3+3") else DESIGN_COLORS["BOIN"]
                    for d in domain
                ]
                chart = (
                    alt.Chart(plot_df)
                    .mark_bar()
                    .encode(
                        x=alt.X("dose_label:N", sort=dose_order, title="Selected dose"),
                        y=alt.Y("selection_percent:Q", title="Selection (%)"),
                        color=alt.Color(
                            "design_legend:N",
                            scale=alt.Scale(domain=domain, range=color_range),
                            title="Design",
                        ),
                        xOffset="design_legend:N",
                        tooltip=[
                            "design_legend",
                            "dose_label",
                            alt.Tooltip("selection_percent:Q", format=".2f"),
                            alt.Tooltip("n_selected:Q", format=",.0f"),
                        ],
                    )
                    .properties(
                        height=320,
                        title=f"Scenario {scenario} selected-dose distribution ({preview_lang})",
                    )
                )
                st.altair_chart(
                    chart,
                    width="stretch",
                    alt="Selected-dose distribution preview",
                )
            else:
                st.info("No selection data available for this filter combination.")
