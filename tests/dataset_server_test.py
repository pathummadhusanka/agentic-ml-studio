from app.mcp.dataset_server.tools import profile_dataset

def test_profile_dataset():
	result = profile_dataset("tests/data/sample.csv")

	assert "rows" in result
	assert "columns" in result