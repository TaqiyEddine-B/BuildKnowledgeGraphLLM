""" Streamlit app for extracting relations from text using OpenAI's API """
import json
import os

import streamlit as st
from streamlit_agraph import Config, Edge, Node, agraph

from src.extractor import extract

st.set_page_config(
    page_title="Knowledge Graph Generator using LLM",
    page_icon="🧠",
    layout="wide",
)
st.title('Knowledge Graph Generator using LLM')

article_text = '''
Albert Einstein was a theoretical physicist who was born on March 14, 1879, in Ulm, Germany. He is best known for his theory of relativity, including the famous equation E=mc². Einstein made groundbreaking contributions to the field of physics, and in 1921, he was awarded the Nobel Prize in Physics for his explanation of the photoelectric effect. He worked at various universities and institutions throughout his career, including the University of Zurich and the Institute for Advanced Study in Princeton, New Jersey. Einstein's work revolutionized our understanding of the universe and had a profound impact on the development of modern physics.
'''


openai_key = st.sidebar.text_input('OpenAI Key', '')
use_cache = st.sidebar.checkbox('Use Cache', value=True)


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


def run(article_text: str, use_cache: bool = False):
    if use_cache and os.path.exists('output.json'):
        with open('output.json', 'r') as f:
            output = json.load(f)
    else:
        output = extract(article_text=article_text)
    with open('output.json', 'w') as f:
        json.dump(output, f)
    return output


nodes, edges, config = None, None, None

col_input, col_result = st.columns([1, 1])
with col_input:
    st.title('Input')
    st.subheader('Article Text', divider="blue")
    article_text = st.text_area('Article Text', article_text, height=200)

    if st.button('Generate Knowledge Graph', type='primary'):

        if len(openai_key) > 0:
            os.environ["OPENAI_API_KEY"] = openai_key
        else:
            if 'OPENAI_API_KEY' not in os.environ:
                st.error('No OpenAI Key')
                st.stop()
            else:
                st.toast('Using OpenAI Key from .env')

        output = run(article_text=article_text, use_cache=use_cache)

        nodes, edges = format_output(output)

        config = Config(width=950,
                        height=950,
                        directed=True,
                        physics=True,
                        hierarchical=False,
                        # **kwargs
                        )


with col_result:
    st.title('Result')
    st.subheader('Knowledge Graph', divider="green")

    if nodes is not None and edges is not None:
        return_value = agraph(nodes=nodes,
                              edges=edges,
                              config=config)
