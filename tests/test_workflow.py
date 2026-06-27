import pytest
from pathlib import Path
from app.agent.workflow import build_ml_workflow, run_ml_workflow

def test_build_ml_workflow():
    app = build_ml_workflow()
    assert app is not None

def test_run_ml_workflow_end_to_end():
    result = run_ml_workflow(
        file_path="tests/data/sample.csv",
        target_column="exam_score"
    )
    
    assert result["status"] == "completed"
    assert "analysis" in result
    assert result["analysis"]["rows"] == 10
    assert "preprocessing_config" in result
    assert "selected_model_name" in result
    assert "metrics" in result
    assert "r2_score" in result["metrics"]
    assert "mae" in result["metrics"]
    assert "rmse" in result["metrics"]
    assert "ai_insights" in result
    assert "report_path" in result
    assert Path(result["report_path"]).exists()
    assert Path(result["model_path"]).exists()
    assert len(result["logs"]) >= 5

def test_run_ml_workflow_explicit_model():
    result = run_ml_workflow(
        file_path="tests/data/sample.csv",
        target_column="exam_score",
        selected_model_name="random_forest"
    )
    assert result["selected_model_name"] == "random_forest"
    assert "random forest" in result["model_selection_reasoning"].lower()
    assert result["status"] == "completed"
