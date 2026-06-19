import pytest
import pandas as pd
import numpy as np
from app.agent.nodes.preprocessing import (
    build_preprocessor,
    prepare_features_and_target,
    preprocessing_node
)
from app.agent.state import AgentState

def test_prepare_features_and_target():
    df = pd.DataFrame({
        "age": [25, np.nan, 30, 45],
        "city": ["NY", "London", np.nan, "Tokyo"],
        "salary": [50000, 60000, 75000, 90000]
    })
    X, y, num_cols, cat_cols = prepare_features_and_target(df, "salary")
    assert "salary" not in X.columns
    assert num_cols == ["age"]
    assert cat_cols == ["city"]
    assert len(y) == 4

def test_build_preprocessor_transform():
    df = pd.DataFrame({
        "age": [25.0, np.nan, 35.0, 45.0],
        "city": ["NY", "London", "NY", "Tokyo"],
        "salary": [50000, 60000, 75000, 90000]
    })
    X, y, num_cols, cat_cols = prepare_features_and_target(df, "salary")
    preprocessor = build_preprocessor(num_cols, cat_cols)
    transformed = preprocessor.fit_transform(X)
    
    # Transformed output should have no NaNs and should include scaled age + onehot encoded city columns
    assert not np.isnan(transformed).any()
    assert transformed.shape[0] == 4
    assert transformed.shape[1] >= 4  # 1 numeric + 3 categories

def test_preprocessing_node():
    state: AgentState = {
        "file_path": "tests/data/sample.csv",
        "target_column": "exam_score",
        "logs": []
    }
    update = preprocessing_node(state)
    assert update["status"] == "preprocessed"
    assert "preprocessing_config" in update
    assert update["preprocessing_config"]["numeric_features"] == ["hours_studied", "sleep_hours"]
