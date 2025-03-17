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
</style>
""", unsafe_allow_html=True)

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(current_dir, "game tst.html")

# Add a simple title
st.markdown('<div class="title">Card Bluff Roulette</div>', unsafe_allow_html=True)

# Read the HTML file with error handling
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Direct audio embed URL
    audio_url = "https://s31.aconvert.com/convert/p3r68-cdx67/xwo2w-3rju8.mp3"
    
    # Replace the original audio source with our new URL
    html_content = html_content.replace(
        '<source src="https://suno.com/song/cdcd7d4d-e050-42f1-a614-356166e25c54" type="audio/mpeg">',
        f'<source src="{audio_url}" type="audio/mpeg">'
    )
    
    # Add the toggleMusic function if it's not already there
    music_function = """
    // --------------------
    // Audio functions
    // --------------------
    let musicPlaying = false;
    
    function toggleMusic() {
      const backgroundMusic = document.getElementById('backgroundMusic');
      const musicButton = document.getElementById('musicToggle');
      
      if (musicPlaying) {
        backgroundMusic.pause();
        musicButton.innerHTML = '🔇';
      } else {
        backgroundMusic.volume = 0.3;
        backgroundMusic.play()
          .then(() => {
            console.log("Music started playing");
          })
          .catch(error => {
            console.error("Error playing music:", error);
          });
        musicButton.innerHTML = '🔊';
      }
      
      musicPlaying = !musicPlaying;
    }
    """
    
    # Make sure the music button is definitely at the right place
    # First, remove any existing music button
    if '<button id="musicToggle" class="button music-button" onclick="toggleMusic()">🔊</button>' in html_content:
        html_content = html_content.replace(
            '<button id="musicToggle" class="button music-button" onclick="toggleMusic()">🔊</button>',
            ''
        )
    
    # Then add the button back in the right place (before the endGameBtn)
    html_content = html_content.replace(
        '<!-- Fixed End Game button -->',
        '<!-- Music control button -->\n  <button id="musicToggle" class="button music-button" onclick="toggleMusic()">🔊</button>\n  <!-- Fixed End Game button -->'
    )
    
    # Make sure the music button style is defined
    music_button_style = """
    .music-button {
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 200;
      font-size: 18px;
      padding: 10px 15px;
      border-radius: 50%;
    }
    """
    
    # Add the style if it's not already there
    if '.music-button {' not in html_content:
        html_content = html_content.replace(
            '</style>',
            f'{music_button_style}</style>'
        )
    
    # Make sure the toggleMusic function is in the JavaScript
    if 'function toggleMusic()' not in html_content:
        html_content = html_content.replace(
            '<script>',
            f'<script>\n{music_function}'
        )
    
    # Display the modified HTML content
    components.html(html_content, height=800, scrolling=True)
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
