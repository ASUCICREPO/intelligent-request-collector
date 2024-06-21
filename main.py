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
        disclaimers = """Disclaimers:

Please be aware that for germplasm distribution and acquisition, the following international standards apply:

- In order to receive Plant Genetic Resources for Food and Agriculture (PGRFA), the customer must accept the Standard Material Transfer Agreement (SMTA) of the International Treaty on Plant Genetic Resources for Food and Agriculture (ITPGRFA) through signature, digital acceptance, or by the act of receiving and unpacking the shipment.

- In order to receive PGRFA in the development phase (breeding materials), the customer must accept the SMTA of the ITPGRFA and additional terms and conditions that apply for the distribution of breeding materials.

- These standard agreements apply to cases where the use is for breeding, research, and education for food and agriculture only. If the purpose of the use is different, such as cosmetic, pharmaceutical, or others, specific agreements and permissions will be required on a case-by-case basis.

- The customer must request an import permit or an official letter issued by the competent authorities (e.g., Ministry of Agriculture) of the importing country specifying the type of requested materials (e.g., in vitro, botanical seeds).

- If the import permit requires additional non-standard plant health tests, the requester must cover the cost for the additional tests.

- It is recommended to check with the competent authorities if additional documents are required for PGRFA importation.

- Depending on the requester and the number of requested PGRFA, a fee will be charged to cover recovery and distribution costs.

- Please be aware that the costs of plant quarantine in the destination country must be covered by the customer. It is therefore recommended to check these costs and country requirements prior to requesting PGRFA.
"""
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
