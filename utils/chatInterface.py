import streamlit as st
import toml
import os
import asyncio
import base64
import itertools

def encode_svg(path):
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


chatbotAvatar_ref = encode_svg("./static/ChatbotAvatar.svg")
userAvatar_ref = encode_svg("./static/UserAvatar.svg")

async def show_spinner(processing_done):
    chatbotAvatar = chatbotAvatar_ref
    placeholder = st.empty()

    # setup typing array
    typing_array = ["Typing" + "." * i for i in range(8)]
    typing_animation = itertools.cycle(typing_array)
    
    while not processing_done.done():
        html_content = f"""
            <div style="display: flex; align-items: center; margin-bottom: 10px; padding-left:16px;justify-content:flex-start;">
                <img src="data:image/svg+xml;base64,{chatbotAvatar}" class="bot-avatar" alt="avatar" style="width: 40px; height: 40px;" />
                <div style="background: {assistantBackgroundColor}; color: {assistantTextColor}; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%; font-size: 14px;">
                    {next(typing_animation)} 
                </div>
            </div>
        """
        placeholder.markdown(html_content, unsafe_allow_html=True)
        await asyncio.sleep(0.25)
    
    placeholder.empty()

__all__ = ['show_spinner']



