import streamlit as st
from crewai import Crew, Task
from agents.data_agent import data_agent
from agents.scoring_agent import scoring_agent
from agents.planning_agent import planning_agent
from agents.engagement_agent import engagement_agent
from models.lead_scoring_model import train_model
import os
from dotenv import load_dotenv

load_dotenv()

st.title("Sales Qualification Agent")
st.write("Enter a lead query (example - Qualify lead with ID 1, company_size: medium, industry: tech, email_opens: 5, website_visits: 10)")

if 'trained' not in st.session_state:
    accuracy = train_model()
    st.session_state.trained = True
    st.write(f"Model trained with accuracy: {accuracy:.2f}")

query = st.text_input("Lead Query")

if st.button("Process") and query:
    st.write("Agent Processing query...")

    plan_task = Task(
        description=f"Plan the qualification for: {query}",
        agent=planning_agent,
    )
    data_task = Task(
        description=f"Gather and enrich lead data",
        agent=data_agent,
    )
    score_task = Task(
        description=f"Score the lead",
        agent=scoring_agent,
    )
    engage_task = Task(
        description=f"Engage if qualified",
        agent=engagement_agent,
    )

    crew = Crew(
        agents=[planning_agent, data_agent, scoring_agent, engagement_agent],
        tasks=[plan_task, data_task, score_task, engage_task],
        verbose=2
    )

    with st.spinner("Running agents..."):
        result = crew.kickoff()
    
    st.write("Final Result:")
    st.write(result)