from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from tools import fetch_stock_data, analyze_financials, integrate_data
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

os.environ["GOOGLE_API_KEY"] = api_key

try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
except Exception as e:
    raise ValueError(f"Failed to initialize Google Generative AI: {str(e)}")

tools = [fetch_stock_data, analyze_financials, integrate_data]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a financial analysis agent. Use tools to fetch and analyze data. Reason step by step using Chain-Of-Thought."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True
)