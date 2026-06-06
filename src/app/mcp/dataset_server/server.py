from mcp.server.fastmcp import FastMCP
from app.mcp.dataset_server.tools import profile_dataset, get_schema

dataset_server_mcp = FastMCP("Dataset Server")

@dataset_server_mcp.tool()
def profile_dataset_tool(file_path):
	return profile_dataset(file_path)

@dataset_server_mcp.tool()
def get_schema_tool(file_path):
	return get_schema(file_path)

if __name__ == "__main__":
	print("dataset-server-mcp")
	dataset_server_mcp.run()