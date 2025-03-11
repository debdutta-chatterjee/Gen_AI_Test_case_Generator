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

class StreamlitUi:

    def __init__(self):
        dotenv.load_dotenv()
        self.page_title = os.environ["PAGE_HEADER"]
        self.page_header = os.environ["PAGE_SUBHEADER"]
    def loadui(self):
        try:
            st.set_page_config(page_title="self.page_title")
            st.title(self.page_title)
            st.subheader(self.page_header)
            
            st.session_state.requirement_text =""
            st.session_state.setdefault("response_state", None)
            st.session_state.setdefault("user_feedback", "")
            
            ado_url=st.sidebar.text_input("Provide ADO url")
            pat=st.sidebar.text_input("Provide ADO token",type="password")
            ado_us_id=st.sidebar.text_input("Provide User story id")
            api_key=st.sidebar.text_input("Provide API key",type="password")

            if st.sidebar.button("Get ADO requirement"):
                
                if not (len(ado_url)>0 & len(pat)>0 & len(ado_us_id)>0):
                    st.warning("Please enter valid details")
                else:
                    ado = AzureConnection()
                    us = ado.get_user_story_details(ado_url,pat,ado_us_id)
                    st.session_state.us_details= us
                    st.session_state.requirement_text = f"Title: {us.title} description:{us.business_context} acceptance criteria:{us.acceptance_critera}"            
                
                    st.text_area("Requirement from ADO:", value =st.session_state.requirement_text,key="Requirement from ADO")
                
                    if st.button("Generate test cases", key="generate_test_case"):
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
                        #st.dataframe(df_reset.to_dict(orient='records'), width=800, height=200)
                        #st.dataframe(editable_df, width=800, height=200)
                        
                        st.session_state.user_feedback = st.text_area("Feedback:",key="Feedback")
                        if len(st.session_state.user_feedback)>0 & st.button("Modify Test Cases"):
                            st.session_state.response_state.user_feedback = st.session_state.user_feedback
                            st.session_state.response_state = AgentState(**dict(flow.invoke(st.session_state.response_state)))
                            #st.rerun()
                            st.write("Here's the AI generated updated test cases, based on the feedback:")
                            st.data_editor(df_reset.to_dict(orient='records'), width=800, height=200)

            # if st.button("Upload to Azure", key="upload_button"):
            #     st.info("Upload functionality is still work in progress!")

        except Exception as e:
            st.write(f"Exception occurred {e} {traceback.print_exc()}")
