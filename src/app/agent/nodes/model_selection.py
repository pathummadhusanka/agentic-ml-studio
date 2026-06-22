from typing import Dict, Any, Optional
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.base import BaseEstimator
from app.agent.state import AgentState

SUPPORTED_MODELS = {
    "linear_regression": {
        "display_name": "Linear Regression",
        "factory": lambda: LinearRegression(),
        "description": "Fast, interpretable linear model suitable for linear relationships."
    },
    "decision_tree": {
        "display_name": "Decision Tree Regressor",
        "factory": lambda: DecisionTreeRegressor(random_state=42),
        "description": "Non-linear tree model capable of capturing feature interactions."
    },
    "random_forest": {
        "display_name": "Random Forest Regressor",
        "factory": lambda: RandomForestRegressor(n_estimators=100, random_state=42),
        "description": "Ensemble of decision trees offering robust performance and reduced variance."
    },
    "gradient_boosting": {
        "display_name": "Gradient Boosting Regressor",
        "factory": lambda: GradientBoostingRegressor(n_estimators=100, random_state=42),
        "description": "Sequential ensemble model optimizing for high predictive accuracy."
    },
}

def get_model_instance(model_name: str) -> BaseEstimator:
    """Instantiates a scikit-learn regressor by canonical name."""
    if model_name not in SUPPORTED_MODELS:
        raise ValueError(
            f"Unsupported model '{model_name}'. Supported models: {list(SUPPORTED_MODELS.keys())}"
        )
    return SUPPORTED_MODELS[model_name]["factory"]()

def select_model_heuristics(
    sample_count: int,
    feature_count: int,
    has_categorical: bool = False
) -> Dict[str, str]:
    """
    Selects an appropriate regression model based on dataset characteristics.
    """
    if sample_count < 30:
        return {
            "model_name": "linear_regression",
            "reasoning": (
                f"Small dataset ({sample_count} samples). Linear Regression is selected "
                f"to prevent severe overfitting."
            )
        }
    elif sample_count < 150:
        if has_categorical or feature_count >= 5:
            return {
                "model_name": "random_forest",
                "reasoning": (
                    f"Moderate dataset size ({sample_count} samples) with multiple features/categories. "
                    f"Random Forest selected to capture non-linear relationships without high variance."
                )
            }
        else:
            return {
                "model_name": "decision_tree",
                "reasoning": (
                    f"Small-to-moderate dataset ({sample_count} samples). Decision Tree Regressor "
                    f"selected for balanced complexity and interpretability."
                )
            }
    else:
        return {
            "model_name": "gradient_boosting",
            "reasoning": (
                f"Sufficient sample size ({sample_count} samples). Gradient Boosting Regressor "
                f"selected for optimal predictive power and gradient optimization."
            )
        }

def model_selection_node(state: AgentState) -> Dict[str, Any]:
    """
    LangGraph node for evaluating dataset properties and selecting the regression model.
    """
    preprocessing_config = state.get("preprocessing_config", {})
    analysis = state.get("analysis", {})
    
    sample_count = preprocessing_config.get("sample_count", analysis.get("rows", 0))
    feature_count = preprocessing_config.get("feature_count", analysis.get("columns", 1) - 1)
    has_categorical = bool(preprocessing_config.get("categorical_features"))
    
    logs = list(state.get("logs", []))
    logs.append("[Model Selection Agent] Evaluating candidate models...")
    
    # If user explicitly requested a specific model in state, honor it
    candidate = state.get("selected_model_name")
    if candidate and candidate in SUPPORTED_MODELS:
        model_name = candidate
        reasoning = f"User explicitly selected {SUPPORTED_MODELS[model_name]['display_name']}."
    else:
        decision = select_model_heuristics(sample_count, feature_count, has_categorical)
        model_name = decision["model_name"]
        reasoning = decision["reasoning"]
        
    display_name = SUPPORTED_MODELS[model_name]["display_name"]
    logs.append(f"[Model Selection Agent] Selected '{display_name}'. Reason: {reasoning}")
    
    return {
        "selected_model_name": model_name,
        "model_selection_reasoning": reasoning,
        "logs": logs,
        "status": "model_selected"
    }
