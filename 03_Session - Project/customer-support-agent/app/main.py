from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agent import process_query

app = FastAPI()

class Query(BaseModel):
    text: str

@app.post("/query")
async def handle_query(query: Query):
    try:
        response = process_query(query.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

