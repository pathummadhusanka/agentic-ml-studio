from pathlib import Path
from typing import Dict, Any
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error

from app.agent.state import AgentState
from app.agent.nodes.preprocessing import prepare_features_and_target

def evaluate_model_pipeline(
    model_path: str,
    file_path: str,
    target_column: str,
    test_size: float = 0.2,
    random_state: int = 42
) -> Dict[str, float]:
    """
    Loads saved model pipeline and calculates real evaluation metrics on the test split.
    """
    pipeline = joblib.load(model_path)
    df = pd.read_csv(file_path)
    X, y, _, _ = prepare_features_and_target(df, target_column)
    
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    predictions = pipeline.predict(X_test)
    
    r2 = float(r2_score(y_test, predictions))
    mae = float(mean_absolute_error(y_test, predictions))
    rmse = float(root_mean_squared_error(y_test, predictions))
    
    return {
        "r2_score": round(r2, 4),
        "mae": round(mae, 4),
        "rmse": round(rmse, 4)
    }

def evaluation_node(state: AgentState) -> Dict[str, Any]:
    """
    LangGraph node for computing empirical regression metrics on held-out test data.
    """
    model_path = state.get("model_path", "")
    file_path = state.get("file_path", "")
    target_column = state.get("target_column", "")
    
    if not model_path or not file_path or not target_column:
        return {
            "errors": ["Model path, file path, and target column required for evaluation."],
            "status": "error"
        }
        
    logs = list(state.get("logs", []))
    logs.append("[Evaluation Agent] Computing evaluation metrics on test split...")
    
    metrics = evaluate_model_pipeline(
        model_path=model_path,
        file_path=file_path,
        target_column=target_column
    )
    
    logs.append(
        f"[Evaluation Agent] Results — R²: {metrics['r2_score']}, "
        f"MAE: {metrics['mae']}, RMSE: {metrics['rmse']}"
    )
    
    return {
        "metrics": metrics,
        "logs": logs,
        "status": "evaluated"
    }
