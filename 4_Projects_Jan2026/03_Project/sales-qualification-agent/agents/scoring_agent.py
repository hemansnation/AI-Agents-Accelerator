from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from models.lead_scoring_model import score_lead
import os

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


scoring_agent = Agent(
    role='Lead Scorer',
    goal='Score leads based on ML model and criteria',
    backstory='uses predictive models for accurate lead scoring',
    tools=[score_lead],
    llm=llm,
    verbose=True
)
