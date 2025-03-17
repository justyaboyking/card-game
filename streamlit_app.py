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
    
    # Create a complete inline JavaScript audio player
    # This approach embeds actual base64 audio directly into the page to avoid CORS issues
    audio_fix_script = '''
    <script>
      // Create audio using Web Audio API - maximum browser compatibility
      let audioContext;
      let audioBuffer;
      let audioSource;
      window.musicPlaying = false;
      
      // This uses a short, completely free sound loop
      const BASE64_SOUND = "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Ljc2LjEwMAAAAAAAAAAAAAAA//tAwAAAAAAAAAAAAAAAAAAAAAAAWGluZwAAAA8AAAACAAADwADMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM//////////////////////////////////////////////////////////////////8AAAAATGF2YzU4LjEzAAAAAAAAAAAAAAAAJAYEAAAAAAAAA8AnCLLjAAAAAAAAAAAAAAAAAAAA//tSwAAB8AAAaQAAAAgAAA0gAAABAMzl8+gEFsJGjCAIchERjQZDIEYxUGDJ4GCAX4EL5P4EOdAEPvJPjnw5/+CYP6gQOV+UDgQHfiQ+T8nP+pzghcoD//IDhwQGP///Lv//////oEQJjof/+pyCQDH//8MXKf//+SDgx///wQcnH//6BAgc///KBw4IBj//9TkEgGP//4YuU///yQcGP//+CDk4//9AgQOf//+UDhwQDH//6nIJAMf//wxcp///kg4Mf//8EHJx//6BAgc///KBw4IBj//9TkEgGP//4YuU///yQcGP//+CDk4//9AgQOf//+VDlz4Y///U5JAMf//wxfKf//yQeGP//+CDk4//9AgQOf//+UDhw4DH//6nJJAMf//wxcp///JB4Y///4IOT///QIED///5QOHDAL//6vkDnADCA38MAAQQON///JB4Y///4IHh///0CA4///8MWP/+QDH//6n//////wQIED//8n/////+UDlw4C//+r//////yQIEBj//9P//////4IPDgP//1P/////4ImU4c///1f/////kg8OA///U///////gg8OA///V//////+SDw4D//9T//////+CBwYD//9X//////5IODAf//qf//////ggcGA///V//////+SDgwH//6n//////4IHBgP//1P//////5IPDAP//qf//////ggcGA///U///////kgcGA///qf//////wQODAf//U///////kgcGA///1P/////+CBwYD//9T//////+SDwwH//6n//////8EDgwH//1P//////5IPDAP//qf/////+p7OPpwwAFsJGjCAIchERjQZDIEYxUGDJ4GCAX4EL5P4EOdAEPvJPjnw5/+CYP6gQOV+UDgQHfiQ+T8nP+pzghcoD//IDhwQGP///Lv//////oEQJjof/+pyCQDH//8MXKf//+SDgx///wQcnH//6BAgc///KBw4IBj//9TkEgGP//4YuU///yQcGP//+CDk4//9AgQOf//+UDhwQDH//6nIJAMf//wxcp///kg4Mf//8EHJx//6BAgc///KBw4IBj//9TkEgGP//4YuU///yQcGP//+CDk4//9AgQOf//+VDlz4Y///U5JAMf//wxfKf//yQeGP//+CDk4//9AgQOf//+UDhw4DH//6nJJAMf//wxcp///JB4Y///4IOT///QIED///5QOHDAL//6vkDnADCA38MAAQQON///JB4Y///4IHh///0CA4///8MWP/+QDH//6n//////wQIED//8n/////+UDlw4C//+r//////yQIEBj//9P//////4IPDgP//1P/////4ImU4c///1f/////kg8OA///U///////gg8OA///V//////+SDw4D//9T//////+CBwYD//9X//////5IODAf//qf//////ggcGA///V//////+SDgwH//6n//////4IHBgP//1P//////5IPDAP//qf//////ggcGA///U///////kgcGA///qf//////wQODAf//U///////kgcGA///1P/////+CBwYD//9T//////+SDwwH//6n//////8EDgwH//1P//////5IPDAP//qf/////+p7OPpw==";

      // Initialize audio system with our embedded sound
      function initAudio() {
        try {
          // Create audio context
          audioContext = new (window.AudioContext || window.webkitAudioContext)();
          
          // Convert base64 to array buffer
          const base64 = BASE64_SOUND;
          const binaryString = window.atob(base64);
          const len = binaryString.length;
          const bytes = new Uint8Array(len);
          for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
          }
          
          // Decode the audio data
          audioContext.decodeAudioData(bytes.buffer, function(buffer) {
            audioBuffer = buffer;
            console.log("Audio initialized successfully!");
          }, function(err) {
            console.error("Error decoding audio", err);
          });
        } catch (e) {
          console.error("Audio initialization failed:", e);
        }
      }
      
      // Play the sound with looping
      function playSound() {
        if (!audioContext || !audioBuffer) {
          console.error("Audio not initialized");
          return false;
        }
        
        try {
          // Create new source
          audioSource = audioContext.createBufferSource();
          audioSource.buffer = audioBuffer;
          audioSource.loop = true;
          audioSource.connect(audioContext.destination);
          audioSource.start(0);
          return true;
        } catch (e) {
          console.error("Error playing sound:", e);
          return false;
        }
      }
      
      // Stop the currently playing sound
      function stopSound() {
        if (audioSource) {
          try {
            audioSource.stop();
          } catch (e) {
            console.error("Error stopping sound:", e);
          }
        }
      }
      
      // Initialize audio on page load
      document.addEventListener('DOMContentLoaded', function() {
        // Initialize our audio system
        initAudio();
        
        // Wait for user interaction to enable audio
        document.addEventListener('click', function enableAudio() {
          if (audioContext && audioContext.state === 'suspended') {
            audioContext.resume();
          }
          document.removeEventListener('click', enableAudio);
        }, { once: true });
      });
      
      // Override the toggleMusic function
      window.toggleMusic = function() {
        const musicButton = document.getElementById('musicToggle');
        
        if (window.musicPlaying) {
          // Stop music
          stopSound();
          musicButton.innerHTML = '🔇';
          window.musicPlaying = false;
        } else {
          // Start music
          if (audioContext && audioContext.state === 'suspended') {
            audioContext.resume();
          }
          
          if (playSound()) {
            musicButton.innerHTML = '🔊';
            window.musicPlaying = true;
          } else {
            // Show error
            musicButton.innerHTML = '❌';
            setTimeout(() => {
              musicButton.innerHTML = '🔊';
            }, 2000);
          }
        }
      };
      
      // Override saveNamesAndStartGame
      const originalSaveNamesAndStartGame = window.saveNamesAndStartGame;
      window.saveNamesAndStartGame = function() {
        const name1 = document.getElementById('player1Name').value || "Player 1";
        const name2 = document.getElementById('player2Name').value || "Player 2";
        gameState.playerNames = [name1, name2];
        const max = parseInt(document.getElementById('maxCards').value);
        gameState.maxCards = (max && max > 0 && max <= 10) ? max : 10;
        
        // Initialize audio if not already done
        if (!audioContext) {
          initAudio();
        }
        
        // Try to play music (will work if user has interacted)
        if (audioContext && audioContext.state === 'running') {
          playSound();
          window.musicPlaying = true;
          const musicButton = document.getElementById('musicToggle');
          if (musicButton) {
            musicButton.innerHTML = '🔊';
          }
        }
        
        startGame();
      };
    </script>
    '''
    
    # Use regex to completely remove the old audio element
    audio_pattern = re.compile(r'<audio[^>]*id=["\']backgroundMusic["\'][^>]*>.*?</audio>', re.DOTALL)
    html_content = audio_pattern.sub('', html_content)
    
    # Insert our audio script before the closing body tag
    html_content = html_content.replace('</body>', f'{audio_fix_script}</body>')
    
    # Display the HTML content
    components.html(html_content, height=800, scrolling=True)
    
    # Add instructions for users
    st.info("🎵 **Music Instructions:** Click the 🔊 button in the top-right corner to toggle game music. You may need to click it twice or interact with the game first.")
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
