import asyncio
from app.mcp.client.dataset_client import profile_dataset_via_mcp

async def main():
	result = await profile_dataset_via_mcp(
		"tests/data/sample.csv"
	)

	print(result)


asyncio.run(main())