from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


def simulate_outreach(lead_data):
    return f"Simulated email to {lead_data['company']}: Hello, interested in out product?"

engagement_agent = Agent(
    role='Engager',
    goal='Handle initial outreach based on score',
    backstory='Automates communication for qualified leads',
    tools=[simulate_outreach],
    llm=llm,
    verbose=True
)