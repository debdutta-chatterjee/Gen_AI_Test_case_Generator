from src.ui.streamlit_gui import StreamlitUi
import streamlit as st
import os
import dotenv
import pandas as pd
import numpy as np
from src.llm.groq_llm import ChatGroq
from src.graph.graph_builder import GraphBuilder
from src.node.node import Node
from src.state.state import AgentState
import traceback

from src.azure.azure import AzureConnection
# ui = StreamlitUi()
# ui.loadui()

try:

    st.set_page_config(page_title="self.page_title")
    st.title(os.environ["PAGE_HEADER"])
    st.subheader(os.environ["PAGE_SUBHEADER"])

    # Define the input fields
    ado_url = st.sidebar.text_input("Provide ADO url")
    pat = st.sidebar.text_input("Provide ADO token", type="password")
    ado_us_id = st.sidebar.text_input("Provide User story id")
    api_key = st.sidebar.text_input("Provide API key", type="password")
    st.session_state.requirement_text=""
    #requirement = st.text_area("Requirement from ADO:",key="Requirement from ADO")

    # Create a button to submit the form
    if st.sidebar.button("Get ADO requirement"):
        # Read and print the values of the input fields
            if ado_url and pat and ado_us_id and api_key:
                ado = AzureConnection()
                us = ado.get_user_story_details(ado_url,pat,ado_us_id)
                st.session_state.us_details= us
                st.session_state.requirement_text = f"Title: {us.title} \n\n Description:{us.business_context} \n\n Acceptance criteria:{us.acceptance_critera}"            

                requirement = st.session_state.requirement_text
                st.text_area("Requirement from ADO:", value =st.session_state.requirement_text,key="Requirement from ADO")
            else:
                st.sidebar.warning("Please fill out all the fields to proceed.")
    if st.button("Generate test cases"):
        print("************")
        #llm
        model = ChatGroq(groq_api_key=api_key,model_name="qwen-2.5-32b")

        #graph
        node = Node(model)
        builder = GraphBuilder(node)
        graph = builder.build_test_case_graph()
        flow = graph.compile()

        #invoke graph
        initial_state = {
            "user_story": st.session_state.us_details,
            "user_feedback": ""
        }
        flow.invoke(initial_state)
        st.session_state.response_state = AgentState(**dict(flow.invoke(initial_state)))
        df = st.session_state.response_state["final_data"]
        df_reset = df.reset_index(drop=True)
    
        # Display the DataFrame
        st.write("Here's the AI generated test cases:")
        st.data_editor(df_reset.to_dict(orient='records'), width=800, height=200)
                
            
except Exception as e:
    st.write(f"Exception occurred {e} {traceback.print_exc()}")

