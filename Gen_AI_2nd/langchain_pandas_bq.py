import numpy as np
import pandas as pd
from langchain.llms import OpenAI
from langchain.llms import VertexAI
from langchain.agents import create_pandas_dataframe_agent
import os
import yaml
import streamlit as st
import time
import base64
from google.cloud import bigquery


st.markdown(

 f"""

 <style>

 .stApp {{

 background-image: url("https://cdn.pixabay.com/photo/2019/04/24/11/27/flowers-4151900_960_720.jpg");

 background-attachment: fixed;

 background-size: cover

 }}

 </style>

 """,

 unsafe_allow_html=True

 )
# use standard pandas approach to answer the questions


# define LLM objects

def agent_out(table, databasename):
    client = bigquery.Client()

    sql = f"""
        SELECT *
        FROM `sadaindia-tvm-poc-de.{databasename}.{table}`
    
    """

    df = client.query(sql).to_dataframe()
    llm = VertexAI()
    agent = create_pandas_dataframe_agent(llm, df, verbose=True)
    return agent

# use LLM to answer the questions

# print("what is value of FEB year 2001")
# print(agent.run("what is value of FEB year 2001"))
#
# print(agent.run("How much percentage increased of temperature value from 1901 to 2017 for Jan"))
st.title("Ask The Database !!")

database_name = st.text_input('Type your database name here')
table_name = st.text_input('Type your table name here')
st.subheader("Type your question here ")
question = st.text_input('Type our question here',label_visibility = "hidden")
if question:
    print("in title")
    agent = agent_out(table_name.strip(), database_name.strip())
    data = agent.run(question)
    st.write(data)