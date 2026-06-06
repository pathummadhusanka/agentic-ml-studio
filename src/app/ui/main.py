import streamlit as st
from pathlib import Path
import asyncio

from app.mcp.client.dataset_client import profile_dataset, get_schema

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

		result = asyncio.run(
			profile_dataset(str(file_path))
		)

		st.subheader("Dataset Profile")
		st.json(result)

		result = asyncio.run(
			get_schema(file_path)
		)

		st.subheader("Dataset Schema")
		st.json(result)