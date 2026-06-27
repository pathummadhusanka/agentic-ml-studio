from typing import Dict, Any
from app.agent.state import AgentState
from app.agent.nodes.model_selection import SUPPORTED_MODELS
from app.llm.ollama_client import generate_response
from app.llm.prompts import WORKFLOW_EXPLANATION_PROMPT

def generate_heuristic_insights(state: AgentState) -> str:
    """Generates deterministic rule-based insights when LLM is unavailable."""
    analysis = state.get("analysis", {})
    metrics = state.get("metrics", {})
    model_name = state.get("selected_model_name", "linear_regression")
    display_name = SUPPORTED_MODELS.get(model_name, {}).get("display_name", model_name)
    r2 = metrics.get("r2_score", 0.0)
    mae = metrics.get("mae", 0.0)
    rmse = metrics.get("rmse", 0.0)
    
    fit_quality = "strong" if r2 > 0.8 else ("moderate" if r2 > 0.5 else "weak")
    
    return f"""### Automated ML Studio Insights

1. **Data Overview**:
   - Analyzed dataset with {analysis.get('rows', 0)} samples and {analysis.get('columns', 0)} total columns.
   - Identified {len(analysis.get('numeric_columns', []))} numeric features and {len(analysis.get('categorical_columns', []))} categorical features.

2. **Model Performance**:
   - Model: **{display_name}**
   - R² Score: **{r2}** ({fit_quality} variance explained).
   - Mean Absolute Error (MAE): **{mae}**
   - Root Mean Squared Error (RMSE): **{rmse}**

3. **Recommendations**:
   - {"The model exhibits strong predictive accuracy." if r2 > 0.8 else "Consider collecting more training samples or engineering non-linear interaction features."}
   - Inspect feature importances and residuals to detect potential heteroscedasticity.
"""

def insights_node(state: AgentState) -> Dict[str, Any]:
    """
    LangGraph node for generating AI-powered workflow analysis and recommendations.
    Uses Ollama with fallback to deterministic heuristic insights if LLM service is offline.
    """
    logs = list(state.get("logs", []))
    logs.append("[Insights Agent] Generating AI interpretation and recommendations...")
    
    analysis = state.get("analysis", {})
    prep = state.get("preprocessing_config", {})
    metrics = state.get("metrics", {})
    model_name = state.get("selected_model_name", "linear_regression")
    display_name = SUPPORTED_MODELS.get(model_name, {}).get("display_name", model_name)
    
    prompt = WORKFLOW_EXPLANATION_PROMPT.format(
        rows=analysis.get("rows", 0),
        columns=analysis.get("columns", 0),
        target_column=state.get("target_column", ""),
        preprocessing_summary=f"{len(prep.get('numeric_features', []))} numeric, {len(prep.get('categorical_features', []))} categorical",
        selected_model=display_name,
        selection_reason=state.get("model_selection_reasoning", "Heuristic selection"),
        r2_score=metrics.get("r2_score", "N/A"),
        mae=metrics.get("mae", "N/A"),
        rmse=metrics.get("rmse", "N/A")
    )
    
    try:
        insights = generate_response(prompt)
        logs.append("[Insights Agent] Successfully generated Ollama LLM insights.")
    except Exception as e:
        logs.append(f"[Insights Agent] Ollama unavailable ({type(e).__name__}). Using heuristic insights.")
        insights = generate_heuristic_insights(state)
        
    return {
        "ai_insights": insights,
        "logs": logs,
        "status": "insights_generated"
    }
