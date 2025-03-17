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
    
    # Direct link to background music
    # This uses a free game music track from Mixkit - replace with your own if desired
    music_url = "https://assets.mixkit.co/music/preview/mixkit-game-show-suspense-waiting-667.mp3"
    
    # Create new audio element with direct URL
    new_audio_element = f'''
    <audio id="backgroundMusic" loop>
      <source src="{music_url}" type="audio/mpeg">
      Your browser does not support the audio element.
    </audio>
    '''
    
    # More robust replacement using regex
    audio_pattern = re.compile(r'<audio[^>]*id=["\']backgroundMusic["\'][^>]*>.*?</audio>', re.DOTALL)
    html_content = audio_pattern.sub(new_audio_element, html_content)
    
    # Add improved audio playback script
    debug_script = '''
    <script>
      // Add this right before the closing </body> tag
      console.log("Music element found:", document.getElementById('backgroundMusic') !== null);
      
      // Override the original toggleMusic function with better error handling
      window.toggleMusic = function() {
        const backgroundMusic = document.getElementById('backgroundMusic');
        const musicButton = document.getElementById('musicToggle');
        
        if (!backgroundMusic) {
          console.error("Background music element not found!");
          return;
        }
        
        console.log("Toggle music called, current state:", musicPlaying);
        
        if (musicPlaying) {
          backgroundMusic.pause();
          musicButton.innerHTML = '🔇';
          console.log("Music paused");
        } else {
          backgroundMusic.volume = 0.3;
          
          try {
            const playPromise = backgroundMusic.play();
            
            if (playPromise !== undefined) {
              playPromise
                .then(() => {
                  console.log("Music started playing successfully");
                  musicButton.innerHTML = '🔊';
                })
                .catch(error => {
                  console.error("Error playing music:", error);
                  alert("Click the 🔊 button to start music (browser autoplay blocked)");
                });
            }
          } catch (e) {
            console.error("Exception playing music:", e);
          }
        }
        
        musicPlaying = !musicPlaying;
      };
    </script>
    '''
    
    # Insert the debug script before closing body tag
    html_content = html_content.replace('</body>', f'{debug_script}</body>')
    
    # Display the HTML content
    components.html(html_content, height=800, scrolling=True)
    
    # Add instructions for users
    st.info("💡 **Tip:** If music doesn't play automatically, click the 🔊 button in the top-right corner.")
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
