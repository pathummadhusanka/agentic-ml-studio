from mcp.server.fastmcp import FastMCP

from app.mcp.training_server.tools import (
	train_linear_regression
)

training_server_mcp = FastMCP("Training Server")

@training_server_mcp.tool()
def train_linear_regression_tool(file_path, target_column):
	return train_linear_regression(file_path, target_column)

if __name__ == "__main__":
	print("training-server-mcp")
	training_server_mcp.run()