import streamlit as st
import os
import dotenv
import pandas as pd
import numpy as np
from src.llm.groq_llm import ChatGroq
from src.graph.graph_builder import GraphBuilder
from src.node.node import Node
from src.state.state import AgentState

from src.azure.azure import AzureConnection

dotenv.load_dotenv()
page_title = os.environ["PAGE_HEADER"]
page_header = os.environ["PAGE_SUBHEADER"]

st.set_page_config(page_title=page_title)
st.title(page_title)
st.subheader(page_header)

ado_url=st.sidebar.text_input("Provide ADO url")
pat=st.sidebar.text_input("Provide ADO token",type="password")
ado_us_id=st.sidebar.text_input("Provide User story id")
api_key=st.sidebar.text_input("Provide API key",type="password")

if 'requirements_text' not in st.session_state:
    st.session_state.requirements_text = ""
if 'user_feedback' not in st.session_state:
    st.session_state.user_feedback = ""
if 'response_state' not in st.session_state:
    st.session_state.response_state = None
if 'final_test_cases' not in st.session_state:
    st.session_state.final_test_cases = None    

requirement = st.text_area("Requirement from ADO:", value=st.session_state.requirements_text,key="Requirement from ADO")
btn_generate_test = st.button("Generate test cases", key="generate_test_case")
feedback = st.text_area("Feedback:",key="Feedback")
btn_submit_feedback = st.button("Submit feedback", key="Submit feedback")
btn_get_us = st.sidebar.button("Get ADO requirement")

if 'model' not in st.session_state:
    st.session_state.model = None
    st.session_state.node = None
    st.session_state.builder = None
    st.session_state.graph = None
    st.session_state.flow = None


if btn_get_us:
        # Read and print the values of the input fields
    if ado_url and pat and ado_us_id and api_key:
        ado = AzureConnection()
        us = ado.get_user_story_details(ado_url,pat,ado_us_id)
        st.session_state.us_details= us
        st.session_state.requirements_text = f"Title: {us.title} \n\n Description:{us.business_context} \n\n Acceptance criteria:{us.acceptance_critera}"            
    else:
        st.sidebar.warning("Please fill out all the fields to proceed.")

if btn_generate_test:
    # Read and print the values of the input fields
    if requirement and api_key:

        #llm
        st.session_state.model = ChatGroq(groq_api_key=api_key,model_name="qwen-2.5-32b")
        #graph
        st.session_state.node = Node(st.session_state.model)
        st.session_state.builder = GraphBuilder(st.session_state.node)
        st.session_state.graph = st.session_state.builder.build_test_case_graph()
        st.session_state.flow = st.session_state.graph.compile()

        #invoke graph
        initial_state = {
            "user_story": st.session_state.us_details,
            "user_feedback": ""
        }
        #flow.invoke(initial_state)
        st.session_state.response_state = AgentState(**dict(st.session_state.flow.invoke(initial_state)))
        df = st.session_state.response_state["final_data"]
        df_reset = df.reset_index(drop=True)
        st.session_state.final_test_cases = df_reset        
        st.write("Here's the AI generated test cases:")
        st.data_editor(df_reset.to_dict(orient='records'), width=800, height=200)
    else:
        st.warning("Please fill out the user story details & api key.")

if btn_submit_feedback:    
    if feedback and api_key:
        #st.info(st.session_state.response_state.user_feedback)

        initial_state = {
            "user_story": st.session_state.us_details,
            "user_feedback": feedback
        }

        st.session_state.response_state.user_feedback = feedback
        st.session_state.response_state = AgentState(**dict(st.session_state.flow.invoke(st.session_state.response_state)))
        df = st.session_state.response_state["final_data"]
        df_reset = df.reset_index(drop=True)
        st.session_state.final_test_cases = df_reset        
        st.write("Here's the modified AI generated test cases:")
        st.data_editor(df_reset.to_dict(orient='records'), width=800, height=200)
    else:
        st.warning("Please fill out the feedback & api key.")

