from pathlib import Path
import pandas as pd
import streamlit as st
from app.agent.workflow import run_ml_workflow
from app.agent.nodes.model_selection import SUPPORTED_MODELS

DATASET_DIR = Path("storage/datasets")
DATASET_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(page_title="Agentic ML Studio — Workflow", page_icon="🤖", layout="wide")

st.title("🤖 Agentic ML Studio — Multi-Agent Workflow")
st.markdown(
    "Coordinate automated dataset analysis, preprocessing, model selection, training, "
    "empirical evaluation, and AI insight generation using LangGraph."
)

st.divider()

# Dataset selection
existing_datasets = list(DATASET_DIR.glob("*.csv"))
dataset_options = [p.name for p in existing_datasets]

col_data1, col_data2 = st.columns([2, 1])

with col_data1:
    uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])
    if uploaded_file:
        file_path = DATASET_DIR / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Saved: {uploaded_file.name}")
        if uploaded_file.name not in dataset_options:
            dataset_options.append(uploaded_file.name)

with col_data2:
    selected_dataset_name = st.selectbox(
        "Or choose existing dataset",
        dataset_options,
        index=0 if dataset_options else None,
        placeholder="Select a dataset..."
    )

if not selected_dataset_name:
    st.info("Please upload or select a CSV dataset to get started.")
    st.stop()

selected_file_path = DATASET_DIR / selected_dataset_name

try:
    df_preview = pd.read_csv(selected_file_path)
except Exception as e:
    st.error(f"Error reading CSV: {e}")
    st.stop()

# Target Selection & Model Preference
st.subheader("Workflow Configuration")
col_conf1, col_conf2 = st.columns(2)

numeric_columns = df_preview.select_dtypes(include=["number"]).columns.tolist()

with col_conf1:
    target_column = st.selectbox(
        "Select Target Column (Regression)",
        numeric_columns,
        index=len(numeric_columns) - 1 if numeric_columns else 0,
        help="The numerical column you want the model to predict."
    )

with col_conf2:
    model_choices = {"auto": "Auto (Agent Heuristic / AI Choice)"}
    model_choices.update({k: v["display_name"] for k, v in SUPPORTED_MODELS.items()})
    
    selected_model_pref = st.selectbox(
        "Model Selection Preference",
        options=list(model_choices.keys()),
        format_func=lambda x: model_choices[x],
        index=0
    )

st.divider()

if st.button("🚀 Run Agentic Workflow", type="primary"):
    with st.spinner("Executing multi-agent workflow stages..."):
        chosen_model = None if selected_model_pref == "auto" else selected_model_pref
        result = run_ml_workflow(
            file_path=str(selected_file_path),
            target_column=target_column,
            selected_model_name=chosen_model
        )
        st.session_state["workflow_result"] = result

if "workflow_result" in st.session_state:
    res = st.session_state["workflow_result"]
    
    if res.get("status") == "error":
        st.error("Workflow encountered errors:")
        for err in res.get("errors", []):
            st.error(f"- {err}")
        st.stop()

    st.success("✨ Multi-Agent Workflow Completed Successfully!")
    
    # 1. Workflow Stage Progress Logs
    with st.expander("📋 Execution Logs & Agent Traces", expanded=False):
        for log_line in res.get("logs", []):
            st.text(log_line)
            
    # 2. Stage Summaries
    tab_analysis, tab_prep, tab_model, tab_metrics, tab_insights, tab_report = st.tabs([
        "1. Analysis",
        "2. Preprocessing",
        "3. Model Selection",
        "4. Evaluation",
        "5. AI Insights",
        "6. Final Report"
    ])
    
    analysis = res.get("analysis", {})
    with tab_analysis:
        st.subheader("Dataset Profile")
        m1, m2, m3 = st.columns(3)
        m1.metric("Rows", analysis.get("rows", 0))
        m2.metric("Columns", analysis.get("columns", 0))
        m3.metric("Duplicates", analysis.get("duplicates", 0))
        
        st.markdown("**Column Schema:**")
        st.json(analysis.get("schema", {}))
        
        st.markdown("**Missing Values:**")
        st.json(analysis.get("missing_values", {}))

    prep = res.get("preprocessing_config", {})
    with tab_prep:
        st.subheader("Configured Pipeline")
        st.markdown(f"- **Numeric Features ({len(prep.get('numeric_features', []))})**: {', '.join(prep.get('numeric_features', []))}")
        st.markdown(f"- **Categorical Features ({len(prep.get('categorical_features', []))})**: {', '.join(prep.get('categorical_features', [])) or 'None'}")
        st.markdown(f"- **Numeric Imputation**: `{prep.get('numeric_imputation')}` | **Scaling**: `{prep.get('scaling')}`")
        st.markdown(f"- **Categorical Imputation**: `{prep.get('categorical_imputation')}` | **Encoding**: `{prep.get('encoding')}`")

    with tab_model:
        st.subheader("Selected Model Architecture")
        model_name = res.get("selected_model_name", "linear_regression")
        display_name = SUPPORTED_MODELS.get(model_name, {}).get("display_name", model_name)
        st.info(f"**Selected Model:** {display_name}")
        st.markdown(f"**Rationale:** {res.get('model_selection_reasoning', '')}")
        st.markdown(f"**Saved Pipeline Artifact:** `{res.get('model_path', '')}`")

    metrics = res.get("metrics", {})
    with tab_metrics:
        st.subheader("Empirical Evaluation (20% Held-Out Test Split)")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("R² Score", metrics.get("r2_score", "N/A"))
        col_m2.metric("Mean Absolute Error (MAE)", metrics.get("mae", "N/A"))
        col_m3.metric("Root Mean Squared Error (RMSE)", metrics.get("rmse", "N/A"))

    with tab_insights:
        st.subheader("AI Consultant Insights")
        st.markdown(res.get("ai_insights", "No insights available."))

    with tab_report:
        st.subheader("Automated Markdown Report")
        report_content = res.get("report_content", "")
        if report_content:
            st.download_button(
                label="📥 Download Full Report (.md)",
                data=report_content,
                file_name=f"agent_report_{selected_dataset_name}.md",
                mime="text/markdown"
            )
            with st.expander("Preview Full Report", expanded=True):
                st.markdown(report_content)
