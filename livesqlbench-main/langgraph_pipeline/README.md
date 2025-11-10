# LangGraph NL2SQL Pipeline

This directory transforms the NL2SQL process into a multi-node graph using LangGraph, enhancing observability and failure recovery capabilities.

## Directory Structure
- **`graph.py`**: Defines states, nodes, and conditional routing, assembling the entire graph.
- **`graph_runner.py`**: Command-line entry point to compile and run the graph, outputting results.
- **`__init__.py`**: Initializes the package.

## Dependencies
To use this pipeline, install the following dependencies:

```bash
pip install -U langgraph
# Optional: Persistent checkpoints (currently unused)
# pip install -U langgraph-checkpoint-sqlite
```

Additional dependencies already included in the project:
- `langchain-core`, `langchain-community`, `langchain-openai`, `langchain-anthropic`, `langchain-chroma`
- `chromadb`, `sqlalchemy`, `pydantic`

> **Note**: If LangChain-related dependencies are missing, install them using `scripts/config/requirements.txt`.

## Usage Instructions
1. Navigate to the `livesqlbench-main` directory:
   ```bash
   cd livesqlbench-main
   ```
2. Run an example query:
   ```bash
   python -m langgraph_pipeline.graph_runner \
     --db_id hospital_1 \
     --question "If John Smith was discharged on International Nurses Day, how many days was he hospitalized?"
   ```
3. (Optional) Save the output to a file:
   ```bash
   python -m langgraph_pipeline.graph_runner \
     --db_id hospital_1 \
     --question "..." \
     --output result.json
   ```

## Node Descriptions
- **`table_selection`**: Multi-stage table selection (coarse + refined), triggers intelligent sorting fallback when confidence is low; uses `TableSelector`.
- **`example_selection`**: Few-shot selection based on semantic similarity RAG; uses `ExampleSelector`.
- **`sql_generation`**: Dual-model generation (Anthropic/OpenAI) and selects the optimal result based on execution; uses `SQLGenerator`.
- **`validate_sql`**: Performs syntax validation using `EXPLAIN QUERY PLAN`, injects m-schema repair when necessary; uses `SQLValidator`.
- **`execute`**: Safe execution (SELECT only, automatically adds LIMIT); uses `SQLExecutor`.
- **`sql_repair`**: Repairs failed executions using runtime errors; retries up to 2 times.

## Design Highlights
- **State Management**: Tracks `question`, `db_id`, `selected_tables`, `examples`, `sql`, `exec_result`, `retries`, and `trace`.
- **Conditional Routing**: Implements `execute -> (success->END | fail->sql_repair->execute)`.
- **Compatibility**: Maintains consistent behavior with existing modules, avoiding the need to rewrite core logic.

## Common Issues
- **`ModuleNotFoundError`**: Ensure you run `python -m langgraph_pipeline.graph_runner` from the `livesqlbench-main` directory.
- **OpenAI/Anthropic API Issues**: Ensure environment variables/configurations are set correctly. Refer to `scripts/config.py` for `get_llm_instance` and `get_llm_anthropic` functions.

## Additional Resources
For more details, visit the [Archer official website](https://sig4kg.github.io/archer-bench/) to download the database and training data.