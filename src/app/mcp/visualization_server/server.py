from mcp.server.fastmcp import FastMCP
from app.mcp.visualization_server.tools import (
	create_histogram
)

visualization_server_mcp = FastMCP("Visualization Server")

@visualization_server_mcp.tool()
def create_histogram_tool(file_path, column):
	return create_histogram(file_path, column)

if __name__ == "__main__":
    print("visualization-server-mcp")
    visualization_server_mcp.run()