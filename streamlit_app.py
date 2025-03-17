import streamlit as st
import streamlit.components.v1 as components
import os
import base64

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
        height: 90vh;
        border: none;
    }
    .title {
        color: #00b4d8;
        text-align: center;
        margin-bottom: 5px;
        font-size: 24px;
    }
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Style audio controls */
    .audio-container {
        background-color: rgba(0, 180, 216, 0.1);
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid rgba(0, 180, 216, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Add a simple title
st.markdown('<div class="title">Card Bluff Roulette</div>', unsafe_allow_html=True)

# Create audio section using Streamlit's native audio support
with st.expander("🎵 Background Music (Click to expand)", expanded=False):
    st.write("Play background music while you enjoy the game!")
    
    # Multiple music options
    st.write("Choose your background track:")
    music_option = st.radio(
        "Select music style:",
        ["Suspense Game Music", "Upbeat Game Music", "Intense Battle", "Relaxing Lounge"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Map music options to URLs
    music_urls = {
        "Suspense Game Music": "https://assets.mixkit.co/music/preview/mixkit-game-show-suspense-waiting-667.mp3",
        "Upbeat Game Music": "https://assets.mixkit.co/music/preview/mixkit-fun-and-quirky-29.mp3",
        "Intense Battle": "https://assets.mixkit.co/music/preview/mixkit-games-worldbeat-466.mp3",
        "Relaxing Lounge": "https://assets.mixkit.co/music/preview/mixkit-tech-house-vibes-130.mp3"
    }
    
    # Display the selected music with Streamlit's native audio player
    st.audio(music_urls[music_option], format="audio/mp3", start_time=0)
    
    st.caption("Music provided by Mixkit - royalty free music and sound effects")

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(current_dir, "game tst.html")

# Read the HTML file with error handling
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Modify the HTML to remove the audio element and music button
    # Use regex to completely remove the old audio element
    import re
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
    components.html(html_content, height=720, scrolling=True)
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
