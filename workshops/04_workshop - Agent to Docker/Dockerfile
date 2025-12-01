FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV GEMINI_API_KEY=your_api_key_here

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
