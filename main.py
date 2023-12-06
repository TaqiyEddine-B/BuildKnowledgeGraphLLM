import os

from dotenv import load_dotenv
from graphdatascience import GraphDataScience
from langchain.chains.llm import LLMChain
from langchain.chains.openai_functions import (
    create_openai_fn_chain,
    create_structured_output_chain,
)
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import streamlit as st
load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-4")

system_message_entity_prompt = """
You are a data scientist working for a company that is building a knowledge graph of a set of input articles.
You are a world class algorithm for extracting information in structured formats.
The desired output format is json  with two keys "nodes" a list of nodes and "edges" a list of edges
"""
prompt_template_entity = ChatPromptTemplate.from_messages([
                                                           ("system",
                                                            system_message_entity_prompt),
                                                           ("human", "{user_input}"),])

article_text='''
Albert Einstein was a theoretical physicist who was born on March 14, 1879, in Ulm, Germany. He is best known for his theory of relativity, including the famous equation E=mc². Einstein made groundbreaking contributions to the field of physics, and in 1921, he was awarded the Nobel Prize in Physics for his explanation of the photoelectric effect. He worked at various universities and institutions throughout his career, including the University of Zurich and the Institute for Advanced Study in Princeton, New Jersey. Einstein's work revolutionized our understanding of the universe and had a profound impact on the development of modern physics.
'''

st.write(article_text)
json_schema  = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "nodes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "label": { "type": "string" },
          "type": { "type": "string" }
        },
        "required": ["id", "label", "type"]
      }
    },
    "edges": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "source": { "type": "string" },
          "target": { "type": "string" },
          "relation": { "type": "string" }
        },
        "required": ["source", "target", "relation"]
      }
    }
  },
  "required": ["nodes", "edges"]
}

# llm_chain = LLMChain(llm=llm, prompt=prompt_template_entity, verbose=True)
llm_chain= create_structured_output_chain(json_schema, llm, prompt_template_entity, verbose=True)


if st.button('Run'):
  output = llm_chain.run(user_input= article_text)
  st.write(output)
