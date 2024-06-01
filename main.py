import streamlit as st
import requests as request
import json
from utils.chatInterface import message_func
import streamlit.components.v1 as components
from streamlit_navigation_bar import st_navbar
from streamlit_float import *
from components.attach_doc import attach_doc_component
import base64
from io import BytesIO
from pypdf import PdfReader
from adapters.BedrockClaudeAdapter import BedrockClaudeAdapter
import re

chat_API = ""  # api goes here


llm_adapter = BedrockClaudeAdapter()

def app():

    pages = ["CGIAR"]

    logo_path = "./static/CustomerLogo.svg"
    # generate 10000 words essay on genai

    urls = {"CGIAR": "https://www.cgiar.org/"}

    styles = {
        "nav": {
            "background-color": "#FDF0E1",
            "justify-content": "space-between",
            "height": "5rem",
            "max-width": "100%",
            "width": "100%",
            "padding": "0rem",
        },
        "div": {
            "max-width": "100%",
        },
        "img": {
            "padding-right": "14px",
            "height": "4rem"
        },
        "span": {
            "color": "transparent",
            "pointer-events": "none !important",
        },
    }
    options = {"show_sidebar": True,  "show_menu": True}

    page = st_navbar(
        pages,
        logo_path=logo_path,
        urls=urls,
        styles=styles,
        options=options,
    )

    gradient_text_html = """
    <div class="gradient-text">CIP Potato Chat Assistant</div>
    """

    st.markdown(gradient_text_html, unsafe_allow_html=True)

    with open("sidebar.md", "r") as sidebar_file:
        sidebar_content = sidebar_file.read()

    with open("styles.md", "r") as styles_file:
        styles_content = styles_file.read()
    st.write(styles_content, unsafe_allow_html=True)

    st.sidebar.markdown(sidebar_content)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if ((message['role'] == "user")):
            content_val = message['content'][0]['text']
            message_func(
                text=content_val,
                is_user=True
            )
        elif ((message['role'] == "assistant")):
            content_val = message['content'][0]['text']
            message_func(
                text=content_val,
                is_user=False
            )

    # Create two columns
    col1, col2 = st.columns([0.34, 4])

    # Render the div in the first column
    with col1:
        with st.container():
            result = attach_doc_component()

            button_b = "0rem"
            button_css_upload = float_css_helper(
                width="38px", height="38px", bottom=button_b, transition=0)
            float_parent(css=button_css_upload)
            if result is not None:
                fileName, value = result.split(".pdf")
                fileName = fileName+".pdf"
                value = value.strip()
                print(fileName)
                # Decode base64 string to bytes
                pdf_bytes = base64.b64decode(value)
                # st.session_state.messages = humanChatFormat("The file  Amazon.pdf is upload succesfully", st.session_state.messages)

                # st.session_state.messages = AIchatFormat("Please ask furter question on Amazon.pdf", st.session_state.messages)
                # Create a PDF file object
                pdf_data = BytesIO(pdf_bytes)
                pdf_reader = PdfReader(pdf_data)
                text_data = ""
                for page in pdf_reader.pages:
                    text_data += page.extract_text()

                # Print the extracted text data
                print(text_data)
            else:
                print("No data")

    # Render the chat input in the second column
    with col2:
        prompt = ""
        # Display a text box for input at the bottom
        with st.container():
            prompt = st.chat_input("Type your query here...")
            print(prompt)
            button_b_pos = "1rem"
            button_css = float_css_helper(
                width="3rem", bottom=button_b_pos, transition=0)
            float_parent(css=button_css)

    if prompt:
        # adding to session chat history
        st.session_state.messages = humanChatFormat(
            prompt, st.session_state.messages)

        # Displaying message
        message_func(
            text=prompt,
            is_user=True
        )

        try:
            llm_payload = llm_adapter.get_llm_body(st.session_state.messages)
            llm_response = llm_adapter.generate_response(llm_payload)
            print(llm_response)
            st.session_state.messages = AIchatFormat(
                llm_response, st.session_state.messages)

            friendly_msg=parse_bot_response(llm_response)
            message_func(
                text=friendly_msg,
                is_user=False
            )
        except Exception as e:
            print(str(e))
            string_response="I'm having some issues currently."
            st.session_state.messages = AIchatFormat(
                string_response, st.session_state.messages)
            message_func(
                text=string_response,
                is_user=False
            )

def parse_bot_response(response):
    response_pattern = r'<Response>(.*?)</Response>'
    match = re.search(response_pattern, response, re.DOTALL)

    if match:
        response_text = match.group(1)
        return response_text
    else: #edge case issue with parsing
        return "I'm having some issues currently"
        
def humanChatFormat(prompt, messageHistory):

    human_chat_element = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt
            }]
    }

    messageHistory.append(human_chat_element)

    return messageHistory


def AIchatFormat(response, messageHistory):

    response_val = response

    AI_chat_element = {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": response_val
            }]
    }

    messageHistory.append(AI_chat_element)
    return messageHistory


if __name__ == '__main__':
    app()
