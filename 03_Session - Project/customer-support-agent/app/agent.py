from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from app.rag import get_retriever
from app.router import route_query
from app.handoff import handoff_to_human
import os

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2,
)

response_prompt = PromptTemplate(
    input_variables=["query", "context"],
    template="Answer empathetically based on the context: {context}\n Query: {query}:"
)

def process_query(query):
    category, confidence = route_query(query)

    if confidence < 0.8 or category == "Unknown":
        return handoff_to_human(query)

    retriever = get_retriever()
    docs = retriever.get_relevant_documents(query)
    context = "\n".join([doc.page_content for doc in docs[:3]])

    chain = LLMChain(llm=llm, prompt=response_prompt)
    response = chain.run({"query": query, "context": context})

    if len(response) < 10:
        return handoff_to_human(query, response)

    return response