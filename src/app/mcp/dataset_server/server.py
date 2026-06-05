from mcp.server.fastmcp import FastMCP
from app.mcp.dataset_server.tools import profile_dataset

dataset_server_mcp = FastMCP("Dataset Server")

@dataset_server_mcp.tool()
def profile_dataset_tool(file_path):
	return profile_dataset(file_path)

if __name__ == "__main__":
	dataset_server_mcp.run()