import pytest
from pathlib import Path
from app.agent.nodes.training import train_model, training_node
from app.agent.nodes.evaluation import evaluate_model_pipeline, evaluation_node
from app.agent.state import AgentState

def test_train_and_evaluate_pipeline():
    pipeline, model_path, X_test, y_test = train_model(
        file_path="tests/data/sample.csv",
        target_column="exam_score",
        model_name="linear_regression"
    )
    assert Path(model_path).exists()
    assert hasattr(pipeline, "predict")
    
    metrics = evaluate_model_pipeline(
        model_path=model_path,
        file_path="tests/data/sample.csv",
        target_column="exam_score"
    )
    assert "r2_score" in metrics
    assert "mae" in metrics
    assert "rmse" in metrics
    assert isinstance(metrics["r2_score"], float)
    assert isinstance(metrics["mae"], float)
    assert isinstance(metrics["rmse"], float)

def test_training_and_evaluation_nodes():
    state: AgentState = {
        "file_path": "tests/data/sample.csv",
        "target_column": "exam_score",
        "selected_model_name": "decision_tree",
        "logs": []
    }
    
    train_update = training_node(state)
    assert train_update["status"] == "trained"
    assert "model_path" in train_update
    
    eval_state = {**state, **train_update}
    eval_update = evaluation_node(eval_state)
    assert eval_update["status"] == "evaluated"
    assert "metrics" in eval_update
    assert eval_update["metrics"]["mae"] >= 0
