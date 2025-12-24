from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2,
)

router_prompt = PromptTemplate(
    input_variables=["query"],
    template="Classify the query into: FAQ, Technical, Billing, or Unknown. Query: {query}. Category: ",
)

def route_query(query):
    chain = router_prompt | llm
    response = chain.invoke({"query": query})
    category = response.content.strip()
    confidence = 0.9 if category in ["FAQ", "Technical", "Billing"] else 0.5
    return category, confidence

