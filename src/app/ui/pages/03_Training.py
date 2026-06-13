import streamlit as st
import asyncio

from app.mcp.client.training_client import train_linear_regression


st.title("Training")

if "profile" not in st.session_state:
	st.warning("Analyze a dataset first")

	st.stop()

schema = st.session_state["schema"]
file_path = st.session_state["file_path"]

numeric_columns = [
	column
	for column, dtypes in schema.items()
	if dtypes in (
		"int64",
		"float64"
	)
]

target_column = st.selectbox(
	"Target column",
	numeric_columns
)

if st.button("Train Linear Regression"):

	metrics = asyncio.run(
		train_linear_regression(str(file_path), target_column)
	)

	st.session_state["metrics"] = metrics
	st.session_state["model_path"] = metrics["model_path"]

	st.metric("R2 Score", metrics["r2_score"])
	st.metric("MAE", metrics["mae"])
	st.metric("RMSE", metrics["rmse"])

	st.success(f"Model saved to: {metrics["model_path"]}")