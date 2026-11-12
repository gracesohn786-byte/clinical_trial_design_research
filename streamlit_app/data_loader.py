"""Canonical Phase I run manifest and cached loaders for the Streamlit app.

Scenario folders and p_true define scenario identity. Includes R and Python
runs for 3+3 and BOIN across Scenarios I–III, including BOIN at Nmax=21.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

# Project root = parent of streamlit_app/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_ROOT = PROJECT_ROOT / "phase_I" / "simulation_results"
TIMING_DIR = RESULTS_ROOT / "simulation_time_comparison"

SCENARIOS: dict[str, dict[str, Any]] = {
    "I": {
        "folder": "scenario_i",
        "title": "Scenario I — Target in the middle",
        "short": "Scenario I",
        "p_true": (0.05, 0.10, 0.25, 0.40, 0.55),
        "target_dose": 3,
        "target_label": "D3",
        "scenario_id": "S1_middle_target",
        "caption": (
            "True DLT rates rise through the middle of the ladder; "
            "the target toxicity 0.25 sits at D3."
        ),
    },
    "II": {
        "folder": "scenario_ii",
        "title": "Scenario II — Target in the lower range",
        "short": "Scenario II",
        "p_true": (0.10, 0.25, 0.40, 0.55, 0.70),
        "target_dose": 2,
        "target_label": "D2",
        "scenario_id": "S2_lower_target",
        "caption": (
            "A more toxic ladder: the target 0.25 is at D2, and higher doses "
            "escalate toxicity quickly."
        ),
    },
    "III": {
        "folder": "scenario_iii",
        "title": "Scenario III — Target in the upper range",
        "short": "Scenario III",
        "p_true": (0.02, 0.05, 0.10, 0.18, 0.25),
        "target_dose": 5,
        "target_label": "D5",
        "scenario_id": "S3_higher_target",
        "caption": (
            "A flatter, safer ladder until the top: the target 0.25 is at D5, "
            "so correct selection requires reaching the highest dose."
        ),
    },
}

# Shared design constants (from report)
TARGET_TOXICITY = 0.25
COHORT_SIZE = 3
N_TRIALS_MAIN = 10_000
MASTER_SEED = 20261003
BOIN_PHI1 = 0.15
BOIN_PHI2 = 0.35
BOIN_LAMBDA_E = 0.1968
BOIN_LAMBDA_D = 0.2984

# Relative paths under RESULTS_ROOT → run directory (not the parent results folder)
RUN_MANIFEST: list[dict[str, Any]] = [
    # Scenario I — 3+3
    {
        "scenario": "I",
        "design": "3+3",
        "language": "R",
        "max_n": 30,
        "n_trials": 10_000,
        "run_rel": "scenario_i/R/3plus3_results_10000_trials/run_20261010_111207_seed20261003",
        "figures_rel": "scenario_i/R/3plus3_results_10000_trials/figures",
    },
    {
        "scenario": "I",
        "design": "3+3",
        "language": "Python",
        "max_n": 30,
        "n_trials": 10_000,
        "run_rel": "scenario_i/python/3plus3_results_10000_trials/run_20261010_120346_seed20261003",
        "figures_rel": "scenario_i/python/3plus3_results_10000_trials/figures",
    },
    # Scenario I — BOIN max 30
    {
        "scenario": "I",
        "design": "BOIN",
        "language": "R",
        "max_n": 30,
        "n_trials": 10_000,
        "run_rel": "scenario_i/R/boin_results_10000_trials/run_20261012_141649_seed20261003",
        "figures_rel": "scenario_i/R/boin_results_10000_trials/figures",
    },
    {
        "scenario": "I",
        "design": "BOIN",
        "language": "Python",
        "max_n": 30,
        "n_trials": 10_000,
        "run_rel": "scenario_i/python/boin_results_10000_trials/run_20261012_225715_seed20261003",
        "figures_rel": "scenario_i/python/boin_results_10000_trials/figures",
    },
    # Scenario I — BOIN max 21
    {
        "scenario": "I",
        "design": "BOIN",
        "language": "R",
        "max_n": 21,
        "n_trials": 10_000,
        "run_rel": "scenario_i/R/boin_results_10000_trials_max=21/run_20261021_215505_seed20261003",
        "figures_rel": "scenario_i/R/boin_results_10000_trials_max=21/figures",
    },
    {
        "scenario": "I",
        "design": "BOIN",
        "language": "Python",
        "max_n": 21,
        "n_trials": 10_000,
        "run_rel": "scenario_i/python/boin_results_10000_trials_max=21/run_20261017_225743_seed20261003",
        "figures_rel": "scenario_i/python/boin_results_10000_trials_max=21/figures",
    },
    # Scenario I — preliminary 1k (R 3+3 only)
    {
        "scenario": "I",
        "design": "3+3",
        "language": "R",
        "max_n": 30,
        "n_trials": 1_000,
        "run_rel": "scenario_i/R/3plus3_preliminary_test_results_1000_trials/run_20261008_232626_seed20261003",
        "figures_rel": "scenario_i/R/3plus3_preliminary_test_results_1000_trials/figures",
        "preliminary": True,
    },
    # Scenario II — 3+3
    {
        "scenario": "II",
        "design": "3+3",
        "language": "R",
        "max_n": 30,
        "n_trials": 10_000,
        "run_rel": "scenario_ii/R/3plus3_results_10000_trials/run_20261010_122944_seed20261003",
        "figures_rel": "scenario_ii/R/3plus3_results_10000_trials/figures",
    },
    {
        "scenario": "II",
        "design": "3+3",
        "language": "Python",
        "max_n": 30,
        "n_trials": 10_000,
        "run_rel": "scenario_ii/python/3plus3_results_10000_trials/run_20261013_214112_seed20261003",
        "figures_rel": "scenario_ii/python/3plus3_results_10000_trials/figures",
    },
    # Scenario II — BOIN max 30
    {
        "scenario": "II",
        "design": "BOIN",
        "language": "R",
        "max_n": 30,
        "n_trials": 10_000,
        "run_rel": "scenario_ii/R/boin_results_10000_trials/run_20261013_204943_seed20261003",
        "figures_rel": "scenario_ii/R/boin_results_10000_trials/figures",
    },
    {
        "scenario": "II",
        "design": "BOIN",
        "language": "Python",
        "max_n": 30,
        "n_trials": 10_000,
        "run_rel": "scenario_ii/python/boin_results_10000_trials/run_20261013_210442_seed20261003",
        "figures_rel": "scenario_ii/python/boin_results_10000_trials/figures",
    },
    # Scenario II — BOIN max 21
    {
        "scenario": "II",
        "design": "BOIN",
        "language": "R",
        "max_n": 21,
        "n_trials": 10_000,
        "run_rel": "scenario_ii/R/boin_results_10000_trials_max=21/run_20261017_233902_seed20261003",
        "figures_rel": "scenario_ii/R/boin_results_10000_trials_max=21/figures",
    },
    {
        "scenario": "II",
        "design": "BOIN",
        "language": "Python",
        "max_n": 21,
        "n_trials": 10_000,
        "run_rel": "scenario_ii/python/boin_results_10000_trials_max=21/run_20261017_232246_seed20261003",
        "figures_rel": "scenario_ii/python/boin_results_10000_trials_max=21/figures",
    },
    # Scenario III — 3+3
    {
        "scenario": "III",
        "design": "3+3",
        "language": "R",
        "max_n": 30,
        "n_trials": 10_000,
        "run_rel": "scenario_iii/R/3plus3_results_10000_trials/run_20261013_231437_seed20261003",
        "figures_rel": "scenario_iii/R/3plus3_results_10000_trials/figures",
    },
    {
        "scenario": "III",
        "design": "3+3",
        "language": "Python",
        "max_n": 30,
        "n_trials": 10_000,
        "run_rel": "scenario_iii/python/3plus3_results_10000_trials/run_20261013_231737_seed20261003",
        "figures_rel": "scenario_iii/python/3plus3_results_10000_trials/figures",
    },
    # Scenario III — BOIN max 30
    {
        "scenario": "III",
        "design": "BOIN",
        "language": "R",
        "max_n": 30,
        "n_trials": 10_000,
        "run_rel": "scenario_iii/R/boin_results_10000_trials/run_20261013_232602_seed20261003",
        "figures_rel": "scenario_iii/R/boin_results_10000_trials/figures",
    },
    {
        "scenario": "III",
        "design": "BOIN",
        "language": "Python",
        "max_n": 30,
        "n_trials": 10_000,
        "run_rel": "scenario_iii/python/boin_results_10000_trials/run_20261013_232430_seed20261003",
        "figures_rel": "scenario_iii/python/boin_results_10000_trials/figures",
    },
    # Scenario III — BOIN max 21
    {
        "scenario": "III",
        "design": "BOIN",
        "language": "R",
        "max_n": 21,
        "n_trials": 10_000,
        "run_rel": "scenario_iii/R/boin_results_10000_trials_max=21/run_20261111_215216_seed20261003",
        "figures_rel": "scenario_iii/R/boin_results_10000_trials_max=21/figures",
    },
    {
        "scenario": "III",
        "design": "BOIN",
        "language": "Python",
        "max_n": 21,
        "n_trials": 10_000,
        "run_rel": "scenario_iii/python/boin_results_10000_trials_max=21/run_20261017_213845_seed20261003",
        "figures_rel": "scenario_iii/python/boin_results_10000_trials_max=21/figures",
    },
]

DESIGN_COLORS = {
    "3+3": "#2F5D8C",
    "BOIN": "#C45C26",
}

LANGUAGE_COLORS = {
    "R": "#276DC2",
    "Python": "#3776AB",
}


def _run_dir(entry: dict[str, Any]) -> Path:
    return RESULTS_ROOT / entry["run_rel"]


def find_run(
    scenario: str,
    design: str,
    language: str,
    max_n: int,
    n_trials: int = 10_000,
) -> dict[str, Any] | None:
    for entry in RUN_MANIFEST:
        if (
            entry["scenario"] == scenario
            and entry["design"] == design
            and entry["language"] == language
            and entry["max_n"] == max_n
            and entry["n_trials"] == n_trials
            and not entry.get("preliminary")
        ):
            return entry
    return None


def find_preliminary() -> dict[str, Any] | None:
    for entry in RUN_MANIFEST:
        if entry.get("preliminary"):
            return entry
    return None


@st.cache_data(show_spinner=False)
def load_csv(run_rel: str, filename: str) -> pd.DataFrame:
    path = RESULTS_ROOT / run_rel / filename
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_configuration(run_rel: str) -> dict[str, str]:
    df = load_csv(run_rel, "configuration.csv")
    if df.empty:
        return {}
    return {str(r["parameter"]): str(r["value"]) for _, r in df.iterrows()}


def _annotate(df: pd.DataFrame, entry: dict[str, Any]) -> pd.DataFrame:
    out = df.copy()
    out["scenario_key"] = entry["scenario"]
    out["language"] = entry["language"]
    out["max_n"] = entry["max_n"]
    out["n_trials"] = entry["n_trials"]
    out["run_rel"] = entry["run_rel"]
    meta = SCENARIOS[entry["scenario"]]
    out["scenario_title"] = meta["title"]
    out["true_target_label"] = meta["target_label"]
    return out


@st.cache_data(show_spinner=False)
def load_all_performance(include_preliminary: bool = False) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for entry in RUN_MANIFEST:
        if entry.get("preliminary") and not include_preliminary:
            continue
        df = load_csv(entry["run_rel"], "performance_summary.csv")
        if df.empty:
            continue
        frames.append(_annotate(df, entry))
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


@st.cache_data(show_spinner=False)
def load_all_selection(include_preliminary: bool = False) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for entry in RUN_MANIFEST:
        if entry.get("preliminary") and not include_preliminary:
            continue
        df = load_csv(entry["run_rel"], "dose_selection_distribution.csv")
        if df.empty:
            continue
        out = _annotate(df, entry)
        out["dose_label"] = out.apply(
            lambda r: "None"
            if int(r["dose_level"]) == 0
            else (r["dose_label"] if pd.notna(r["dose_label"]) else f"D{int(r['dose_level'])}"),
            axis=1,
        )
        frames.append(out)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


@st.cache_data(show_spinner=False)
def load_all_runtime(include_preliminary: bool = False) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for entry in RUN_MANIFEST:
        if entry.get("preliminary") and not include_preliminary:
            continue
        df = load_csv(entry["run_rel"], "runtime_summary.csv")
        if df.empty:
            continue
        frames.append(_annotate(df, entry))
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


@st.cache_data(show_spinner=False)
def load_boundary_example() -> pd.DataFrame:
    entry = find_run("I", "BOIN", "R", 30)
    if entry is None:
        return pd.DataFrame()
    return load_csv(entry["run_rel"], "boundary_summary.csv")


@st.cache_data(show_spinner=False)
def pcs_table() -> pd.DataFrame:
    """Wide PCS table for main 10k-trial runs."""
    perf = load_all_performance(include_preliminary=False)
    if perf.empty:
        return pd.DataFrame()
    pcs = perf[perf["metric"] == "PCS"].copy()
    pcs["PCS (%)"] = (pcs["estimate"] * 100).round(2)
    pcs["95% CI"] = pcs.apply(
        lambda r: f"[{r['mc_ci_low'] * 100:.2f}, {r['mc_ci_high'] * 100:.2f}]",
        axis=1,
    )
    return pcs[
        [
            "scenario_key",
            "scenario_title",
            "true_target_label",
            "design",
            "language",
            "max_n",
            "PCS (%)",
            "estimate",
            "mcse",
            "95% CI",
            "mc_ci_low",
            "mc_ci_high",
        ]
    ].sort_values(["scenario_key", "design", "max_n", "language"])


@st.cache_data(show_spinner=False)
def runtime_comparison_table() -> pd.DataFrame:
    """R vs Python elapsed seconds for Nmax=30 main runs (report Tables 3–4)."""
    rt = load_all_runtime(include_preliminary=False)
    if rt.empty:
        return pd.DataFrame()
    sub = rt[(rt["max_n"] == 30) & (rt["n_trials"] == 10_000)].copy()
    rows: list[dict[str, Any]] = []
    for (scenario, design), g in sub.groupby(["scenario_key", "design"]):
        r_row = g[g["language"] == "R"]
        p_row = g[g["language"] == "Python"]
        if r_row.empty or p_row.empty:
            continue
        r_sec = float(r_row.iloc[0]["elapsed_seconds"])
        p_sec = float(p_row.iloc[0]["elapsed_seconds"])
        reduction = (r_sec - p_sec) / r_sec * 100 if r_sec else float("nan")
        rows.append(
            {
                "scenario_key": scenario,
                "design": design,
                "R (sec)": round(r_sec, 1),
                "Python (sec)": round(p_sec, 1),
                "Time reduction (%)": round(reduction, 1),
            }
        )
    return pd.DataFrame(rows).sort_values(["design", "scenario_key"])


def scenario_toxicity_frame(scenario_key: str) -> pd.DataFrame:
    meta = SCENARIOS[scenario_key]
    rows = []
    for i, p in enumerate(meta["p_true"], start=1):
        rows.append(
            {
                "Dose": f"D{i}",
                "dose_level": i,
                "True DLT rate": p,
                "is_target": i == meta["target_dose"],
            }
        )
    return pd.DataFrame(rows)


def timing_figure_path(design: str) -> Path | None:
    name = (
        "3plus3_execution_time_bar_graph.png"
        if design == "3+3"
        else "BOIN_execution_time_bar_graph.png"
    )
    path = TIMING_DIR / name
    return path if path.exists() else None


def find_selection_figure(entry: dict[str, Any]) -> Path | None:
    fig_dir = RESULTS_ROOT / entry.get("figures_rel", "")
    if not fig_dir.exists():
        return None
    candidates = sorted(fig_dir.glob("*.png"))
    # Prefer names that look like selection distributions
    preferred = [
        p
        for p in candidates
        if "select" in p.name.lower() or "dose" in p.name.lower()
    ]
    if preferred:
        return preferred[0]
    return candidates[0] if candidates else None


CAVEATS = [
    (
        "R vs Python agreement",
        "PCS usually agrees closely across languages (often within about 1–2 "
        "percentage points). Small differences are expected from independent "
        "random-number generators under the same master seed.",
    ),
]
