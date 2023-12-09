""" This module contains the extractor function that is used to extract information from a given article. """
from dotenv import load_dotenv

from langchain.chains.openai_functions import (
    create_structured_output_chain,
)
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate

load_dotenv()

system_message_entity_prompt = """
You are a data scientist working for a company that is building a knowledge graph of a set of input articles.
You are a world class algorithm for extracting information in structured formats.
The desired output format is json  with two keys "nodes" a list of nodes and "edges" a list of edges
"""
prompt_template_entity = ChatPromptTemplate.from_messages([
    ("system",
     system_message_entity_prompt),
    ("human", "{user_input}"),])


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


def extract(article_text):
    llm = ChatOpenAI(temperature=0, model="gpt-4")
    llm_chain = create_structured_output_chain(json_schema, llm, prompt_template_entity, verbose=True)
    output = llm_chain.run(user_input=article_text)
    return output
