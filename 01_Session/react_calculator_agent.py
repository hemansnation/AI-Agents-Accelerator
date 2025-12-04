# installing libraries
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# load api key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")


# define my tool
@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression.
    only allow basic operations: +, -, *, /
    """
    allowed_chars = set("0123456789.+-*/()")
    if not all(c in allowed_chars or c.isspace() for c in expression):
        return "Error: Invalid characters in expression."
    
    try:
        import ast
        tree = ast.parse(expression, mode='eval')
        allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.USub, ast.UAdd)
        if not all(isinstance(node, allowed_nodes) for node in ast.walk(tree)):
            return "Error: Unsafe expression."
        
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as e:
        return f"Error: {str(e)}"

tools = [calculate]


# gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0,
    convert_system_message_to_human=True
)

# react prompt
prompt = hub.pull("hwchase17/react")

# react agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10
)

# run the agent

if __name__ == "__main__":
    print("ReAct agent with gemini 2.5 flash:")

    query = "what is the multiplication of 65 and 85?"

    print("Question:", query)

    result = agent_executor.invoke({
        "input": query
    })

    print("Answer:", result['output'])