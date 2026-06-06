import pandas as pd
import plotly.express as px

def create_histogram(file_path, column):
	df = pd.read_csv(file_path)

	fig = px.histogram(
		df,
		x=column,
		title=f"Histogram of {column}"
	)

	return fig.to_json()