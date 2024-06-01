import streamlit as st
import html
import re
import toml
import os
import re
import base64

def _encode_svg(path):
    """Encode an SVG to base64, from an absolute path."""
    svg = open(path).read()
    return base64.b64encode(svg.encode("utf-8")).decode("utf-8")


# Define the path to the config.toml file
config_path = os.path.join(os.path.dirname(
    __file__), '..', '.streamlit', 'config.toml')

# Define the path to the config.toml file
custom_theme_path = os.path.join(os.path.dirname(
    __file__), '..', '.custom_themes', 'cip.toml')

# Load the configuration file
config = toml.load(config_path)
custom_theme= toml.load(custom_theme_path)

# Extract colors from the config

primary_color = custom_theme["theme"]["primaryColor"]
text_color = custom_theme["theme"]["textColor"]

userTextColor = custom_theme["theme"]["userTextColor"]
userBackgroundColor = custom_theme["theme"]["userBackgroundColor"]

assistantTextColor = custom_theme["theme"]["assistantTextColor"]
assistantBackgroundColor = custom_theme["theme"]["assistantBackgroundColor"]


chatbotAvatar_ref = _encode_svg("./static/ChatbotAvatar.svg")
userAvatar_ref = _encode_svg("./static/UserAvatar.svg")


def message_func(text, is_user=False, is_df=False, model="gpt", phi=False):
    """
    This function is used to display the messages in the chatbot UI.

    Parameters:
    text (str): The text to be displayed.
    is_user (bool): Whether the message is from the user or not.
    is_df (bool): Whether the message is a dataframe or not.
    """
    chatbotAvatar = chatbotAvatar_ref

    userAvatar = userAvatar_ref
    if is_user:
        userAvatar = userAvatar_ref
        avatar_class = "user-avatar"
        st.write(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content:flex-end;">
                    <div style="background: {userBackgroundColor}; color: {userTextColor}; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 14px;">
                        {text} \n </div>
                    <img src="data:image/svg+xml;base64,{chatbotAvatar}" class="{avatar_class}" alt="avatar" style="width: 40px; height: 40px;" />
                </div>
                """,
            unsafe_allow_html=True,
        )
    else:
        avatar_class = "bot-avatar"
        st.write(
            f"""
                    <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content:flex-start;">
                    <img src="data:image/svg+xml;base64,{userAvatar}" class="{avatar_class}" alt="avatar" style="width: 40px; height: 40px;" />
                    <div style="background: {assistantBackgroundColor}; color: {assistantTextColor}; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 14px;">
                        {text} \n </div>
                </div>
                    """,
            unsafe_allow_html=True,
        )