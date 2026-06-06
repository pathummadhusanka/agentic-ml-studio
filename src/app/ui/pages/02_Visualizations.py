import asyncio

import plotly.io as pio
import streamlit as st

from app.mcp.client.visualization_client import (
    create_histogram,
)

st.title("Visualizations")

if "file_path" not in st.session_state:
    st.warning(
        "Please upload and analyze a dataset first."
    )
    st.stop()

file_path = st.session_state["file_path"]
schema = st.session_state["schema"]

st.info(
    f"Dataset: {st.session_state['dataset_name']}"
)

selected_column = st.selectbox(
    "Select Column",
    list(schema.keys())
)

histogram_json = asyncio.run(
    create_histogram(
        file_path,
        selected_column
    )
)

fig = pio.from_json(histogram_json)

st.plotly_chart(
    fig,
    use_container_width=True
)