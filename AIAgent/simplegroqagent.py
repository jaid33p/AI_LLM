from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model=Groq(id="deepseek-r1-distill-llama-70b")
)

agent.print_response("who is the President of India?")