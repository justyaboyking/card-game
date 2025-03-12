import streamlit as st
import streamlit.components.v1 as components
import os

# Set full page width and remove padding
st.set_page_config(
    page_title="Card Bluff Roulette",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS to maximize space
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    .stApp {
        background-color: #080b14;
    }
    iframe {
        width: 100%;
        height: 100vh;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(current_dir, "game tst.html")

# Read the HTML file with error handling
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Modify the HTML content to make it work better in an iframe
    modified_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body, html {{
                margin: 0;
                padding: 0;
                height: 100%;
                overflow: auto;
            }}
            #game-container {{
                width: 100%;
                min-height: 100vh;
                display: flex;
                justify-content: center;
            }}
            .container {{
                max-width: 800px;
                width: 100%;
            }}
        </style>
    </head>
    <body>
        <div id="game-container">
            {html_content}
        </div>
    </body>
    </html>
    """
    
    # Display the HTML content
    components.html(modified_html, height=1000, scrolling=True)
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
