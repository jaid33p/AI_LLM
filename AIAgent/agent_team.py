from phi.agent import Agent
from phi.document.reader.pdf import PDFReader
from phi.model.openai import OpenAIChat
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.tools.pandas import PandasTools
from dotenv import load_dotenv
import io
import sys

load_dotenv()

web_agent = Agent(
    name="Web Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    # model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=Groq(id="llama-3.3-70b-versatile"),
    # model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

# Data Processing Agent
data_agent = Agent(
    name="Data Agent",
    role="Process CSV and Excel files",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[PandasTools()],
    instructions=["Provide insights from the data."],
    show_tool_calls=True,
    markdown=True
)

# doc_agent = Agent(
#     name="Document Processor",
#     model=Groq(id="llama-3.3-70b-versatile"),
#     tools=[PDFReader(), TextExtractor()],
#     instructions=["Extract text and summarize documents"],
#     show_tool_calls=True,
#     markdown=True,
# )

# Weather Agent (for fetching weather data)
weather_agent = Agent(
    name="Weather Agent",
    role="Provide current weather updates",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=["Provide real-time weather information with sources."],
    show_tool_calls=True,
    markdown=True
)

agent_team = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    team=[web_agent, finance_agent],
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

# Create a StringIO object to capture the output
output_buffer = io.StringIO()

# Redirect stdout to the StringIO object
sys.stdout = output_buffer

# Call the method (its printed output will go into the buffer)
agent_team.print_response("Summarize analyst recommendations and share the latest news for TSLA", stream=True)
# web_agent.print_response("Who is the president of india?", stream=True)
# weather_agent.print_response("What is the current weather in New York", stream=True)

# Reset stdout to its original value
sys.stdout = sys.__stdout__

# Retrieve the captured output as a string
output_string = output_buffer.getvalue()

# Close the buffer
output_buffer.close()

# Save the output to a text file
with open("output.txt", "w", encoding="utf-8") as file:
    file.write(output_string)

print("Output saved to 'output.txt'")
