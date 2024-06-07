import streamlit as st
import re




def is_email_valid(email):
    pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, email):
        return True
    else:
        return False


st.set_page_config(
    page_title="Login Page",
    page_icon="🔐",
    layout="wide", 
    initial_sidebar_state="collapsed"  
)


st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)


st.write("International Potato Center")

def verify_email(email):
    return is_email_valid(email)

emails= ["example@gmail.com", 'epython.com', 'epython@info.com', 'ep-info.com', 'ep-info@gmail.com']


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
            st.success("Login successful!")
            st.switch_page("pages/chat.py")
        else:
            st.error("Invalid email")