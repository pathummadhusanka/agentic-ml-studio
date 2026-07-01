# Agentic ML Studio — Project Status & Feature Summary

**Current Version:** `0.1.0`  
**Status:** Functional Prototype / Active Development  
**Last Updated:** September 2026

---

## 1. Project Overview

**Agentic ML Studio** is an agentic, modular machine learning studio that combines a **Streamlit** multi-page user interface with **Model Context Protocol (MCP)** tool servers and a local **Ollama** LLM backend. It allows users to upload datasets, inspect data quality, generate interactive visualizations, obtain automated AI dataset insights, train baseline machine learning models, and export comprehensive markdown reports.

---

## 2. Architecture & Tech Stack

- **UI Layer:** Streamlit (Multi-page app: Home, Dataset, Visualizations, Insights, Training, Reporting)
- **Tool Protocol:** Model Context Protocol (FastMCP via `mcp` stdio sessions)
- **Data & ML Processing:** `pandas`, `scikit-learn`, `joblib`, `plotly`
- **LLM Integration:** `ollama` (defaulting to `llama3`)
- **Package & Environment Management:** `uv` / `pyproject.toml` (Python `>= 3.14`)

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit UI (Pages)                  │
└───────┬──────────────┬──────────────┬─────────────┬─────┘
        │ (MCP Stdio)  │ (MCP Stdio)  │ (Ollama)    │ (MCP Stdio)
        ▼              ▼              ▼             ▼
┌──────────────┐ ┌──────────────┐ ┌──────────┐ ┌──────────────┐
│Dataset Server│ │Visualization │ │ Insights │ │Training &    │
│    (MCP)     │ │ Server (MCP) │ │ Service  │ │Report Servers│
└──────────────┘ └──────────────┘ └──────────┘ └──────────────┘
```

---

## 3. Implemented Features

### 📁 1. Dataset Management & Profiling (`00_Dataset.py` & `dataset_server`)
- **CSV Upload & Storage:** Local dataset persistence in `storage/datasets/`.
- **Dataset Profiling:** Row and column count computation.
- **Schema Detection:** Column data type extraction (`dtypes`).
- **Data Quality Checks:** Missing value counts per column and duplicate row identification.
- **MCP Server Tools:** `profile_dataset_tool`, `get_schema_tool`, `detect_missing_values_tool`, `detect_duplicates_tool`.

### 📊 2. Interactive Visualizations (`01_Visualizations.py` & `visualization_server`)
- **Histograms:** Distribution plots for selected columns.
- **Correlation Heatmap:** Interactive correlation matrix for all numeric columns.
- **Scatter Plots:** Custom 2D scatter plots between selectable numeric variables.
- **Plotly Integration:** Serialized via JSON over MCP and rendered natively in Streamlit.
- **MCP Server Tools:** `create_histogram`, `create_heatmap`, `create_scatter_plot`.

### 🧠 3. AI Insights (`02_Insights.py` & `dataset_insights`)
- **Automated Quality Analysis:** Uses Ollama (`llama3`) to assess summary statistics, missing values, duplicates, and schema.
- **Actionable Recommendations:** Generates preprocessing suggestions and evaluates data suitability for regression modeling.

### ⚙️ 4. Model Training (`03_Training.py` & `training_server`)
- **Target Selection:** UI dropdown of numeric target variables.
- **Model Pipeline:** Automated 80/20 train-test split, numeric feature selection, and Scikit-Learn `LinearRegression` fitting.
- **Evaluation Metrics:** Automatic computation of $R^2$ Score, MAE, and RMSE.
- **Model Persistence:** Serialized model export to `storage/models/linear_regression.pkl` via `joblib`.
- **MCP Server Tools:** `train_linear_regression`.

### 📄 5. Automated Reporting (`04_Reporting.py` & `reporting_server`)
- **Report Aggregation:** Combines dataset summary, missing values, duplicates, AI insights, model performance metrics, and model artifact paths.
- **Markdown Export:** Generates formatted `storage/reports/report.md`.
- **Download Capability:** Direct in-browser markdown file download.
- **MCP Server Tools:** `generate_report`.

---

## 4. Storage Structure

- `storage/datasets/` — Uploaded CSV datasets
- `storage/models/` — Serialized trained models (`.pkl`)
- `storage/reports/` — Exported markdown reports

---

## 5. Potential Next Steps / Roadmap

1. **Multi-Model Training:** Add support for classification, decision trees, Random Forests, and Gradient Boosting.
2. **Data Preprocessing Pipeline:** Automated missing value imputation, categorical encoding, and feature scaling.
3. **Model Configuration:** Configurable hyperparameters and cross-validation directly from the UI.
4. **LLM Provider Options:** Support for external API providers (OpenAI, Anthropic, Gemini) alongside local Ollama.
