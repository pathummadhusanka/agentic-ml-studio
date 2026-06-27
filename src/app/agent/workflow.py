from typing import Optional
from langgraph.graph import StateGraph, START, END
from app.agent.state import AgentState
from app.agent.nodes import (
    dataset_analysis_node,
    preprocessing_node,
    model_selection_node,
    training_node,
    evaluation_node,
    insights_node,
    reporting_node,
)

def build_ml_workflow():
    """
    Compiles the end-to-end LangGraph state machine workflow for Agentic ML Studio.
    Flow: START -> analysis -> preprocessing -> model_selection -> training -> evaluation -> insights -> reporting -> END
    """
    workflow = StateGraph(AgentState)
    
    workflow.add_node("analysis", dataset_analysis_node)
    workflow.add_node("preprocessing", preprocessing_node)
    workflow.add_node("model_selection", model_selection_node)
    workflow.add_node("training", training_node)
    workflow.add_node("evaluation", evaluation_node)
    workflow.add_node("insights", insights_node)
    workflow.add_node("reporting", reporting_node)
    
    workflow.add_edge(START, "analysis")
    workflow.add_edge("analysis", "preprocessing")
    workflow.add_edge("preprocessing", "model_selection")
    workflow.add_edge("model_selection", "training")
    workflow.add_edge("training", "evaluation")
    workflow.add_edge("evaluation", "insights")
    workflow.add_edge("insights", "reporting")
    workflow.add_edge("reporting", END)
    
    return workflow.compile()

def run_ml_workflow(
    file_path: str,
    target_column: str,
    selected_model_name: Optional[str] = None
) -> AgentState:
    """
    Executes the full agentic ML workflow with initial parameters.
    """
    app = build_ml_workflow()
    initial_state: AgentState = {
        "file_path": file_path,
        "target_column": target_column,
        "selected_model_name": selected_model_name,
        "logs": []
    }
    return app.invoke(initial_state)
