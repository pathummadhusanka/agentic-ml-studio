import asyncio
import streamlit as st

from app.mcp.client.reporting_client import (
    generate_report,
)

st.title("Report")

required_keys = [
    "profile",
    "schema",
    "missing_values",
    "duplicates",
    "insights",
    "metrics",
    "model_path",
]

missing = [
    key
    for key in required_keys
    if key not in st.session_state
]

# st.subheader(st.session_state)

if missing:
    st.warning(
        "Please complete analysis, insights, and training first."
    )
    st.stop()
    

if st.button(
    "Generate Report"
):
    report = asyncio.run(
        generate_report(
            st.session_state["profile"],
            st.session_state["schema"],
            st.session_state["missing_values"],
            st.session_state["duplicates"],
            st.session_state["insights"],
            st.session_state["metrics"],
            st.session_state["model_path"],
        )
    )

    st.session_state["report_path"] = (
        report["report_path"]
    )

if "report_path" in st.session_state:
    st.success(
        f"Report saved: {st.session_state['report_path']}"
    )

    with open(
        st.session_state["report_path"],
        "r",
        encoding="utf-8",
    ) as file:
        st.download_button(
            label="Download Report",
            data=file.read(),
            file_name="report.md",
        )
else:
    st.info("Click 'Generate Report' to create a report first.")