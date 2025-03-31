# AI Assistant 

## Overview

This project sets up a team of AI agents to perform various tasks such as retrieving web data, fetching financial information, processing structured data, and providing weather updates. The agents utilize the `phi` framework and models from `Groq` to handle different types of queries effectively.

## Features

- **Web Agent**: Fetches web data using DuckDuckGo.
- **Finance Agent**: Retrieves financial data, including stock prices, analyst recommendations, and company details, using `YFinanceTools`.
- **Data Agent**: Processes CSV and Excel files using `PandasTools`.
- **Weather Agent**: Provides real-time weather updates with sources.
- **Agent Team**: A combined agent that integrates `Web Agent` and `Finance Agent` for comprehensive responses.

## Dependencies

Ensure you have the following dependencies installed:

- Python 3.x (required runtime environment)

- `phi` (for AI agent framework)
- `dotenv` (for environment variable management)
- `io` and `sys` (for handling output capture)

- API keys for Groq or OpenAI (if using their models)

To install missing dependencies, run:

```sh
pip install phi python-dotenv
```

## Usage

1. **Run the script**:
   ```sh
   python agent_team.py
   ```
2. The script initializes multiple agents and executes a predefined query for financial and web-based data.
3. The output is captured and saved to `output.txt`.

## Configuration

- The script uses the `Groq` AI model (`llama-3.3-70b-versatile`).
- Uncomment lines to enable additional agents such as `Document Processor`.
- Modify `instructions` to customize agent behavior.

## Example Query

```python
agent_team.print_response("Summarize analyst recommendations and share the latest news for TSLA", stream=True)
```

## Output

The response is saved in `output.txt` for further analysis.

## Future Enhancements

- Enable document processing by adding `PDFReader` and `TextExtractor`.
- Extend functionality with additional AI models.
- Implement dynamic agent selection based on query type.
- Build a frontend using TypeScript to create a webpage for interacting with the AI agents and displaying responses dynamically.



