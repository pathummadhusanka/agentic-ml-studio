from mcp.server.fastmcp import FastMCP
from app.mcp.visualization_server.tools import (
	create_histogram,
    create_heatmap
)

visualization_server_mcp = FastMCP("Visualization Server")

@visualization_server_mcp.tool()
def create_histogram_tool(file_path, column):
	return create_histogram(file_path, column)

@visualization_server_mcp.tool()
def create_heatmap_tool(
    file_path: str
):
    return create_heatmap(file_path)

if __name__ == "__main__":
    print("visualization-server-mcp")
    visualization_server_mcp.run()