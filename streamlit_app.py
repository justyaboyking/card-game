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
    .title {
        color: #00b4d8;
        text-align: center;
        margin-bottom: 5px;
        font-size: 24px;
    }
    .audio-button {
        background: linear-gradient(135deg, #00b4d8, #0096c7);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 8px 15px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        display: flex;
        margin: 0 auto 10px auto;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0, 180, 216, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(current_dir, "game tst.html")

# Add a title and audio button
st.markdown('<div class="title">Card Bluff Roulette</div>', unsafe_allow_html=True)

# Add a simple audio player in Streamlit
audio_file = "https://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3"
st.audio(audio_file, format='audio/mp3', start_time=0)

# Read the HTML file with error handling
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Remove the old audio element and music button to avoid conflicts
    html_content = html_content.replace(
        '<!-- Audio element for background music -->\n  <audio id="backgroundMusic" loop>\n    <source src="https://suno.com/song/cdcd7d4d-e050-42f1-a614-356166e25c54" type="audio/mpeg">\n    Je browser ondersteunt het audio-element niet.\n  </audio>',
        '<!-- Audio is now handled by Streamlit -->'
    )
    
    html_content = html_content.replace(
        '<button id="musicToggle" class="button music-button" onclick="toggleMusic()">🔊</button>',
        ''
    )
    
    # Display the modified HTML content
    components.html(html_content, height=800, scrolling=True)
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
