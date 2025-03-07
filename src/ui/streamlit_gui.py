import streamlit as st
import os
import dotenv
import pandas as pd
import numpy as np

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

            mysql_host=st.sidebar.text_input("Provide ADO url")
            mysql_host=st.sidebar.text_input("Provide ADO token",type="password")
            mysql_host=st.sidebar.text_input("Provide API key",type="password")

            if st.sidebar.button("Get ADO requirement"):
                pass
            st.text_area("Requirement from ADO:", key="Requirement from ADO")
            st.text_area("Precondition:", key="Precondition")


            df = pd.DataFrame(
            np.random.rand(5, 5), 
            columns=['Column1', 'Column2', 'Column3', 'Column4', 'Column5']
            )
            # Display the DataFrame
            st.write("Here's a preview of your data:")
            st.dataframe(df, width=800, height=200)

            if st.button("Upload to Azure", key="upload_button"):
                st.info("Upload functionality is still work in progress!")

            # Style the button
            st.markdown(
                """
                <style>
                div.stButton > button[key="upload_button"] {
                    background-color: #4CAF50;
                    color: white;
                    padding: 15px 32px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                    border-radius: 12px;
                    transition-duration: 0.4s;
                }
                div.stButton > button:hover {
                    background-color: white;
                    color: black;
                    border: 2px solid #4CAF50;
                }
                </style>                
                """, unsafe_allow_html=True
            )
        except Exception as e:
            st.write(f"Exception occurred {e}")
