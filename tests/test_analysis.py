import pytest
from app.agent.nodes.analysis import analyze_dataset, dataset_analysis_node
from app.agent.state import AgentState

def test_analyze_dataset():
    result = analyze_dataset("tests/data/sample.csv", target_column="exam_score")
    assert result["rows"] == 10
    assert result["columns"] == 3
    assert "hours_studied" in result["numeric_columns"]
    assert "sleep_hours" in result["numeric_columns"]
    assert "exam_score" in result["numeric_columns"]
    assert result["duplicates"] == 0
    assert "summary_statistics" in result
    assert "hours_studied" in result["summary_statistics"]

def test_dataset_analysis_node():
    state: AgentState = {
        "file_path": "tests/data/sample.csv",
        "target_column": "exam_score",
        "logs": []
    }
    update = dataset_analysis_node(state)
    assert update["status"] == "analyzed"
    assert "analysis" in update
    assert update["analysis"]["rows"] == 10
    assert len(update["logs"]) >= 2
