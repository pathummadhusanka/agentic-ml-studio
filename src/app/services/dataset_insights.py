from app.llm.ollama_client import generate_response
from app.llm.prompts import DATASET_INSIGHT_PROMPT

def generate_dataset_insights(
		profile,
		schema,
		missing_values,
		duplicates
):
	dataset_info = f"""
Profile:
{profile}

Schema:
{schema}

Missing Values:
{missing_values}

Duplicates:
{duplicates}
"""
	
	prompt = DATASET_INSIGHT_PROMPT.format(dataset_info=dataset_info)

	return generate_response(prompt)