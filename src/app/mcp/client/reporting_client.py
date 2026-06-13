
from contextlib import AsyncExitStack
import json
import sys
from mcp import ClientSession
from mcp.types import TextContent

from mcp.client.stdio import stdio_client, StdioServerParameters


async def call_training_tool(tool_name, arguments):
	server_params = StdioServerParameters(
		command=sys.executable,
		args=["-m", "app.mcp.reporting_server.server"]
	)

	async with AsyncExitStack() as stack:
		read, write = await stack.enter_async_context(
			stdio_client(server_params)
		)

		session = await stack.enter_async_context(
			ClientSession(read, write)
		)

		await session.initialize()

		result = await session.call_tool(
			tool_name,
			arguments
		)

		content = result.content[0]

		if isinstance(content, TextContent):
			return json.loads(content.text)
		
		raise ValueError(
			f"Unexpected response type: {type(content)}"
		)

async def generate_report(
	profile,
	schema,
	missing_values,
	duplicates,
	insights,
	metrics,
	model_path
):
	return await call_training_tool(
		"generate_report_tool",
		{
			"profile": profile,
			"schema": schema,
			"missing_values": missing_values,
			"duplicates": duplicates,
			"insights": insights,
			"metrics": metrics,
			"model_path": model_path
		}
	)
