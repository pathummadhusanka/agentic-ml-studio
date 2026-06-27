from pathlib import Path
from typing import Dict, Any
from app.agent.state import AgentState
from app.agent.nodes.model_selection import SUPPORTED_MODELS

REPORT_DIR = Path("storage/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def generate_agent_report_content(state: AgentState) -> str:
    """Formats full workflow state into a detailed markdown report."""
    analysis = state.get("analysis", {})
    prep = state.get("preprocessing_config", {})
    model_name = state.get("selected_model_name", "linear_regression")
    display_name = SUPPORTED_MODELS.get(model_name, {}).get("display_name", model_name)
    metrics = state.get("metrics", {})
    insights = state.get("ai_insights", "No insights generated.")
    model_path = state.get("model_path", "N/A")
    file_path = state.get("file_path", "N/A")
    target_column = state.get("target_column", "N/A")
    
    return f"""# Agentic ML Studio — Automated Workflow Report

## 1. Dataset & Target Specification
- **Dataset File**: `{file_path}`
- **Target Variable**: `{target_column}`
- **Total Records**: {analysis.get('rows', 0)}
- **Total Features**: {analysis.get('columns', 0)}
- **Duplicate Records**: {analysis.get('duplicates', 0)}

## 2. Feature Schema & Missing Values
- **Numeric Columns ({len(analysis.get('numeric_columns', []))})**: {', '.join(analysis.get('numeric_columns', []))}
- **Categorical Columns ({len(analysis.get('categorical_columns', []))})**: {', '.join(analysis.get('categorical_columns', [])) or 'None'}
- **Missing Value Summary**:
```json
{analysis.get('missing_values', {})}
```

## 3. Data Preprocessing Pipeline
- **Numeric Handling**: {prep.get('numeric_imputation', 'median')} imputation + {prep.get('scaling', 'standard')} scaling
- **Categorical Handling**: {prep.get('categorical_imputation', 'most_frequent')} imputation + {prep.get('encoding', 'one_hot')} encoding

## 4. Model Selection & Architecture
- **Selected Model**: **{display_name}**
- **Selection Rationale**: {state.get('model_selection_reasoning', 'Default regression heuristic')}
- **Saved Model Artifact**: `{model_path}`

## 5. Empirical Evaluation Metrics (Test Split: 20%)
- **R² Score (Coefficient of Determination)**: {metrics.get('r2_score', 'N/A')}
- **Mean Absolute Error (MAE)**: {metrics.get('mae', 'N/A')}
- **Root Mean Squared Error (RMSE)**: {metrics.get('rmse', 'N/A')}

## 6. AI Insights & Recommendations
{insights}

---
*Report generated automatically by Agentic ML Studio workflow engine.*
"""

def reporting_node(state: AgentState) -> Dict[str, Any]:
    """
    LangGraph node for compiling and saving the final markdown report.
    """
    logs = list(state.get("logs", []))
    logs.append("[Reporting Agent] Compiling end-to-end markdown report...")
    
    report_content = generate_agent_report_content(state)
    report_path = REPORT_DIR / "agent_workflow_report.md"
    report_path.write_text(report_content, encoding="utf-8")
    
    logs.append(f"[Reporting Agent] Report successfully generated at '{report_path}'.")
    
    return {
        "report_path": str(report_path),
        "report_content": report_content,
        "logs": logs,
        "status": "completed"
    }
