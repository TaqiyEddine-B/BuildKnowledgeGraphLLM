""" Streamlit app for extracting relations from text using OpenAI's API """
import json
import os
import streamlit as st
from src.extractor import extract
from src.utils import load_openai_key,format_output_pyvis,display_pyvis

st.set_page_config(
    page_title="Knowledge Graph Generator using LLM",
    page_icon="🧠",
    layout="wide",
)


st.title('Knowledge Graph Generator using LLM')
st.write('This app generates a knowledge graph from the input text.')

article_text = '''
Albert Einstein was a theoretical physicist who was born on March 14, 1879, in Ulm, Germany. He is best known for his theory of relativity, including the famous equation E=mc². Einstein made groundbreaking contributions to the field of physics, and in 1921, he was awarded the Nobel Prize in Physics for his explanation of the photoelectric effect. He worked at various universities and institutions throughout his career, including the University of Zurich and the Institute for Advanced Study in Princeton, New Jersey. Einstein's work revolutionized our understanding of the universe and had a profound impact on the development of modern physics.
'''


st.sidebar.subheader('Steps')
st.sidebar.write("1. Add the OpenAI API key and press 'Enter'")
st.sidebar.write("2. Enter the article text")
st.sidebar.write("3. Click 'Generate Knowledge Graph'")

st.sidebar.divider()
openai_key, is_key_provided = load_openai_key()

# use_cache = st.sidebar.checkbox('Use Cache', value=True)
use_cache = False


st.sidebar.divider()

st.sidebar.subheader('About')
st.sidebar.link_button("GitHub Repository",
                       "https://github.com/TaqiyEddine-B/BuildKnowledgeGraphLLM")
st.sidebar.link_button("My website", "https://taqiyeddine.com")


def run(article_text: str, use_cache: bool = False):
    if use_cache and os.path.exists('output.json'):
        with open('output.json', 'r') as f:
            output = json.load(f)
    else:
        output = extract(article_text=article_text,openai_key=openai_key)
    with open('output.json', 'w') as f:
        json.dump(output, f)
    return output

col_input, col_result = st.columns([1, 1])
with col_input:
    st.subheader('Article Text', divider="blue")
    article_text = st.text_area('Article Text', article_text, height=400)


with col_result:
    st.subheader('Knowledge Graph', divider="green")
    if st.button('Generate Knowledge Graph', type='primary'):
        output = run(article_text=article_text, use_cache=use_cache)
        net = format_output_pyvis(output)
        display_pyvis(net)
