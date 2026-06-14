from typing import Optional, TypedDict, Any, List, Dict

class AgentState(TypedDict, total=False):
    file_path: str
    target_column: str
    analysis: Optional[Dict[str, Any]]
    preprocessing_config: Optional[Dict[str, Any]]
    selected_model_name: Optional[str]
    model_selection_reasoning: Optional[str]
    metrics: Optional[Dict[str, float]]
    model_path: Optional[str]
    report_path: Optional[str]
    report_content: Optional[str]
    ai_insights: Optional[str]
    status: Optional[str]
    errors: Optional[List[str]]
    logs: Optional[List[str]]
