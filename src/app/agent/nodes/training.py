from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error

from app.agent.state import AgentState
from app.agent.nodes.preprocessing import prepare_features_and_target, build_preprocessor
from app.agent.nodes.model_selection import get_model_instance, SUPPORTED_MODELS

MODEL_DIR = Path("storage/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

def train_model(
    file_path: str,
    target_column: str,
    model_name: str = "linear_regression",
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[Pipeline, str, pd.DataFrame, pd.Series]:
    """
    Trains the full preprocessing + regressor pipeline on train split and saves the pipeline artifact.
    """
    df = pd.read_csv(file_path)
    X, y, num_cols, cat_cols = prepare_features_and_target(df, target_column)
    
    # Train / test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    preprocessor = build_preprocessor(num_cols, cat_cols)
    regressor = get_model_instance(model_name)
    
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", regressor)
    ])
    
    pipeline.fit(X_train, y_train)
    
    model_path = MODEL_DIR / f"{model_name}.pkl"
    joblib.dump(pipeline, model_path)
    
    return pipeline, str(model_path), X_test, y_test

def training_node(state: AgentState) -> Dict[str, Any]:
    """
    LangGraph node for training the selected model with the preprocessing pipeline.
    """
    file_path = state.get("file_path", "")
    target_column = state.get("target_column", "")
    model_name = state.get("selected_model_name", "linear_regression")
    
    if not file_path or not target_column:
        return {
            "errors": ["File path and target column required for training."],
            "status": "error"
        }
        
    logs = list(state.get("logs", []))
    display_name = SUPPORTED_MODELS.get(model_name, {}).get("display_name", model_name)
    logs.append(f"[Training Agent] Training {display_name} on target '{target_column}'...")
    
    pipeline, model_path, X_test, y_test = train_model(
        file_path=file_path,
        target_column=target_column,
        model_name=model_name
    )
    
    logs.append(f"[Training Agent] Model successfully trained and saved to '{model_path}'.")
    
    return {
        "model_path": model_path,
        "logs": logs,
        "status": "trained"
    }
