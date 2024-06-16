import streamlit as st
import re
import uuid


def is_email_valid(email):
    pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, email):
        return True
    else:
        return False

def app():
    styles="""
        <style>
    [aria-label="Your Email"] {
        border:1px solid #f47a1f;
    }       
        </style>
    """
    st.write("International Potato Center")
    st.write(styles, unsafe_allow_html=True)

    if "email" not in st.session_state:
        st.session_state.email = None
        st.session_state.uuid = None

    if  st.session_state.email is None:
        st.write("# Welcome!")
        disclaimers=f"""Disclaimers:\n\n
- Need to sign SMTA of the ITPGRFA for genebank \n
- Need to sign SMTA of the ITPGRFA and aditional terms and conditions for breeding materials\n
- Need to request for an Import Permit or an Official letter from their Ministry of Agriculture\n
- If the Import Permit requires not standards tests, the requester must cover the costs of the aditional tests\n
- Need to check with your Ministry of Agriculture if any extra document is needed\n
- Need to cover the adm costs of producing the plants (depending on the requester and number of materials)\n
- Need to cover the costs of quarantine in your country - it is recommended to check these cost before engaging in the process of requests, because sometimes can be very expensive\n"""

        st.warning('This is prototype level code demonstrating technical feasibility. This is not suitable for production environments and provided as-is and without warranties.', icon="⚠️")

        ### Center Potato With Headset ####
        col1,col2,col3=st.columns(3)
        with col1:
            st.empty()
        with col2:
            st.image("static/potato_mod_frame3.png")
        with col3:
            st.empty()

        st.info(disclaimers,icon="ℹ️")
        email = st.text_input("Your Email",placeholder="Please enter a valid email address")
        
        

        if st.button("Proceed to Chatbot"):
            if is_email_valid(email):
                is_valid= is_email_valid(email)
                st.session_state.email = email
                st.session_state.uuid = uuid.uuid4().hex
                #page switching logic 
                st.success("Starting new chat...")
                st.switch_page("pages/chat.py")
            else:
                st.error("Invalid email")
        
if __name__ == '__main__':
    app()
