import streamlit as st
import re

def is_email_valid(email):
    pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, email):
        return True
    else:
        return False

def app():
    styles="""
        <style>
    [aria-label="Email"] {
        border:1px solid #f47a1f;
    }       
        </style>
    """
    st.write("International Potato Center")
    st.write(styles, unsafe_allow_html=True)

    if "email" not in st.session_state:
        st.session_state.email = None

    if  st.session_state.email is None:
        st.write("# Welcome!")
        
        email = st.text_input("Your Email",placeholder="Please enter a valid email address")
        
        if st.button("Proceed to Chatbot"):
            if is_email_valid(email):
                is_valid= is_email_valid(email)
                st.session_state.email = email
                #page switching logic 
                st.success("Starting new chat...")
                st.switch_page("pages/chat.py")
            else:
                st.error("Invalid email")
    
if __name__ == '__main__':
    app()
