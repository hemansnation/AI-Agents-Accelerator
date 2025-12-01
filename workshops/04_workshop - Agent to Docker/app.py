from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import agent_response

app = FastAPI()

class Query(BaseModel):
    user_input: str

@app.post("/query")
async def handle_query(query: Query):
    try:
        reply = agent_response(query.user_input)
        return {"response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
