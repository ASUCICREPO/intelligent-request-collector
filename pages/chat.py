import streamlit as st
from streamlit_navigation_bar import st_navbar
from streamlit_float import *
from components.attach_doc import attach_doc_component
import asyncio
from adapters.BedrockClaudeAdapter import BedrockClaudeAdapter
from managers.MessageHandler import MessageHandler
from managers.S3FileHandler import S3Handler
from managers.EmailHandler import EmailHandler
from dotenv import load_dotenv
import os
import logging

load_dotenv()


# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler('chat.log')
file_handler.setLevel(logging.INFO)

# Create a formatter and add it to the file handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


# Initializing S3Handler Class
bucket_name=os.getenv('BUCKET_NAME') # required
from_email=os.getenv('FROM_EMAIL') # required
region_name=os.getenv('REGION_NAME') or None 
dynamo_table_name=os.getenv('DYNAMO_TABLE_NAME') or None

# prevent direct entry to chat page
if "uuid" not in st.session_state:
    st.switch_page("main.py")
else:
    logger.debug("UUID: %s",st.session_state.uuid)
    S3Handler_ = S3Handler(
        uuid=st.session_state.uuid, 
        bucket_name=bucket_name,
        logger=logger,
        region=region_name,
        dynamo_table_name=dynamo_table_name )



chat_API = ""  # api goes here

msg_handler = MessageHandler(logger=logger)
llm_adapter = BedrockClaudeAdapter()
email_handler = EmailHandler(uuid=st.session_state.uuid, email=st.session_state.email,from_email=from_email)

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

    with open("styles.html", "r") as styles_file:
        styles_content = styles_file.read()

    st.write(styles_content, unsafe_allow_html=True)
    st.sidebar.markdown(sidebar_content)

    # Initialize chat history
    if "messages" not in st.session_state:
        logger.info("Chat session for {%s} started.", st.session_state.uuid)
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
    attachments = st.file_uploader("Attach a file (optional)", type=["jpg", "png", "pdf"], disabled=st.session_state.disabled, accept_multiple_files= True)
    if len(attachments) >= 1:
        logger.debug("%s",attachments) 
        
        S3Handler_.upload_files(file_objects=attachments)
        for attachment in attachments:
            st.session_state.attached_files.append(S3Handler_.uploaded_files[st.session_state.uuid+'/'+attachment.name])
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
                    if "Got everything I need" in friendly_msg:
                        logger.debug(llm_response)
                        stored_table = msg_handler.get_stored_table(llm_response)
                        email_handler.send_email(body=stored_table, files=st.session_state.attached_files)
                        unformatted_msg="<Response> An email with your request has been sent to CIP. If you'd like to start a new request go to http://localhost:8501. </Response>"
                        friendly_msg=msg_handler.parse_bot_response(llm_response)
                        st.session_state.messages.append({
                            'role': 'assistant', 
                            'content': [{
                                'type': 'text', 
                                'text': unformatted_msg
                            }]
                        })

                        st.image('static/HeadsetAvatar.png',width='60')
                        with st.chat_message("assistant",avatar='static/ChatbotAvatar.svg'):
                            st.markdown(friendly_msg)
                        

                        disable()
                        logger.info("Chat session for {%s} concluded.", st.session_state.uuid)
                        st.rerun()
                        
    
                    with st.chat_message("assistant",avatar='static/ChatbotAvatar.svg'):
                        st.markdown(friendly_msg)

                asyncio.run(llm_logic())

            except Exception as e:
                logger.critical(str(e))
                string_response="I'm having some issues currently."
                st.session_state.messages = msg_handler.AIchatFormat(string_response, st.session_state.messages)
                with st.chat_message("assistant",avatar='static/ChatbotAvatar.svg'):
                    st.markdown(string_response)
            
            st.session_state["disabled"] = False
            st.rerun()
        
if __name__ == '__main__':
    app()