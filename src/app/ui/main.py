import streamlit as st
from pathlib import Path
import asyncio

from app.mcp.client.dataset_client import (
	profile_dataset,
	get_schema,
	detect_missing_values,
	detect_duplicates
)

DATASET_DIR = Path("storage/datasets")
DATASET_DIR.mkdir(parents=True, exist_ok=True)

st.title("Agentic ML Studio")

uploaded_csv_file = st.file_uploader(
	"Upload CSV file",
	type=["csv"]
)

if uploaded_csv_file:
	file_path = DATASET_DIR / uploaded_csv_file.name

	with open(file_path, "wb") as f:
		f.write(uploaded_csv_file.getbuffer())
	
	st.write(file_path)

	if st.button("Analyze Dataset"):

		profile = asyncio.run(
			profile_dataset(str(file_path))
		)

		schema = asyncio.run(
			get_schema(str(file_path))
		)

		missing_values = asyncio.run(
			detect_missing_values(str(file_path))
		)

		duplicates = asyncio.run(
			detect_duplicates(str(file_path))
		)

		st.subheader("Dataset Summary")

		col1, col2 = st.columns(2)

		col1.metric(
			"Rows",
			profile["rows"]
		)

		col2.metric(
			"Columns",
			profile["columns"]
		)

		st.subheader("Schema")
		st.json(schema)

		st.subheader("Missing Values")
		st.json(missing_values)

		st.subheader("Duplicates")
		st.metric(
			"Duplicate Rows",
			duplicates[
				"duplicate_rows"
			]
		)

