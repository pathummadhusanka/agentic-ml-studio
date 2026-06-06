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

def create_heatmap(file_path):

    df = pd.read_csv(file_path)

    numeric_df = df.select_dtypes(
        include="number"
    )

    correlation_matrix = numeric_df.corr()

    fig = px.imshow(
        correlation_matrix,
        text_auto=True,
        title="Correlation Heatmap"
    )

    return fig.to_json()

def create_scatter_plot(
    file_path,
    x_column,
    y_column,
):
    df = pd.read_csv(file_path)

    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        title=f"{x_column} vs {y_column}",
    )

    return fig.to_json()