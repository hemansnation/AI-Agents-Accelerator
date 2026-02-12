from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

planning_agent = Agent(
    role='Planner',
    goal='Create step-by-step plans for lead qualification',
    backstory='Orchestrates multi-agent workflows',
    llm=llm,
    verbose=True
)