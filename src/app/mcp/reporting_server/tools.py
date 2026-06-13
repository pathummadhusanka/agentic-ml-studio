from pathlib import Path

REPORT_DIR = Path("storage/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def generate_report(
	profile,
	schema,
	missing_values,
	duplicates,
	insights,
	metrics,
	model_path		
):

	report_content = f"""
# Machine Learning Report

## Dataset Summary

Rows: {profile["rows"]}

Columns: {profile["columns"]}

## Missing Values

{missing_values}

## Duplicates

{duplicates}

## AI Insights

{insights}

## Model Metrics

R² Score: {metrics["r2_score"]}

MAE: {metrics["mae"]}

RMSE: {metrics["rmse"]}

## Saved Model

{model_path}
"""

	report_path = REPORT_DIR / "report.md"

	report_path.write_text(report_content, encoding="utf-8")

	return {
		"report_path": str(report_path)
	}

