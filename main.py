import streamlit as st
import re

def is_email_valid(email):
    pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, email):
        return True
    else:
        return False

def app():
    st.write("International Potato Center")

    def verify_email(email):
        return is_email_valid(email)

    if "email" not in st.session_state:
        st.session_state.email = None

    if  st.session_state.email is None:
        st.write("# Welcome!")
        
        email = st.text_input("Email")
        
        if st.button("Proceed to Chatbot"):
            if verify_email(email):
                is_valid= is_email_valid(email)
                st.session_state.email = email
                #page switching logic 
                st.success("Starting new chat...")
                st.switch_page("pages/chat.py")
            else:
                st.error("Invalid email")

if __name__ == '__main__':
    app()
