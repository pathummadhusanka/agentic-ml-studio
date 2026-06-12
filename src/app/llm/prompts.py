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