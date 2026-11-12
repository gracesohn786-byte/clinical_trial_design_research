"""R vs Python simulation timing comparisons."""

from __future__ import annotations

import streamlit as st

from charts import runtime_bar_chart
from data_loader import runtime_comparison_table, timing_figure_path

st.title("Simulation time comparisons: R vs Python")
st.caption("Phase I · Same designs, same 10,000-trial jobs, independent implementations")

st.markdown(
    """
Both languages implement the same trial algorithms and shared master seed, but use
independent random-number generators. Runtime is a secondary endpoint: the primary
goal of dual implementation is **validation** (PCS and selection distributions agree),
with Python’s speed as a practical bonus for large Monte Carlo campaigns.
"""
)

rt = runtime_comparison_table()
if rt.empty:
    st.error("Runtime summaries could not be loaded.")
    st.stop()

# KPI strip — averages by design
for design, avg_label in [("3+3", "3+3 average time reduction"), ("BOIN", "BOIN average time reduction")]:
    sub = rt[rt["design"] == design]
    if sub.empty:
        continue
    avg_red = float(sub["Time reduction (%)"].mean())
    avg_r = float(sub["R (sec)"].mean())
    avg_p = float(sub["Python (sec)"].mean())
    if design == "3+3":
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(avg_label, f"{avg_red:.1f}%", border=True)
        with c2:
            st.metric("3+3 mean R time", f"{avg_r:.1f} s", border=True)
        with c3:
            st.metric("3+3 mean Python time", f"{avg_p:.1f} s", border=True)
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(avg_label, f"{avg_red:.1f}%", border=True)
        with c2:
            st.metric("BOIN mean R time", f"{avg_r:.1f} s", border=True)
        with c3:
            st.metric("BOIN mean Python time", f"{avg_p:.1f} s", border=True)

st.subheader("3+3 design simulation elapsed time")
st.markdown(
    "Across the three scenarios, Python reduced 3+3 wall-clock time by roughly "
    "**91% on average** (about a 10× speedup)."
)
three = rt[rt["design"] == "3+3"].drop(columns=["design"]).rename(
    columns={"scenario_key": "Scenario"}
)
st.dataframe(three, hide_index=True, width="stretch", alt="3+3 R vs Python timing table")
st.altair_chart(
    runtime_bar_chart(rt, "3+3"),
    width="stretch",
    alt="3+3 elapsed time bar chart",
)
fig_33 = timing_figure_path("3+3")
if fig_33 is not None:
    with st.expander("Show saved report figure (3+3)"):
        st.image(str(fig_33), caption="3+3 execution time comparison (saved PNG)", width="stretch")

st.subheader("BOIN design simulation elapsed time")
st.markdown(
    "For BOIN, Python reduced elapsed time by roughly **77% on average** "
    "(about a 4–5× speedup). Absolute times are longer than 3+3 because of "
    "posterior calculations, elimination checks, and isotonic MTD selection."
)
boin = rt[rt["design"] == "BOIN"].drop(columns=["design"]).rename(
    columns={"scenario_key": "Scenario"}
)
st.dataframe(boin, hide_index=True, width="stretch", alt="BOIN R vs Python timing table")
st.altair_chart(
    runtime_bar_chart(rt, "BOIN"),
    width="stretch",
    alt="BOIN elapsed time bar chart",
)
fig_boin = timing_figure_path("BOIN")
if fig_boin is not None:
    with st.expander("Show saved report figure (BOIN)"):
        st.image(str(fig_boin), caption="BOIN execution time comparison (saved PNG)", width="stretch")

st.info(
    "Timing comparisons use **Nmax = 30** main runs only (matching the report’s "
    "R vs Python elapsed-time tables). BOIN Nmax = 21 runs are included in the "
    "PCS / selection results pages but are not part of this runtime summary.",
    icon=":material/info:",
    title="Scope: Nmax = 30",
)
