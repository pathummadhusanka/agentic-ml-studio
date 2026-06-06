from contextlib import AsyncExitStack
import json
import sys
from mcp import ClientSession
from mcp.types import TextContent

from mcp.client.stdio import stdio_client, StdioServerParameters


async def call_dataset_tool(tool_name, arguments):
	server_params = StdioServerParameters(
		command=sys.executable,
		args=["-m", "app.mcp.visualization_server.server"]
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
			return content.text
		
		raise ValueError(
			f"Unexpected response type: {type(content)}"
		)

async def create_histogram(file_path, column):
	return await call_dataset_tool(
		"create_histogram_tool",
		{
			"file_path": file_path,
			"column": column
			}
	)