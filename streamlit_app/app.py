"""Phase I Streamlit publication — entry point.

Run from the project root or this folder:
    streamlit run streamlit_app/app.py
"""

from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="Phase I dosage selection",
    page_icon=":material/science:",
    layout="wide",
    initial_sidebar_state="expanded",
)

pages = {
    "": [
        st.Page("app_pages/overview.py", title="Overview", icon=":material/home:"),
    ],
    "Phase I": [
        st.Page(
            "app_pages/settings.py",
            title="Simulation settings",
            icon=":material/tune:",
        ),
        st.Page(
            "app_pages/designs.py",
            title="3+3 & BOIN designs",
            icon=":material/account_tree:",
        ),
        st.Page(
            "app_pages/runtime.py",
            title="R vs Python timing",
            icon=":material/timer:",
        ),
        st.Page(
            "app_pages/results.py",
            title="Simulation results",
            icon=":material/analytics:",
        ),
        st.Page(
            "app_pages/about.py",
            title="Methods & caveats",
            icon=":material/info:",
        ),
    ],
}

page = st.navigation(pages, position="sidebar")
page.run()
