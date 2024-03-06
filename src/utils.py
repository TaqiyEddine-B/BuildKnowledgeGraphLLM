""" Utils for the Streamlit app."""
import os

import streamlit as st

def load_openai_key()->str:
    """ Load the OpenAI key from the environment variable or from the user input."""
    key =""
    env_var = os.getenv('OPENAI_API_KEY')
    if env_var is not None:
        st.sidebar.success('Using OpenAI Key from .env')
        key = env_var
    else:
        key = st.sidebar.text_input('Enter your OpenAI API key', type="password")
        if len(key) > 0:
            os.environ["OPENAI_API_KEY"] = key
            st.sidebar.success('Using the provided OpenAI Key')
        else:
            st.error('No OpenAI Key')
            st.stop()
    return key
