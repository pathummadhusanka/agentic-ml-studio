import asyncio
from pathlib import Path

import streamlit as st

from app.mcp.client.dataset_client import (
    profile_dataset,
    get_schema,
    detect_missing_values,
    detect_duplicates,
)

st.title("Agentic ML Studio")