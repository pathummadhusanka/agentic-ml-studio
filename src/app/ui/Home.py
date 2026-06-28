import streamlit as st

st.set_page_config(page_title="Agentic ML Studio", page_icon="🚀", layout="wide")

st.title("🚀 Agentic ML Studio")
st.markdown(
    """
Welcome to **Agentic ML Studio** — an interactive and agentic machine learning environment powered by 
**LangGraph**, **scikit-learn**, **MCP (Model Context Protocol)**, and **Ollama**.

### Available Capabilities:

1. **🤖 Agentic Studio (`05_Agentic_Studio`)**:
   - Run an automated, end-to-end multi-agent ML workflow (Data Analysis → Preprocessing → Model Selection → Training → Evaluation → AI Insights → Report Generation).
2. **📁 Dataset Profiler (`00_Dataset`)**:
   - Upload CSV datasets and inspect schema, row/column counts, missing values, and duplicates.
3. **📊 Visualizations (`01_Visualizations`)**:
   - Generate interactive Plotly histograms, correlation matrices, and scatter plots.
4. **🧠 AI Insights (`02_Insights`)**:
   - Local LLM data quality inspection and preprocessing recommendations.
5. **⚙️ Manual Training (`03_Training`)**:
   - Train and save baseline Linear Regression models.
6. **📄 Report Generator (`04_Reporting`)**:
   - Compile and download summary reports.

---
*Select a page from the sidebar to begin.*
"""
)