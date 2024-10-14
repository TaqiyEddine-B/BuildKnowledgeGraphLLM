""" Utils for the Streamlit app."""
import os

import streamlit as st
import streamlit as st
from streamlit_agraph import Config, Edge, Node, agraph
from pyvis.network import Network
import streamlit.components.v1 as components


def load_openai_key() -> str:
    """
    Load the OpenAI API key from the environment variable or user input.

    This function checks for the OpenAI API key in the following order:
    1. Streamlit secrets (secrets.toml file)
    2. User input via Streamlit sidebar

    Returns:
        tuple[str, bool]: A tuple containing:
            - str: The OpenAI API key
            - bool: A flag indicating whether a valid key was provided
    """
    key = ""
    is_key_provided = False
    secrets_file = os.path.join(".streamlit", "secrets.toml")
    if os.path.exists(secrets_file) and "OPENAI_API_KEY" in st.secrets.keys():
        key = st.secrets["OPENAI_API_KEY"]
        st.sidebar.success('Using OpenAI Key from sectrets.toml')
        is_key_provided = True
    else:
        key = st.sidebar.text_input(
            'Add OpenAI API key and press \'Enter \'', type="password")
        if len(key) > 0:
            st.sidebar.success('Using the provided OpenAI Key')
            is_key_provided = True
        else:
            st.sidebar.error('No OpenAI Key')
    return key, is_key_provided


def format_output_agraph(output):
    nodes = []
    edges = []
    for node in output["nodes"]:
        nodes.append(
            Node(id=node["id"], label=node["label"], size=8, shape="diamond"))
    for edge in output["edges"]:
        edges.append(Edge(source=edge["source"], label=edge["relation"],
                     target=edge["target"], color="#4CAF50", arrows="to"))
    return nodes, edges


def display_agraph(nodes, edges):
    config = Config(width=950,
                    height=950,
                    directed=True,
                    physics=True,
                    hierarchical=True,
                    nodeHighlightBehavior=False,
                    highlightColor="#F7A7A6",  # or "blue"
                    collapsible=False,
                    node={'labelProperty': 'label'},
                    )

    return agraph(nodes=nodes, edges=edges, config=config)


def format_output_pyvis(output):
    net = Network(height="800px", width="800px", bgcolor="#FFFFFF", font_color="#333333")
    net.set_edge_smooth('dynamic')
    
    for node in output["nodes"]:
        net.add_node(node["id"], 
                label=node["label"], 
                title=node["label"],
                     size=5,
                     color="#FF4B4B",
                     font={'size': 14, 'color': '#262730', 'face': 'sans-serif'},
                     shape='dot')
    
    for edge in output["edges"]:
        net.add_edge(edge["source"], edge["target"], 
                     label=edge["relation"], 
                     title=edge["relation"],
                                          width=1,
                     color="#0068C9",
                     font={'size': 11, 'color': '#262730', 'face': 'sans-serif'},
                     arrows='to')
    
    net.toggle_physics(True)
    net.show_buttons(filter_=['physics'])
    return net


def display_pyvis(net):
    net.save_graph("graph.html")
    with open("graph.html", 'r', encoding='utf-8') as f:
        source_code = f.read()
    components.html(source_code, height=800)
