import streamlit as st
from agent import agent_executor

query = st.text_input("Enter your investment research query (eg - Analyze AAPL stock) :")

if st.button("Run Analysis"):
    if query:
        with st.spinner("Agent is working..."):
            result = agent_executor.invoke({"input": query})
            st.write("### Agent Thoughts and Actions (Verbose Log):")
            intermediate_steps = result.get("intermediate_steps", [])
            if intermediate_steps:
                for step in intermediate_steps:
                    st.text(str(step))
            else:
                st.text("No steps logged.")
            st.write("### Final Report:")
            st.write(result["output"])
    else:
        st.warning("Please enter a valid query.")