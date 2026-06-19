import pandas as pd
from typing import Dict, Any, List
from app.mcp.dataset_server.tools import (
    profile_dataset,
    get_schema,
    detect_missing_values,
    detect_duplicates,
)
from app.agent.state import AgentState

def analyze_dataset(file_path: str, target_column: str = "") -> Dict[str, Any]:
    """
    Analyzes a CSV dataset and returns structured metadata including
    dimensions, schema, missing values, duplicates, column types, and summary statistics.
    """
    df = pd.read_csv(file_path)
    
    profile = profile_dataset(file_path)
    schema = get_schema(file_path)
    missing_values = detect_missing_values(file_path)
    duplicates = detect_duplicates(file_path)
    
    numeric_cols: List[str] = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols: List[str] = df.select_dtypes(include=["object", "string", "str", "category", "bool"]).columns.tolist()
    
    # Calculate basic numeric summary statistics
    numeric_df = df[numeric_cols] if numeric_cols else pd.DataFrame()
    summary_stats = {}
    if not numeric_df.empty:
        stats_df = numeric_df.describe().round(4)
        summary_stats = stats_df.to_dict()

    return {
        "rows": profile["rows"],
        "columns": profile["columns"],
        "schema": schema,
        "missing_values": missing_values,
        "duplicates": duplicates["duplicate_rows"],
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "summary_statistics": summary_stats,
        "target_column": target_column,
    }

def dataset_analysis_node(state: AgentState) -> Dict[str, Any]:
    """LangGraph node for dataset exploration and profiling."""
    file_path = state.get("file_path", "")
    target_column = state.get("target_column", "")
    
    if not file_path:
        return {
            "errors": ["Dataset file path is required for analysis."],
            "status": "error"
        }
    
    logs = list(state.get("logs", []))
    logs.append(f"[Data Analysis Agent] Analyzing dataset: {file_path}")
    
    analysis = analyze_dataset(file_path, target_column)
    logs.append(
        f"[Data Analysis Agent] Detected {analysis['rows']} rows, {analysis['columns']} columns "
        f"({len(analysis['numeric_columns'])} numeric, {len(analysis['categorical_columns'])} categorical)."
    )
    
    return {
        "analysis": analysis,
        "logs": logs,
        "status": "analyzed"
    }
