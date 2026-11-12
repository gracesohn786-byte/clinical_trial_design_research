"""Main Phase I results hub: preliminary + per-scenario PCS / selection / timing."""

from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from charts import pcs_fairness_chart, selection_bar_chart, toxicity_curve_chart
from data_loader import (
    DESIGN_COLORS,
    SCENARIOS,
    find_preliminary,
    find_run,
    find_selection_figure,
    load_all_runtime,
    load_all_selection,
    load_csv,
    pcs_table,
)

st.title("Simulation results")
st.caption("Phase I · 10,000-trial operating characteristics (plus preliminary 1,000-trial dry run)")

INTERPRETATIONS = {
    "I": (
        "With the target in the middle (D3), 3+3 often selects neighboring D2, "
        "while BOIN concentrates more mass on D3. At Nmax = 21, BOIN PCS remains "
        "well above 3+3 even after losing some of the Nmax = 30 advantage."
    ),
    "II": (
        "On this more toxic ladder, 3+3 shows a high rate of selecting D1 or "
        "**None**, reflecting early toxicity stops. BOIN recovers the true target "
        "D2 much more often and rarely ends with no dose."
    ),
    "III": (
        "When the target sits at the highest dose (D5), both designs struggle more: "
        "mass spreads onto D4 and D3. BOIN still improves PCS relative to 3+3 at "
        "both Nmax = 30 and the fairer Nmax = 21 comparison in R and Python."
    ),
}


def _pcs_metric_row(scenario: str, language: str) -> None:
    pcs = pcs_table()
    sub = pcs[(pcs["scenario_key"] == scenario) & (pcs["language"] == language)]
    specs = [
        ("3+3", 30, "3+3"),
        ("BOIN", 30, "BOIN · Nmax=30"),
        ("BOIN", 21, "BOIN · Nmax=21"),
    ]
    cols = st.columns(3, border=True)
    for col, (design, max_n, label) in zip(cols, specs):
        row = sub[(sub["design"] == design) & (sub["max_n"] == max_n)]
        with col:
            st.markdown(f"**{label}**")
            if row.empty:
                st.caption("Not available")
            else:
                r = row.iloc[0]
                st.metric("PCS", f"{r['PCS (%)']:.2f}%")
                st.caption(f"95% MC CI {r['95% CI']}")


def _pcs_detail_table(scenario: str) -> None:
    pcs = pcs_table()
    sub = pcs[pcs["scenario_key"] == scenario][
        ["design", "language", "max_n", "PCS (%)", "95% CI"]
    ].rename(columns={"max_n": "Nmax", "design": "Design", "language": "Language"})
    st.dataframe(sub, hide_index=True, width="stretch", alt=f"PCS table for scenario {scenario}")


def _selection_section(scenario: str) -> None:
    sel = load_all_selection(include_preliminary=False)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        language = st.segmented_control(
            "Language",
            options=["Python", "R"],
            default="Python",
            key=f"sel_lang_{scenario}",
        )
    with c2:
        design = st.segmented_control(
            "Design",
            options=["3+3", "BOIN", "Both"],
            default="Both",
            key=f"sel_design_{scenario}",
        )
    with c3:
        max_n_options = [30, 21] if design != "3+3" else [30]
        if design == "Both":
            max_n = st.segmented_control(
                "BOIN Nmax (with 3+3 at 30)",
                options=[21, 30],
                default=21,
                key=f"sel_maxn_{scenario}",
            )
        else:
            max_n = st.segmented_control(
                "Nmax",
                options=max_n_options,
                default=max_n_options[0],
                key=f"sel_maxn_{scenario}",
            )

    if not language or not design or max_n is None:
        return

    frames: list[pd.DataFrame] = []
    notes: list[str] = []

    if design in ("3+3", "Both"):
        entry = find_run(scenario, "3+3", language, 30)
        if entry:
            frames.append(sel[sel["run_rel"] == entry["run_rel"]])
        else:
            notes.append("3+3 run missing.")

    if design in ("BOIN", "Both"):
        boin_n = 30 if design == "BOIN" else int(max_n)
        if design == "BOIN":
            boin_n = int(max_n)
        entry = find_run(scenario, "BOIN", language, boin_n)
        if entry:
            frames.append(sel[sel["run_rel"] == entry["run_rel"]])
        else:
            notes.append(f"BOIN Nmax={boin_n} unavailable for {language}.")

    for note in notes:
        st.warning(note, icon=":material/warning:")

    if not frames:
        st.info("No selection data for this filter combination.")
        return

    plot_df = pd.concat(frames, ignore_index=True).copy()
    if design == "Both":
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
                    alt.Tooltip("mc_ci_low:Q", format=".4f", title="CI low"),
                    alt.Tooltip("mc_ci_high:Q", format=".4f", title="CI high"),
                ],
            )
            .properties(
                height=340,
                title=f"Scenario {scenario} selected-dose distribution ({language})",
            )
        )
        st.altair_chart(chart, width="stretch", alt="Selected-dose distribution")
    else:
        st.altair_chart(
            selection_bar_chart(
                plot_df,
                title=f"Scenario {scenario} · {design} · Nmax={int(max_n)} · {language}",
            ),
            width="stretch",
            alt="Selected-dose distribution",
        )

    # Numeric table
    table = plot_df[
        ["design", "max_n", "dose_label", "n_selected", "selection_percent", "mc_ci_low", "mc_ci_high"]
    ].copy()
    table["selection_percent"] = table["selection_percent"].round(2)
    table["mc_ci_low"] = (table["mc_ci_low"] * 100).round(2)
    table["mc_ci_high"] = (table["mc_ci_high"] * 100).round(2)
    table = table.rename(
        columns={
            "design": "Design",
            "max_n": "Nmax",
            "dose_label": "Dose",
            "n_selected": "Trials selected",
            "selection_percent": "Selection %",
            "mc_ci_low": "CI low (%)",
            "mc_ci_high": "CI high (%)",
        }
    )
    st.dataframe(table, hide_index=True, width="stretch", alt="Selection probability table")

    # Optional saved PNG
    if design != "Both":
        entry = find_run(
            scenario,
            design,
            language,
            30 if design == "3+3" else int(max_n),
        )
        if entry:
            fig = find_selection_figure(entry)
            if fig is not None:
                with st.expander("Show saved selection figure from the simulation run"):
                    st.image(str(fig), caption=fig.name, width="stretch")


