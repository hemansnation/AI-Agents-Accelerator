import pytest
from app.agent import process_query

def test_process_query():
    response = process_query("What is your skills alex have?")
    assert len(response) > 0

