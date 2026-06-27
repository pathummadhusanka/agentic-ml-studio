DATASET_INSIGHT_PROMPT = """
You are a machine learning assistant.

Analyze the dataset information below.

Provide:

1. Dataset Summary
2. Potential Data Quality Issues
3. Recommended Preprocessing
4. Linear Regression Suitability

Dataset Information:

{dataset_info}
"""

WORKFLOW_EXPLANATION_PROMPT = """
You are an expert AI machine learning consultant reviewing an automated ML workflow run.

Dataset & Workflow Details:
- Dataset rows: {rows}, columns: {columns}
- Target feature: {target_column}
- Preprocessing: {preprocessing_summary}
- Selected Model: {selected_model}
- Model Selection Reason: {selection_reason}
- Evaluation Metrics: R² = {r2_score}, MAE = {mae}, RMSE = {rmse}

Provide a concise, professional analysis covering:
1. Data Quality & Preprocessing Assessment
2. Model Performance Interpretation (how well the model fits and what the errors mean)
3. Actionable Next Steps / Recommendations for Improvement
"""