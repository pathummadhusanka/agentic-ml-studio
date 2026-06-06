
from contextlib import AsyncExitStack
import json
import sys
from mcp import ClientSession
from mcp.types import TextContent

from mcp.client.stdio import stdio_client, StdioServerParameters


async def call_dataset_tool(tool_name, arguments):
	server_params = StdioServerParameters(
		command=sys.executable,
		args=["-m", "app.mcp.dataset_server.server"]
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

async def profile_dataset(file_path):
	return await call_dataset_tool(
		"profile_dataset_tool",
		{"file_path": file_path}
	)

async def get_schema(file_path):
	return await call_dataset_tool(
		"get_schema_tool",
		{"file_path": file_path}
	)

async def detect_missing_values(file_path):
	return await call_dataset_tool(
		"detect_missing_values_tool",
		{"file_path": file_path}
	)

async def detect_duplicates(file_path):
	return await call_dataset_tool(
		"detect_duplicates_tool",
		{"file_path": file_path}
	)
