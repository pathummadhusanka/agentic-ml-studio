from typing import Dict, Any, List, Tuple
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from app.agent.state import AgentState

def build_preprocessor(
    numeric_features: List[str],
    categorical_features: List[str],
    scale_numeric: bool = True
) -> ColumnTransformer:
    """
    Builds a scikit-learn ColumnTransformer for handling numeric and categorical features.
    """
    transformers = []
    
    if numeric_features:
        num_steps = [("imputer", SimpleImputer(strategy="median"))]
        if scale_numeric:
            num_steps.append(("scaler", StandardScaler()))
        num_pipeline = Pipeline(steps=num_steps)
        transformers.append(("num", num_pipeline, numeric_features))
        
    if categorical_features:
        cat_pipeline = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ])
        transformers.append(("cat", cat_pipeline, categorical_features))
        
    return ColumnTransformer(transformers=transformers, remainder="drop")

def prepare_features_and_target(
    df: pd.DataFrame,
    target_column: str
) -> Tuple[pd.DataFrame, pd.Series, List[str], List[str]]:
    """
    Separates X and y, dropping rows where target is NaN, and identifies feature column types.
    """
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset.")
        
    # Drop rows where target is missing
    clean_df = df.dropna(subset=[target_column]).copy()
    
    X = clean_df.drop(columns=[target_column])
    y = clean_df[target_column]
    
    numeric_features = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_features = X.select_dtypes(include=["object", "string", "str", "category", "bool"]).columns.tolist()
    
    return X, y, numeric_features, categorical_features

def preprocessing_node(state: AgentState) -> Dict[str, Any]:
    """
    LangGraph node for determining and configuring preprocessing strategy.
    """
    file_path = state.get("file_path", "")
    target_column = state.get("target_column", "")
    
    if not file_path or not target_column:
        return {
            "errors": ["Dataset file path and target column are required for preprocessing."],
            "status": "error"
        }
        
    logs = list(state.get("logs", []))
    logs.append(f"[Preprocessing Agent] Configuring pipeline for target '{target_column}'")
    
    df = pd.read_csv(file_path)
    X, y, num_cols, cat_cols = prepare_features_and_target(df, target_column)
    
    preprocessing_config = {
        "numeric_features": num_cols,
        "categorical_features": cat_cols,
        "target_column": target_column,
        "numeric_imputation": "median",
        "categorical_imputation": "most_frequent",
        "scaling": "standard",
        "encoding": "one_hot",
        "feature_count": len(num_cols) + len(cat_cols),
        "sample_count": len(X)
    }
    
    logs.append(
        f"[Preprocessing Agent] Configured {len(num_cols)} numeric features (median imputer + standard scaler) "
        f"and {len(cat_cols)} categorical features (mode imputer + one-hot encoder)."
    )
    
    return {
        "preprocessing_config": preprocessing_config,
        "logs": logs,
        "status": "preprocessed"
    }
