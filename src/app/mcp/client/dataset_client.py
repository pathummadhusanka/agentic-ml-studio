
from contextlib import AsyncExitStack
import json

from mcp import ClientSession
from mcp.types import TextContent

from mcp.client.stdio import stdio_client, StdioServerParameters

async def profile_dataset_via_mcp(file_path):

	print("profile_dataset_via_mcp")

	server_params = StdioServerParameters(
		command="python",
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
			"profile_dataset_tool",
			{"file_path": file_path}
		)

		content = result.content[0]

		if isinstance(content, TextContent):
			return json.loads(content.text)
		
		raise ValueError(
			f"Unexpected response type: {type(content)}"
		)