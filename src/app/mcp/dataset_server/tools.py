import pandas as pd

def profile_dataset(file_path):
	df = pd.read_csv(file_path)

	return {
		"rows": len(df),
		"columns": len(df.columns)
	}