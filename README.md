- Run MCP Servers

    ```
    uv run -m app.mcp.dataset_server.server
    uv run -m app.mcp.visualization_server.server
    uv run -m app.mcp.training_server.server
    ```

- Run Streamlit

    ```
    streamlit run src/app/ui/Home.py
    ```
