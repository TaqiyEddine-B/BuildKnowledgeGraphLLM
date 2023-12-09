import json
import os

import streamlit as st
from dotenv import load_dotenv
from graphdatascience import GraphDataScience
from langchain.chains.llm import LLMChain
from langchain.chains.openai_functions import (
    create_openai_fn_chain,
    create_structured_output_chain,
)
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from streamlit_agraph import Config, Edge, Node, agraph

from src.extractor import extract

article_text = '''
Albert Einstein was a theoretical physicist who was born on March 14, 1879, in Ulm, Germany. He is best known for his theory of relativity, including the famous equation E=mc². Einstein made groundbreaking contributions to the field of physics, and in 1921, he was awarded the Nobel Prize in Physics for his explanation of the photoelectric effect. He worked at various universities and institutions throughout his career, including the University of Zurich and the Institute for Advanced Study in Princeton, New Jersey. Einstein's work revolutionized our understanding of the universe and had a profound impact on the development of modern physics.
'''
st.write(article_text)
openai_key = st.sidebar.text_input('OpenAI Key', '')

def format_output(output):
    nodes = []
    edges = []
    # https://github.com/ChrisDelClea/streamlit-agraph/blob/master/streamlit_agraph/node.py
    for node in output["nodes"]:
        nodes.append(Node(id=node["id"], label=node["label"],
                     size=25, shape="diamond"))

    for edge in output["edges"]:
        edges.append(
            Edge(source=edge["source"], label=edge["relation"], target=edge["target"]))

    return nodes, edges


@st.cache_data
def run(article_text:str):

    if os.path.exists('output.json'):
        with open('output.json', 'r') as f:
            output = json.load(f)
    else:
        output = extract(article_text=article_text)
        with open('output.json', 'w') as f:
            json.dump(output, f)
    return output


if st.button('Run'):

    if len(openai_key) > 0:
        os.environ["OPENAI_API_KEY"] = openai_key
    else:
        if 'OPENAI_API_KEY' not in os.environ:
            st.error('No OpenAI Key')
            st.stop()
        else :
            st.toast('Using OpenAI Key from .env')

    output = run(article_text=article_text)

    nodes, edges = format_output(output)

    config = Config(width=950,
                    height=950,
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    # **kwargs
                    )

    return_value = agraph(nodes=nodes,
                          edges=edges,
                          config=config)
