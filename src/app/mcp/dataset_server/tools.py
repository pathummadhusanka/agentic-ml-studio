import pandas as pd

def profile_dataset(file_path):
	df = pd.read_csv(file_path)

	return {
		"rows": len(df),
		"columns": len(df.columns)
	}

def get_schema(file_path):
	df = pd.read_csv(file_path)

	return {
		column: str(dtype) for column, dtype in df.dtypes.items()
	}

def detect_missing_values(file_path: str) -> dict:
    df = pd.read_csv(file_path)

    return (
        df.isnull().sum().to_dict()
    )

def detect_duplicates(file_path: str) -> dict:
    df = pd.read_csv(file_path)

    return {
        "duplicate_rows": int(
            df.duplicated().sum()
        )
    }