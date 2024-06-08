import streamlit as st
from utils.chatInterface import message_func
from streamlit_navigation_bar import st_navbar
from streamlit_float import *
from components.attach_doc import attach_doc_component
import base64
from io import BytesIO
from pypdf import PdfReader
from adapters.BedrockClaudeAdapter import BedrockClaudeAdapter
from managers.MessageHandler import MessageHandler
import asyncio

chat_API = ""  # api goes here

msg_handler = MessageHandler()
llm_adapter = BedrockClaudeAdapter()


if "disabled" not in st.session_state:
    st.session_state["disabled"] = False

def disable():
    st.session_state["disabled"] = True


def app():
    pages = ["CGIAR"]

    logo_path = "./static/CustomerLogo.svg"
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
        st.session_state.messages = [
            {
                'role': 'user', 
                'content': [{
                    'type': 'text', 
                    'text': "Hi"
                }]
            }, 
            {
                'role': 'assistant', 
                'content': [{
                    'type': 'text', 
                    'text': "<Response> Hello! I'm your CIP assistant, here to support you with your important potato germplasm needs. Please share your specific requirements, and I'll handle the rest. </Response>"
                 }]
            }
        ]

    # Display chat messages from history on app rerun
    for idx, message in enumerate(st.session_state.messages):
        if ((message['role'] == "user") and idx != 0):
            content_val = message['content'][0]['text']
            message_func(
                text=content_val,
                is_user=True
            )
        elif ((message['role'] == "assistant")):
            content_val = msg_handler.parse_bot_response(message['content'][0]['text'])
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

            print("Result: ", result)

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
            prompt = st.chat_input("Type your query here...", disabled=st.session_state.disabled, on_submit=disable)
            print(prompt)
            button_b_pos = "1rem"
            button_css = float_css_helper(
                width="3rem", bottom=button_b_pos, transition=0)
            float_parent(css=button_css)

    if prompt:
        # adding to session chat history
        st.session_state.messages = msg_handler.humanChatFormat(prompt, st.session_state.messages)

        # Displaying message
        message_func(
            text=prompt,
            is_user=True
        )

        try:
            async def main():
                llm_payload = llm_adapter.get_llm_body(st.session_state.messages)
                llm_response =await llm_adapter.fetch_with_loader(llm_payload)
                st.session_state.messages = msg_handler.AIchatFormat(llm_response, st.session_state.messages)
                friendly_msg=msg_handler.parse_bot_response(llm_response)

                message_func(
                    text=friendly_msg,
                    is_user=False
                )
            asyncio.run(main())

        except Exception as e:
            print(str(e))
            string_response="I'm having some issues currently."
            st.session_state.messages = msg_handler.AIchatFormat(string_response, st.session_state.messages)
            message_func(
                text=string_response,
                is_user=False
            )
        st.session_state["disabled"] = False
        st.rerun()

if __name__ == '__main__':
    app()