<style>
    /* Style for the input container at the bottom of the page */
    #input-container {
        position: fixed;
        bottom: 0;
        width: 100%;
        padding: 10px;
        background-color: #F5F8FE;
        z-index: 100; /* Ensures it is on top of other elements */
    }

    /* Gradient text styles for headers */
    h1, h2 {
        font-weight: bold;
        background: linear-gradient(89.84deg, #5F2700 19.48%, #F47A1F 47.28%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline;
        font-size: 3em;
    }


    /* Styles for user avatar */
    .user-avatar {
        float: right;
        width: 40px;
        height: 40px;
        margin-left: 5px;
        margin-bottom: -10px;
        border-radius: 50%;
        object-fit: cover;
    }

    /* Styles for bot avatar */
    .bot-avatar {
        float: left;
        width: 40px;
        height: 40px;
        margin-right: 5px;
        border-radius: 50%;
        object-fit: cover;
    }

    /* Styles for horizontal blocks in Streamlit */
    div[data-testid="stHorizontalBlock"] {
        bottom: 0px;
        position: fixed;
        width: inherit;
        display: flex;
        align-items: baseline;
    }

    /* Adjusts padding for sidebar user content */
    div[data-testid="stSidebarUserContent"] {
        padding-top: 1rem; /* Streamlit's default padding-top when there is no nav is 6rem */
    }

    /* Styles for the sidebar section */
    section[data-testid="stSidebar"] {
        height: calc(100% - 5rem) !important;
        margin-top: 5rem;
        background: #FFFDFA;
        border-right: 1px solid #fbebde;
        box-shadow: none;
    }

    /* Main section adjustments */
    section.main {
        pointer-events: auto;
        position: relative;
        top: 5rem;
    }

    /* Styles for the navigation bar iframe */
    iframe[title="streamlit_navigation_bar.st_navbar"] {
        margin-left: 0px;
        margin-right: 0px;
        padding-left: 2rem;
        width: 50%;
        border-bottom: 1px solid  #fccfa9;
    }

    /* Styles for the header section */
    header[data-testid="stHeader"] {
        border-bottom: 1px solid  #fccfa9;
    }

    /* Adjustments for collapsed control */
    div[data-testid="collapsedControl"] {
        margin-top: 4.1rem;
        padding-left: 1rem;
    }

    /* Color change for collapsed control and main menu icons */
    div[data-testid="collapsedControl"] path:nth-of-type(2),
    span[data-testid="stMainMenu"] path:nth-of-type(2) {
        fill: #00205A !important;
    }

    /* Hides the Streamlit toolbar */
    div[data-testid="stToolbar"] {
        display: none;
    }
    .gradient-text {
  font-weight: bold;
 
background: linear-gradient(89.84deg, #5F2700 6.14%, #F47A1F 36.64%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline;
  font-size: 3em;
}
 div[data-testid="stChatInput"] {
    background: #F8F8F8;
}

</style>