import re
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import io
import sys

# Load environment variables
load_dotenv()

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

# Ask the Weather Agent for current weather
location = "New York"  # Replace with the city you want
query = f"What is the current weather in {location}?"

# Capture the agent response
output_buffer = io.StringIO()
sys.stdout = output_buffer

# Call the weather agent to search for the weather using DuckDuckGo
weather_agent.print_response(query, stream=True)

# Reset stdout to its original value
sys.stdout = sys.__stdout__

# Get the output from the buffer
output_string = output_buffer.getvalue()
output_buffer.close()

# Extracting specific weather data using regex
temperature_pattern = re.compile(r"(\d{1,2}\.\d{1,2}|\d{1,2})\s*°\s*(C|F)")
match = temperature_pattern.search(output_string)

if match:
    temperature = match.group(0)
    print(f"Temperature found: {temperature}")
else:
    print("No temperature data found.")

# Save the raw output to a text file
with open("weather_output.txt", "w", encoding="utf-8") as file:
    file.write(output_string)

print("Weather data saved to 'weather_output.txt'")
