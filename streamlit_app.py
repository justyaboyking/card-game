import streamlit as st
import streamlit.components.v1 as components
import os
import re
import base64

# Set full page width and remove padding
st.set_page_config(
    page_title="Card Bluff Roulette",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to autoplay audio in the background
def autoplay_audio(file_url):
    audio_html = f"""
        <audio autoplay loop style="display:none;">
            <source src="{file_url}" type="audio/mpeg">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

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
        height: 88vh;
        border: none;
    }
    .title {
        color: #00b4d8;
        text-align: center;
        margin-bottom: 5px;
        font-size: 24px;
    }
    /* Hide audio controls when not active */
    .audio-player {
        margin-bottom: 10px;
    }
    /* Make audio player look nicer */
    audio {
        border-radius: 30px;
        background-color: rgba(0, 180, 216, 0.1);
    }
    /* Hide Streamlit elements we don't need */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Add a simple title
st.markdown('<div class="title">Card Bluff Roulette</div>', unsafe_allow_html=True)

# Set the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Autoplay background music (hidden)
# Convert local audio file to base64 for embedding
def get_base64_audio(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            if len(data) < 1000:  # Check if file is too small (likely invalid)
                st.warning(f"The audio file at {file_path} appears to be invalid or too small ({len(data)} bytes). Please replace it with a valid MP3 file.")
                return None
            return base64.b64encode(data).decode()
    except Exception as e:
        st.error(f"Error loading audio file: {str(e)}")
        return None

# Try to use local file first, fall back to remote URL if not available
shadows_shuffle_path = os.path.join(current_dir, "Shadows Shuffle.mp3")
music_file_path = os.path.join(current_dir, "background_music.mp3")

# First try to use Shadows Shuffle.mp3
if os.path.exists(shadows_shuffle_path) and os.path.getsize(shadows_shuffle_path) > 1000:
    audio_base64 = get_base64_audio(shadows_shuffle_path)
    if audio_base64:
        audio_url = f"data:audio/mp3;base64,{audio_base64}"
        autoplay_audio(audio_url)
        st.success("Playing music from 'Shadows Shuffle.mp3'")
    else:
        # Fall back to background_music.mp3
        if os.path.exists(music_file_path) and os.path.getsize(music_file_path) > 1000:
            audio_base64 = get_base64_audio(music_file_path)
            if audio_base64:
                audio_url = f"data:audio/mp3;base64,{audio_base64}"
                autoplay_audio(audio_url)
                st.success("Playing music from 'background_music.mp3'")
            else:
                # No fallback to remote URL, just show error
                st.error("Could not load local MP3 files. Please ensure valid MP3 files are available.")
        else:
            # No fallback to remote URL, just show error
            st.error("Local MP3 files not found or invalid. Please add valid MP3 files to the application directory.")
else:
    # Try background_music.mp3 as fallback
    if os.path.exists(music_file_path) and os.path.getsize(music_file_path) > 1000:
        audio_base64 = get_base64_audio(music_file_path)
        if audio_base64:
            audio_url = f"data:audio/mp3;base64,{audio_base64}"
            autoplay_audio(audio_url)
            st.success("Playing music from 'background_music.mp3'")
        else:
            # No fallback to remote URL, just show error
            st.error("Could not load local MP3 file. Please ensure a valid MP3 file is available.")
    else:
        # No fallback to remote URL, just show error
        if not os.path.exists(music_file_path):
            st.error("Local MP3 files not found. Please add MP3 files to the application directory.")
        elif os.path.getsize(music_file_path) <= 1000:
            st.error(f"The MP3 file is too small ({os.path.getsize(music_file_path)} bytes) and appears to be invalid. Please replace it with a valid MP3 file.")

# Set the HTML file path (current_dir is already defined above)
html_file_path = os.path.join(current_dir, "game tst.html")

# Read the HTML file with error handling
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Remove audio element completely
    audio_pattern = re.compile(r'<audio[^>]*id=["\']backgroundMusic["\'][^>]*>.*?</audio>', re.DOTALL)
    html_content = audio_pattern.sub('', html_content)
    
    # Remove music button or repurpose it
    music_button_pattern = re.compile(r'<button id="musicToggle"[^>]*>.*?</button>', re.DOTALL)
    html_content = music_button_pattern.sub('', html_content)
    
    # Disable the toggleMusic function to prevent errors
    music_toggle_fix = '''
    <script>
      // Override music toggle to prevent errors
      window.toggleMusic = function() { return false; };
      
      // Override saveNamesAndStartGame to avoid audio errors
      const originalSaveNamesAndStartGame = window.saveNamesAndStartGame;
      window.saveNamesAndStartGame = function() {
        const name1 = document.getElementById('player1Name').value || "Player 1";
        const name2 = document.getElementById('player2Name').value || "Player 2";
        gameState.playerNames = [name1, name2];
        const max = parseInt(document.getElementById('maxCards').value);
        gameState.maxCards = (max && max > 0 && max <= 10) ? max : 10;
        
        // Skip audio part
        startGame();
      };
    </script>
    '''
    
    # Insert the fix before the closing body tag
    html_content = html_content.replace('</body>', f'{music_toggle_fix}</body>')
    
    # Display the HTML content
    components.html(html_content, height=750, scrolling=True)
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
