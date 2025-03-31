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
import os

# Load environment variables
load_dotenv()

# Define agents
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

# Create agent team
agent_team = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    team=[web_agent, finance_agent],
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

# List of questions to ask
questions = [
    "Compare the recent performance of AAPL and MSFT and summarize recent news about both companies",
    "What are the growth prospects for renewable energy stocks and which analysts are most bullish on the sector?",
    "Analyze the impact of recent Fed announcements on banking stocks like JPM and BAC",
    "What are the current market trends for AI companies and how does NVDA compare to its competitors?",
    "Summarize the latest earnings reports for Amazon and provide analyst outlook for the next quarter",
    "How have supply chain issues affected Tesla's stock price over the past year?",
    "Compare dividend yields of top energy companies and summarize recent industry news",
    "What are the key financial metrics for the top 3 cloud computing companies?",
    "Analyze recent market volatility and how it has affected tech stocks",
    "Provide an overview of ESG investing trends and which companies are rated highest by analysts"
]


def ask_question(question, save_to_file=True):
    """Ask a question to the agent team and optionally save the response to a file"""
    print(f"\n\n{'=' * 80}\nQUESTION: {question}\n{'=' * 80}\n")

    # Create a StringIO object to capture the output
    output_buffer = io.StringIO()

    # Redirect stdout to the StringIO object
    sys.stdout = output_buffer

    # Call the method (its printed output will go into the buffer)
    agent_team.print_response(question, stream=True)

    # Reset stdout to its original value
    sys.stdout = sys.__stdout__

    # Retrieve the captured output as a string
    output_string = output_buffer.getvalue()

    # Close the buffer
    output_buffer.close()

    # Print the output to console
    print(output_string)

    # Save the output to a text file if requested
    if save_to_file:
        # Create outputs directory if it doesn't exist
        os.makedirs("outputs", exist_ok=True)

        # Create a filename based on the first few words of the question
        filename = "_".join(question.split()[:5]).lower()
        filename = "".join(c if c.isalnum() or c == "_" else "" for c in filename)
        filepath = f"outputs/{filename}.txt"

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(f"QUESTION: {question}\n\n")
            file.write(output_string)

        print(f"Output saved to '{filepath}'")


# Ask a single question
# ask_question(questions[0])

# Ask all questions
def ask_all_questions():
    for i, question in enumerate(questions):
        print(f"\nProcessing question {i + 1}/{len(questions)}")
        ask_question(question)


# Uncomment one of these to run:
ask_question(questions[5])
# ask_all_questions()         # Ask all questions

# Or ask a custom question
# custom_question = "Summarize analyst recommendations and share the latest news for TSLA"
# ask_question(custom_question)