"""Altair chart helpers for Phase I Streamlit views."""

from __future__ import annotations

import altair as alt
import pandas as pd

from data_loader import DESIGN_COLORS, LANGUAGE_COLORS, SCENARIOS


def toxicity_curve_chart(scenario_key: str, height: int = 220) -> alt.Chart:
    df = pd.DataFrame(
        {
            "Dose": [f"D{i}" for i in range(1, 6)],
            "True DLT rate": list(SCENARIOS[scenario_key]["p_true"]),
            "Role": [
                "Target"
                if i == SCENARIOS[scenario_key]["target_dose"]
                else "Other"
                for i in range(1, 6)
            ],
        }
    )
    target = SCENARIOS[scenario_key]["target_dose"]
    points = (
        alt.Chart(df)
        .mark_line(point=True, color="#2F5D8C")
        .encode(
            x=alt.X("Dose:N", sort=[f"D{i}" for i in range(1, 6)], title="Dose"),
            y=alt.Y("True DLT rate:Q", title="True DLT probability", scale=alt.Scale(domain=[0, 0.8])),
            tooltip=["Dose", "True DLT rate", "Role"],
        )
    )
    rule = (
        alt.Chart(pd.DataFrame({"y": [0.25]}))
        .mark_rule(strokeDash=[4, 4], color="#888888")
        .encode(y="y:Q")
    )
    target_df = df[df["Role"] == "Target"]
    highlight = (
        alt.Chart(target_df)
        .mark_point(size=120, filled=True, color="#C45C26")
        .encode(x="Dose:N", y="True DLT rate:Q", tooltip=["Dose", "True DLT rate"])
    )
    return (points + rule + highlight).properties(
        height=height,
        title=f"{SCENARIOS[scenario_key]['short']} (target {SCENARIOS[scenario_key]['target_label']})",
    )


def selection_bar_chart(
    selection_df: pd.DataFrame,
    title: str = "Selected-dose distribution",
    height: int = 320,
) -> alt.Chart:
    """selection_df must include dose_label, selection_percent, and optionally design."""
    df = selection_df.copy()
    dose_order = ["None", "D1", "D2", "D3", "D4", "D5"]
    if "design" in df.columns and df["design"].nunique() > 1:
        color = alt.Color(
            "design:N",
            scale=alt.Scale(
                domain=list(DESIGN_COLORS.keys()),
                range=list(DESIGN_COLORS.values()),
            ),
            title="Design",
        )
        chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X("dose_label:N", sort=dose_order, title="Selected dose"),
                y=alt.Y("selection_percent:Q", title="Selection (%)"),
                color=color,
                xOffset="design:N",
                tooltip=[
                    "design",
                    "dose_label",
                    alt.Tooltip("selection_percent:Q", format=".2f"),
                    alt.Tooltip("n_selected:Q", format=",.0f"),
                    alt.Tooltip("mc_ci_low:Q", format=".3f", title="CI low (prob)"),
                    alt.Tooltip("mc_ci_high:Q", format=".3f", title="CI high (prob)"),
                ],
            )
            .properties(height=height, title=title)
        )
    else:
        chart = (
            alt.Chart(df)
            .mark_bar(color=DESIGN_COLORS.get(df["design"].iloc[0], "#2F5D8C") if "design" in df.columns else "#2F5D8C")
            .encode(
                x=alt.X("dose_label:N", sort=dose_order, title="Selected dose"),
                y=alt.Y("selection_percent:Q", title="Selection (%)"),
                tooltip=[
                    "dose_label",
                    alt.Tooltip("selection_percent:Q", format=".2f"),
                    alt.Tooltip("n_selected:Q", format=",.0f"),
                ],
            )
            .properties(height=height, title=title)
        )
    # Target highlight rule via text annotation if true target present
    if "is_true_target" in df.columns and df["is_true_target"].any():
        target_label = df.loc[df["is_true_target"] == 1, "dose_label"].iloc[0]
        target_line = (
            alt.Chart(pd.DataFrame({"dose_label": [target_label]}))
            .mark_rule(color="#C45C26", strokeDash=[3, 3])
            .encode(x=alt.X("dose_label:N", sort=dose_order))
        )
        return chart + target_line
    return chart


def pcs_fairness_chart(pcs_df: pd.DataFrame, language: str = "Python", height: int = 300) -> alt.Chart:
    """Compare 3+3 (Nmax=30) vs BOIN (Nmax=21) — fair sample-size comparison."""
    df = pcs_df.copy()
    df = df[df["language"] == language]
    three = df[(df["design"] == "3+3") & (df["max_n"] == 30)]
    boin = df[(df["design"] == "BOIN") & (df["max_n"] == 21)]
    plot = pd.concat([three, boin], ignore_index=True)
    if plot.empty:
        return alt.Chart(pd.DataFrame({"x": [], "y": []})).mark_bar()
    plot["Comparison arm"] = plot.apply(
        lambda r: "3+3 (Nmax=30)" if r["design"] == "3+3" else "BOIN (Nmax=21)",
        axis=1,
    )
    return (
        alt.Chart(plot)
        .mark_bar()
        .encode(
            x=alt.X("scenario_key:N", sort=["I", "II", "III"], title="Scenario"),
            y=alt.Y("PCS (%):Q", title="PCS (%)"),
            color=alt.Color(
                "Comparison arm:N",
                scale=alt.Scale(
                    domain=["3+3 (Nmax=30)", "BOIN (Nmax=21)"],
                    range=[DESIGN_COLORS["3+3"], DESIGN_COLORS["BOIN"]],
                ),
            ),
            xOffset="Comparison arm:N",
            tooltip=[
                "scenario_key",
                "Comparison arm",
                alt.Tooltip("PCS (%):Q", format=".2f"),
                "95% CI",
            ],
        )
        .properties(
            height=height,
            title=f"Fair comparison ({language}): 3+3 vs BOIN at matched sample size",
        )
    )


def runtime_bar_chart(runtime_df: pd.DataFrame, design: str, height: int = 280) -> alt.Chart:
    df = runtime_df[runtime_df["design"] == design].copy()
    if df.empty:
        return alt.Chart(pd.DataFrame({"x": [], "y": []})).mark_bar()
    long = df.melt(
        id_vars=["scenario_key"],
        value_vars=["R (sec)", "Python (sec)"],
        var_name="Language",
        value_name="Seconds",
    )
    long["Language"] = long["Language"].str.replace(" (sec)", "", regex=False)
    return (
        alt.Chart(long)
        .mark_bar()
        .encode(
            x=alt.X("scenario_key:N", sort=["I", "II", "III"], title="Scenario"),
            y=alt.Y("Seconds:Q", title="Elapsed seconds (10,000 trials)"),
            color=alt.Color(
                "Language:N",
                scale=alt.Scale(
                    domain=list(LANGUAGE_COLORS.keys()),
                    range=list(LANGUAGE_COLORS.values()),
                ),
            ),
            xOffset="Language:N",
            tooltip=["scenario_key", "Language", alt.Tooltip("Seconds:Q", format=".1f")],
        )
        .properties(height=height, title=f"{design} simulation elapsed time")
    )
