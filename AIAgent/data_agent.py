from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.tools.pandas import PandasTools
from dotenv import load_dotenv
import pandas as pd
import io
import sys
import os

# Load environment variables
load_dotenv()

# Web Agent (for searching online)
web_agent = Agent(
    name="Web Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True
)

# Finance Agent (for stock market data)
finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

# Data Processing Agent (for CSV/Excel analysis)
data_agent = Agent(
    name="Data Agent",
    role="Process CSV and Excel files",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[PandasTools()],
    instructions=["Provide insights from the data."],
    show_tool_calls=True,
    markdown=True
)

# Weather Agent (for fetching weather data)
weather_agent = Agent(
    name="Weather Agent",
    role="Provide current weather updates",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],  # Using DuckDuckGo as a general search tool for weather
    instructions=["Provide real-time weather information with sources."],
    show_tool_calls=True,
    markdown=True
)

# Creating the main agent team
agent_team = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    team=[web_agent, finance_agent, data_agent, weather_agent],
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

# --- TESTING DATA PROCESSING AGENT ---
# Create a sample CSV file for testing
csv_filename = "sample_data.csv"

# If the CSV file doesn't exist, create it
if not os.path.exists(csv_filename):
    data = {
        "Date": ["2024-03-01", "2024-03-02", "2024-03-03"],
        "Stock": ["TSLA", "TSLA", "TSLA"],
        "Price": [200, 210, 215],
        "Volume": [1500000, 1600000, 1400000]
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_filename, index=False)

# Ensure df is valid before analysis
if os.path.exists(csv_filename):
    df = pd.read_csv(csv_filename)

    # Capture the agent response
    output_buffer = io.StringIO()
    sys.stdout = output_buffer

    try:
        # Provide the file path directly instead of trying to pass it as a special object
        data_agent.run(message="Analyze trends in stock prices and provide insights from the dataset.", data={"csv_file": df.to_csv(index=False)})
    except Exception as e:
        print("Error during agent execution:", e)

    # Reset stdout to its original value
    sys.stdout = sys.__stdout__

    # Get the output from the buffer
    output_string = output_buffer.getvalue()
    output_buffer.close()

    # Save the output to a text file
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write(output_string)

    print("✅ Output saved to 'output.txt'")

else:
    print(f"❌ {csv_filename} does not exist!")
