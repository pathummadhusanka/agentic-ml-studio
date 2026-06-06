import asyncio

import plotly.io as pio
import streamlit as st

from app.mcp.client.visualization_client import (
    create_histogram,
    create_heatmap,
    create_scatter_plot
)

st.title("Visualizations")

required_keys = [
    "file_path",
    "dataset_name",
    "schema",
]

if not all(
    key in st.session_state
    for key in required_keys
):
    st.warning(
        "Please upload and analyze a dataset first."
    )
    st.stop()

file_path = st.session_state["file_path"]
schema = st.session_state["schema"]

st.info(
    f"Dataset: {st.
                session_state['dataset_name']}"
)

st.subheader(
    "Histogram Plot"
)

selected_column = st.selectbox(
    "Select Column",
    list(schema.keys()),
    index=None,
    placeholder="Choose a column"
)

if selected_column:

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


st.subheader(
    "Correlation Heatmap"
)

heatmap_json = asyncio.run(
    create_heatmap(file_path)
)

heatmap_fig = pio.from_json(
    heatmap_json
)

st.plotly_chart(
    heatmap_fig,
    use_container_width=True
)

numeric_columns = [
    column
    for column, dtype in schema.items()
    if dtype in (
        "int64",
        "float64",
        "int32",
        "float32",
    )
]

st.subheader(
    "Scatter Plot"
)

x_column = st.selectbox(
    "X Axis",
    numeric_columns,
    index=None,
    placeholder="Select X column",
    key="scatter_x",
)

y_column = st.selectbox(
    "Y Axis",
    numeric_columns,
    index=None,
    placeholder="Select Y column",
    key="scatter_y",
)

if x_column and y_column:

    scatter_json = asyncio.run(
        create_scatter_plot(
            file_path,
            x_column,
            y_column,
        )
    )

    scatter_fig = pio.from_json(
        scatter_json
    )

    st.plotly_chart(
        scatter_fig,
        use_container_width=True,
    )