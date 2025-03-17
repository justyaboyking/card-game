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
    .audio-player {
        width: 1px;
        height: 1px;
        position: absolute;
        top: -100px;
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
    
    # Use a reliable, browser-friendly audio source
    music_url = "https://assets.mixkit.co/music/preview/mixkit-game-show-suspense-waiting-667.mp3"
    
    # Create a completely new audio implementation
    new_audio_script = f'''
    <script>
      // Create audio element dynamically to avoid browser restrictions
      window.setupGameAudio = function() {{
        // Create a new audio element programmatically
        if (!window.gameAudio) {{
          window.gameAudio = new Audio("{music_url}");
          window.gameAudio.loop = true;
          window.gameAudio.volume = 0.3;
          window.musicPlaying = false;
          
          // Log that audio was created
          console.log("Audio element created successfully");
        }}
      }};
      
      // New toggle music function with better error handling
      window.toggleMusic = function() {{
        // Make sure audio is set up
        if (!window.gameAudio) {{
          setupGameAudio();
        }}
        
        const musicButton = document.getElementById('musicToggle');
        console.log("Toggle music called, current state:", window.musicPlaying);
        
        if (window.musicPlaying) {{
          // Pause music
          window.gameAudio.pause();
          musicButton.innerHTML = '🔇';
          console.log("Music paused");
        }} else {{
          // Play music with detailed error handling
          try {{
            const playPromise = window.gameAudio.play();
            
            if (playPromise !== undefined) {{
              playPromise
                .then(() => {{
                  console.log("Music started playing successfully");
                  musicButton.innerHTML = '🔊';
                  // Show success message
                  const message = document.createElement('div');
                  message.style.cssText = 'position:fixed; top:60px; right:20px; background-color:rgba(0,180,216,0.8); color:white; padding:10px; border-radius:5px; z-index:1000; animation: fadeOut 2s forwards 3s;';
                  message.innerHTML = "Music playing! 🎵";
                  document.body.appendChild(message);
                  
                  // Add fade out animation
                  const style = document.createElement('style');
                  style.innerHTML = '@keyframes fadeOut {{ from {{ opacity: 1; }} to {{ opacity: 0; }} }}';
                  document.head.appendChild(style);
                  
                  // Remove message after animation
                  setTimeout(() => {{ document.body.removeChild(message); }}, 5000);
                }})
                .catch(error => {{
                  console.error("Error playing music:", error);
                  musicButton.innerHTML = '❌';
                  
                  // Show error message with instructions
                  alert("Unable to play music: " + error.message + "\\n\\nTry clicking the button again or refreshing the page.");
                  
                  // Reset button after 2 seconds
                  setTimeout(() => {{ musicButton.innerHTML = '🔊'; }}, 2000);
                }});
            }}
          }} catch (e) {{
            console.error("Exception playing music:", e);
            alert("Error with audio playback: " + e.message);
          }}
        }}
        
        window.musicPlaying = !window.musicPlaying;
      }};
      
      // Initialize audio on page load
      document.addEventListener('DOMContentLoaded', function() {{
        setupGameAudio();
        console.log("Audio setup complete on page load");
        
        // Add a click handler to the whole document to enable audio
        document.addEventListener('click', function audioEnabler() {{
          // This helps overcome browser autoplay restrictions
          setupGameAudio();
          window.gameAudio.play().then(() => {{
            window.gameAudio.pause(); // Immediately pause, but now audio is enabled
            window.musicPlaying = false;
            console.log("Audio enabled by user interaction");
          }}).catch(e => {{
            console.log("Audio not yet enabled:", e);
          }});
          
          // Remove this listener after first click
          document.removeEventListener('click', audioEnabler);
        }}, {{ once: true }});
      }});
    </script>
    '''
    
    # Use regex to completely remove the old audio element
    audio_pattern = re.compile(r'<audio[^>]*id=["\']backgroundMusic["\'][^>]*>.*?</audio>', re.DOTALL)
    html_content = audio_pattern.sub('', html_content)
    
    # Remove any old toggleMusic implementation
    old_toggle_pattern = re.compile(r'function toggleMusic\(\).*?}', re.DOTALL)
    html_content = old_toggle_pattern.sub('', html_content)
    
    # Add our new implementation before the closing </body> tag
    html_content = html_content.replace('</body>', f'{new_audio_script}</body>')
    
    # Create a small embedded player that's immediately accessible for testing
    test_player = '''
    <div style="position: fixed; bottom: 10px; left: 10px; z-index: 1000;">
      <button onclick="toggleMusic()" style="background: #00b4d8; color: white; border: none; border-radius: 4px; padding: 5px 10px;">
        Test Music
      </button>
    </div>
    '''
    
    # Add the test player
    html_content = html_content.replace('</body>', f'{test_player}</body>')
    
    # Display the HTML content
    components.html(html_content, height=800, scrolling=True)
    
    # Add instructions for users
    st.info("💡 **Tip:** Click the 🔊 button in the top-right corner to toggle music. If it doesn't work, use the 'Test Music' button in the bottom-left corner.")
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