def _timing_section(scenario: str) -> None:
    rt = load_all_runtime(include_preliminary=False)
    sub = rt[(rt["scenario_key"] == scenario) & (rt["max_n"] == 30) & (rt["n_trials"] == 10_000)]
    if sub.empty:
        st.info("No timing rows for this scenario.")
        return
    view = sub[["design", "language", "elapsed_seconds", "elapsed_minutes"]].copy()
    view["elapsed_seconds"] = view["elapsed_seconds"].round(1)
    view["elapsed_minutes"] = view["elapsed_minutes"].round(2)
    view = view.rename(
        columns={
            "design": "Design",
            "language": "Language",
            "elapsed_seconds": "Elapsed (sec)",
            "elapsed_minutes": "Elapsed (min)",
        }
    )
    st.dataframe(view, hide_index=True, width="stretch", alt=f"Elapsed time for scenario {scenario}")


# ---- Cross-scenario summary ----
st.subheader("Cross-scenario PCS summary")
pcs = pcs_table()
lang_fair = st.segmented_control(
    "Language for fair comparison chart",
    options=["Python", "R"],
    default="Python",
    key="results_fair_lang",
)
if not pcs.empty and lang_fair:
    st.altair_chart(
        pcs_fairness_chart(pcs, language=lang_fair),
        width="stretch",
        alt="Fair PCS comparison across scenarios",
    )

# ---- Preliminary ----
prelim_box = st.expander(
    "Preliminary simulation test results (1,000 trials)",
    expanded=False,
    on_change="rerun",
    key="prelim_expander",
)
if prelim_box.open:
    with prelim_box:
        st.markdown(
            """
Before the main 10,000-trial campaign, a **1,000-trial** dry run of the R 3+3
implementation was completed for Scenario I to check the pipeline and rough PCS.
"""
        )
        prelim = find_preliminary()
        if prelim is None:
            st.warning("Preliminary run not found in the manifest.")
        else:
            perf = load_csv(prelim["run_rel"], "performance_summary.csv")
            sel = load_csv(prelim["run_rel"], "dose_selection_distribution.csv")
            pcs_row = perf[perf["metric"] == "PCS"]
            if not pcs_row.empty:
                r = pcs_row.iloc[0]
                st.metric(
                    "Scenario I · 3+3 · R · PCS (1,000 trials)",
                    f"{100 * r['estimate']:.1f}%",
                    border=True,
                )
                st.caption(
                    f"95% CI [{100 * r['mc_ci_low']:.1f}%, {100 * r['mc_ci_high']:.1f}%] · "
                    f"n_trials = {prelim['n_trials']:,}"
                )
            if not sel.empty:
                sel = sel.copy()
                sel["dose_label"] = sel.apply(
                    lambda r: "None"
                    if int(r["dose_level"]) == 0
                    else (
                        r["dose_label"]
                        if pd.notna(r["dose_label"])
                        else f"D{int(r['dose_level'])}"
                    ),
                    axis=1,
                )
                st.altair_chart(
                    selection_bar_chart(
                        sel.assign(design="3+3"),
                        title="Preliminary selected-dose distribution",
                    ),
                    width="stretch",
                    alt="Preliminary dose selection distribution",
                )
                prelim_table = sel[["dose_label", "n_selected", "selection_percent"]].copy()
                prelim_table["selection_percent"] = prelim_table["selection_percent"].round(2)
                st.dataframe(
                    prelim_table.rename(
                        columns={
                            "dose_label": "Dose",
                            "n_selected": "Trials selected",
                            "selection_percent": "Selection %",
                        }
                    ),
                    hide_index=True,
                    width="stretch",
                    alt="Preliminary selection table",
                )

# ---- Per-scenario hub ----
st.subheader("Main results by scenario (10,000 trials)")
scenario_labels = [
    f"{SCENARIOS[k]['short']} · target {SCENARIOS[k]['target_label']}"
    for k in ["I", "II", "III"]
]
scenario_tabs = st.tabs(
    scenario_labels,
    on_change="rerun",
    key="scenario_results_tabs",
)

for tab, scenario in zip(scenario_tabs, ["I", "II", "III"]):
    if not tab.open:
        continue
    with tab:
        meta = SCENARIOS[scenario]
        st.markdown(f"### {meta['title']}")
        st.write(meta["caption"])
        st.info(INTERPRETATIONS[scenario], icon=":material/lightbulb:")

        left, right = st.columns([1, 2])
        with left:
            st.altair_chart(
                toxicity_curve_chart(scenario, height=220),
                width="stretch",
                alt=f"Toxicity curve for scenario {scenario}",
            )
        with right:
            lang_cards = st.segmented_control(
                "Language for PCS cards",
                options=["Python", "R"],
                default="Python",
                key=f"pcs_lang_{scenario}",
            )
            if lang_cards:
                _pcs_metric_row(scenario, lang_cards)

        st.markdown("#### PCS")
        _pcs_detail_table(scenario)

        st.markdown("#### Selected-dose distribution")
        _selection_section(scenario)

        st.markdown("#### Total elapsed time (Nmax = 30)")
        _timing_section(scenario)
