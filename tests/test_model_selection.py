import pytest
from app.agent.nodes.model_selection import (
    SUPPORTED_MODELS,
    get_model_instance,
    select_model_heuristics,
    model_selection_node
)
from app.agent.state import AgentState

def test_supported_models_suite():
    expected_models = ["linear_regression", "decision_tree", "random_forest", "gradient_boosting"]
    for model_name in expected_models:
        assert model_name in SUPPORTED_MODELS
        instance = get_model_instance(model_name)
        assert hasattr(instance, "fit")
        assert hasattr(instance, "predict")

def test_unsupported_model_raises():
    with pytest.raises(ValueError):
        get_model_instance("unsupported_nn")

def test_select_model_heuristics():
    # Small dataset -> Linear Regression
    res1 = select_model_heuristics(sample_count=15, feature_count=2)
    assert res1["model_name"] == "linear_regression"
    
    # Moderate dataset with categories -> Random Forest
    res2 = select_model_heuristics(sample_count=80, feature_count=6, has_categorical=True)
    assert res2["model_name"] == "random_forest"
    
    # Large dataset -> Gradient Boosting
    res3 = select_model_heuristics(sample_count=500, feature_count=10)
    assert res3["model_name"] == "gradient_boosting"

def test_model_selection_node():
    state: AgentState = {
        "preprocessing_config": {
            "sample_count": 20,
            "feature_count": 2,
            "categorical_features": []
        },
        "logs": []
    }
    update = model_selection_node(state)
    assert update["status"] == "model_selected"
    assert update["selected_model_name"] == "linear_regression"
    assert "reasoning" in update["model_selection_reasoning"].lower() or "linear" in update["model_selection_reasoning"].lower()
