from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.api_utils import enrich_data
import os

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

data_agent = Agent(
    role='Data Gatherer',
    goal='Collect and enrich lead data from sources',
    backstory='Expert in data aggregation and API calls',
    tools=[enrich_data],
    llm=llm,
    verbose=True
)