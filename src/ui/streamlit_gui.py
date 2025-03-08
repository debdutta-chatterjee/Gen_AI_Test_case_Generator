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

            if st.button("Generate test cases", key="generate_test_case"):
                st.info("Generate test cases is still work in progress!")

            df = pd.DataFrame(
            np.random.rand(5, 5), 
            columns=['Column1', 'Column2', 'Column3', 'Column4', 'Column5']
            )
            # Display the DataFrame
            st.write("Here's a preview of your data:")
            st.dataframe(df, width=800, height=200)

            if st.button("Upload to Azure", key="upload_button"):
                st.info("Upload functionality is still work in progress!")

        except Exception as e:
            st.write(f"Exception occurred {e}")
