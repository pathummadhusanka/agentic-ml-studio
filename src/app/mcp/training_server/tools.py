import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
	r2_score,
	mean_absolute_error,
	root_mean_squared_error
)
from pathlib import Path
import joblib

MODEL_DIR = Path("storage/models")

MODEL_DIR.mkdir(parents=True, exist_ok=True)

def train_linear_regression(file_path, target_column):
	df = pd.read_csv(file_path)

	X = df.drop(columns=[target_column])
	y = df[target_column]

	X = X.select_dtypes(
		include="number"
	)

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

	model = LinearRegression()

	model.fit(X_train, y_train)

	model_path = MODEL_DIR / "linear_regression.pkl"

	joblib.dump(model, model_path)

	predictions = model.predict(X_test)

	r2 = r2_score(y_test, predictions)
	mae = mean_absolute_error(y_test, predictions)
	rmse = root_mean_squared_error(y_test, predictions)

	return {
		"r2_score": round(r2, 4),
		"mae": round(mae, 4),
		"rmse": round(rmse, 4),
		"model_path": str(model_path)
	}
