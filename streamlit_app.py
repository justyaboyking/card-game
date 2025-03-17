import streamlit as st
import streamlit.components.v1 as components
import os
import re

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

# Add a simple title
st.markdown('<div class="title">Card Bluff Roulette</div>', unsafe_allow_html=True)

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(current_dir, "game tst.html")

# Read the HTML file with error handling
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # No audio fix script - this completely removes audio functionality
    # but preserves all game functionality
    remove_audio_script = '''
    <script>
      // Fix for music toggle button
      window.toggleMusic = function() {
        const musicButton = document.getElementById('musicToggle');
        if (musicButton) {
          musicButton.innerHTML = '🎮';  // Change to a game icon instead
        }
        
        // Show a small notification
        const notification = document.createElement('div');
        notification.style.cssText = 'position:fixed; top:70px; right:20px; background-color:rgba(255,255,255,0.8); color:#333; padding:8px 15px; border-radius:4px; font-size:14px; z-index:1000; transition:opacity 0.5s;';
        notification.innerHTML = "Playing without music";
        document.body.appendChild(notification);
        
        // Fade out and remove notification
        setTimeout(() => {
          notification.style.opacity = '0';
          setTimeout(() => {
            document.body.removeChild(notification);
          }, 500);
        }, 2000);
        
        return false;
      };
      
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
      
      // Set music button on load
      document.addEventListener('DOMContentLoaded', function() {
        const musicButton = document.getElementById('musicToggle');
        if (musicButton) {
          musicButton.innerHTML = '🎮';
        }
      });
    </script>
    '''
    
    # Use regex to completely remove the audio element 
    audio_pattern = re.compile(r'<audio[^>]*id=["\']backgroundMusic["\'][^>]*>.*?</audio>', re.DOTALL)
    html_content = audio_pattern.sub('', html_content)
    
    # Insert the remove audio script before the closing body tag
    html_content = html_content.replace('</body>', f'{remove_audio_script}</body>')
    
    # Display the HTML content
    components.html(html_content, height=800, scrolling=True)
    
    # Add instructions for users
    st.warning("⚠️ Game music has been disabled to ensure the game works correctly. Enjoy playing!")
    st.info("If you'd like to add your own background music, consider playing it from your device while enjoying the game.")
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
