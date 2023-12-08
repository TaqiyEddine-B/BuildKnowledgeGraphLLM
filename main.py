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

load_dotenv()


openai_key = st.sidebar.text_input('OpenAI Key', '')


system_message_entity_prompt = """
You are a data scientist working for a company that is building a knowledge graph of a set of input articles.
You are a world class algorithm for extracting information in structured formats.
The desired output format is json  with two keys "nodes" a list of nodes and "edges" a list of edges
"""
prompt_template_entity = ChatPromptTemplate.from_messages([
    ("system",
     system_message_entity_prompt),
    ("human", "{user_input}"),])

article_text = '''
Albert Einstein was a theoretical physicist who was born on March 14, 1879, in Ulm, Germany. He is best known for his theory of relativity, including the famous equation E=mc². Einstein made groundbreaking contributions to the field of physics, and in 1921, he was awarded the Nobel Prize in Physics for his explanation of the photoelectric effect. He worked at various universities and institutions throughout his career, including the University of Zurich and the Institute for Advanced Study in Princeton, New Jersey. Einstein's work revolutionized our understanding of the universe and had a profound impact on the development of modern physics.
'''

st.write(article_text)
json_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "nodes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "label": {"type": "string"},
                    "type": {"type": "string"}
                },
                "required": ["id", "label", "type"]
            }
        },
        "edges": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source": {"type": "string"},
                    "target": {"type": "string"},
                    "relation": {"type": "string"}
                },
                "required": ["source", "target", "relation"]
            }
        }
    },
    "required": ["nodes", "edges"]
}

# llm_chain = LLMChain(llm=llm, prompt=prompt_template_entity, verbose=True)



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
def run(article_text):

    if os.path.exists('output.json'):
        with open('output.json', 'r') as f:
            output = json.load(f)
    else:
        llm = ChatOpenAI(temperature=0, model="gpt-4")
        llm_chain = create_structured_output_chain(json_schema, llm, prompt_template_entity, verbose=True)
        output = llm_chain.run(user_input=article_text)
        with open('output.json', 'w') as f:
            json.dump(output, f)
    return output


if st.button('Run'):
    if len(openai_key) > 0:
        st.write('Setting OpenAI Key')
        os.environ["OPENAI_API_KEY"] = openai_key
    else:
        st.write('Checking OpenAI Key from .env')
        if 'OPENAI_API_KEY' not in os.environ:
            st.write('No OpenAI Key')
            st.stop()
        else :
            st.write('Using OpenAI Key from .env')

    output = run(article_text)

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
