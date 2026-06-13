from mcp.server.fastmcp import FastMCP

from app.mcp.reporting_server.tools import generate_report

reporting_server_mcp = FastMCP("Reporting Server")

@reporting_server_mcp.tool()
def generate_report_tool(
	profile,
	schema,
	missing_values,
	duplicates,
	insights,
	metrics,
	model_path):
	return generate_report(
		profile,
		schema,
		missing_values,
		duplicates,
		insights,
		metrics,
		model_path)

if __name__ == "__main__":
	print("reporting-server-mcp")
	reporting_server_mcp.run()