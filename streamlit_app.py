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

# Function to serve local audio file
def get_audio_file_path():
    # Look for these music files in the current directory
    possible_filenames = ["background_music.mp3", "music.mp3", "game_music.mp3"]
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    for filename in possible_filenames:
        path = os.path.join(current_dir, filename)
        if os.path.exists(path):
            return path
    
    # If no music file is found, return None
    return None

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(current_dir, "game tst.html")

# Add a simple title
st.markdown('<div class="title">Card Bluff Roulette</div>', unsafe_allow_html=True)

# Read the HTML file with error handling
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Check if we have a local audio file
    audio_path = get_audio_file_path()
    
    if audio_path:
        # If we have a local audio file, create a base64 data URL
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            audio_b64 = base64.b64encode(audio_bytes).decode()
            audio_data_url = f"data:audio/mpeg;base64,{audio_b64}"
        
        # Create new audio element with the base64 data URL
        new_audio_element = f'''
        <audio id="backgroundMusic" loop>
          <source src="{audio_data_url}" type="audio/mpeg">
          Your browser does not support the audio element.
        </audio>
        '''
    else:
        # Fallback to a free music source if no local file is found
        new_audio_element = '''
        <audio id="backgroundMusic" loop>
          <source src="https://assets.mixkit.co/music/preview/mixkit-game-show-suspense-waiting-667.mp3" type="audio/mpeg">
          Your browser does not support the audio element.
        </audio>
        '''
        st.warning("No music file found. Using default music. Add 'background_music.mp3' to your project folder to use your own music.")
    
    # Replace the original audio element
    html_content = html_content.replace(
        '<audio id="backgroundMusic" loop>\n    <source src="https://suno.com/song/cdcd7d4d-e050-42f1-a614-356166e25c54" type="audio/mpeg">\n    Je browser ondersteunt het audio-element niet.\n  </audio>',
        new_audio_element
    )
    
    # Add improved audio playback script
    debug_script = '''
    <script>
      // Add this right before the closing </body> tag
      console.log("Music element found:", document.getElementById('backgroundMusic') !== null);
      
      // Override the original toggleMusic function with better error handling
      const originalToggleMusic = window.toggleMusic;
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
