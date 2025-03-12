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

# Apply custom CSS to maximize space and prevent flickering
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
    /* Prevent Streamlit from handling clicks outside specific UI elements */
    .element-container {
        pointer-events: none;
    }
    /* But allow pointer events on the iframe itself */
    iframe {
        pointer-events: auto !important;
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
    
    # Add a wrapper to the HTML content to prevent event bubbling
    wrapped_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body, html {{
                margin: 0;
                padding: 0;
                height: 100%;
                overflow: hidden;
            }}
            #game-container {{
                width: 100%;
                height: 100vh;
            }}
        </style>
    </head>
    <body>
        <div id="game-container">
            {html_content}
        </div>
        <script>
            // Prevent event bubbling to Streamlit
            document.getElementById('game-container').addEventListener('click', function(e) {{
                e.stopPropagation();
            }}, true);
        </script>
    </body>
    </html>
    """
    
    # Display the wrapped HTML content
    components.html(wrapped_html, height=1000, scrolling=False)
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
