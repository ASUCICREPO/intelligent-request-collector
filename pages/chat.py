import streamlit as st
from streamlit_navigation_bar import st_navbar
from streamlit_float import *
from components.attach_doc import attach_doc_component
from adapters.BedrockClaudeAdapter import BedrockClaudeAdapter
from managers.MessageHandler import MessageHandler
import asyncio
from managers.S3FileHandler import S3Handler

# Initializing S3Handler Class
S3Handler_1 = S3Handler()

chat_API = ""  # api goes here

msg_handler = MessageHandler()
llm_adapter = BedrockClaudeAdapter()


if "disabled" not in st.session_state:
    st.session_state["disabled"] = False

def disable():
    st.session_state["disabled"] = True


def app():
    pages = ["CGIAR"]

    #Initializing the memory to store a list of attached files by the user
    st.session_state.attached_files = []

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

    prompt=st.chat_input("Type your query here...", disabled=st.session_state.disabled, on_submit=disable)
    attachment = st.file_uploader("Attach a file (optional)", type=["jpg", "png", "pdf"], disabled=st.session_state.disabled)
    if attachment is not None:
        print(attachment) 
        
        S3Handler_1.upload_files(file_objects=[attachment])
        st.session_state.attached_files.append(S3Handler_1.uploaded_files[attachment.name])
        st.success("File Upload Success!", icon="✅")

    # Display chat messages from history on app rerun
    with st.container(border=False):
        for idx, message in enumerate(st.session_state.messages):
            if message['role'] == "user" and idx != 0:
                content_val = message['content'][0]['text']
                with st.chat_message("user",avatar='static/UserAvatar.svg'):
                    st.markdown(content_val)
            elif ((message['role'] == "assistant")):
                content_val = msg_handler.parse_bot_response(message['content'][0]['text'])
                with st.chat_message("assistant", avatar='static/ChatbotAvatar.svg'):
                    st.markdown(content_val)

        if prompt:
            # adding to session chat history
            st.session_state.messages = msg_handler.humanChatFormat(prompt, st.session_state.messages)

            # Displaying message
            with st.chat_message("user",avatar='static/UserAvatar.svg'):
                st.markdown(prompt)

            try:
                async def llm_logic():
                    llm_payload = llm_adapter.get_llm_body(st.session_state.messages)
                    llm_response =await llm_adapter.fetch_with_loader(llm_payload)
                    st.session_state.messages = msg_handler.AIchatFormat(llm_response, st.session_state.messages)
                    friendly_msg=msg_handler.parse_bot_response(llm_response)

                    with st.chat_message("assistant",avatar='static/ChatbotAvatar.svg'):
                        st.markdown(friendly_msg)

                asyncio.run(llm_logic())

            except Exception as e:
                print(str(e))
                string_response="I'm having some issues currently."
                st.session_state.messages = msg_handler.AIchatFormat(string_response, st.session_state.messages)
                with st.chat_message("assistant",avatar='static/ChatbotAvatar.svg'):
                    st.markdown(string_response)
            
            st.session_state["disabled"] = False
            st.rerun()
        
if __name__ == '__main__':
    app()