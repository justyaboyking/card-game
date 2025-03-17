import streamlit as st
import streamlit.components.v1 as components
import os
import base64
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
    .file-info {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Debug information display
st.markdown('<div class="title">Card Bluff Roulette</div>', unsafe_allow_html=True)

# Get the current directory and list all files
current_dir = os.path.dirname(os.path.abspath(__file__))
files_in_dir = os.listdir(current_dir)

# Display files for debugging
with st.expander("⚙️ Debug Info (Click to expand)"):
    st.write("Files in directory:")
    for file in files_in_dir:
        st.write(f"- {file}")

# Function to find music files
def get_audio_file_path():
    # Look for music files with case-insensitive matching
    possible_filenames = ["background_music.mp3", "music.mp3", "game_music.mp3", 
                         "BACKGROUND_MUSIC.MP3", "Background_Music.mp3"]
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # First check exact matches
    for filename in possible_filenames:
        path = os.path.join(current_dir, filename)
        if os.path.exists(path):
            return path
    
    # Then try case-insensitive search through all files
    for file in os.listdir(current_dir):
        if file.lower().endswith('.mp3'):
            return os.path.join(current_dir, file)
    
    # If no music file is found, return None
    return None

# Path to HTML file
html_file_path = os.path.join(current_dir, "game tst.html")

# Read the HTML file with error handling
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Check if we have a local audio file
    audio_path = get_audio_file_path()
    
    if audio_path:
        st.success(f"Found music file: {os.path.basename(audio_path)}")
        
        # Get file size for debugging
        file_size = os.path.getsize(audio_path) / (1024 * 1024)  # Size in MB
        
        # If we have a local audio file, create a base64 data URL
        try:
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
            st.info(f"Music file encoded successfully. File size: {file_size:.2f} MB")
        except Exception as e:
            st.error(f"Error encoding music file: {e}")
            # Fallback to default music
            new_audio_element = '''
            <audio id="backgroundMusic" loop>
              <source src="https://assets.mixkit.co/music/preview/mixkit-game-show-suspense-waiting-667.mp3" type="audio/mpeg">
              Your browser does not support the audio element.
            </audio>
            '''
    else:
        st.warning("No music file found. Using default music. Add 'background_music.mp3' to your project folder to use your own music.")
        # Fallback to a free music source if no local file is found
        new_audio_element = '''
        <audio id="backgroundMusic" loop>
          <source src="https://assets.mixkit.co/music/preview/mixkit-game-show-suspense-waiting-667.mp3" type="audio/mpeg">
          Your browser does not support the audio element.
        </audio>
        '''
    
    # More robust replacement using regex to handle whitespace variations
    audio_pattern = re.compile(r'<audio[^>]*id=["\']backgroundMusic["\'][^>]*>.*?</audio>', re.DOTALL)
    if audio_pattern.search(html_content):
        html_content = audio_pattern.sub(new_audio_element, html_content)
        st.success("Audio element replaced successfully")
    else:
        st.error("Could not find audio element in HTML file")
    
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
          alert("Music player not found. Try refreshing the page.");
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
            alert("Error playing music. Please try again.");
          }
        }
        
        musicPlaying = !musicPlaying;
      };
    </script>
    '''
    
    # Insert the debug script before closing body tag
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', f'{debug_script}</body>')
        st.success("Debug script inserted successfully")
    else:
        st.error("Could not find </body> tag in HTML file")
    
    # Display the HTML content
    components.html(html_content, height=800, scrolling=True)
    
    # Add instructions for users
    st.info("💡 **Tip:** If music doesn't play automatically, click the 🔊 button in the top-right corner.")
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
