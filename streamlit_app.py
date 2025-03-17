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

# Function to get base64 encoded audio for direct embedding
def get_audio_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        return base64.b64encode(data).decode()

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
    .music-button {
        background: linear-gradient(135deg, #00b4d8, #0096c7);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 8px 15px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 180, 216, 0.3);
        display: flex;
        margin: 0 auto;
        align-items: center;
    }
    .button-container {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
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
    
    # Direct audio embed URL - using your provided URL
    audio_url = "https://s31.aconvert.com/convert/p3r68-cdx67/xwo2w-3rju8.mp3"
    
    # Modify the HTML to include direct audio playback
    modified_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body, html {{
                margin: 0;
                padding: 0;
                height: 100%;
                overflow: auto;
            }}
            #game-container {{
                width: 100%;
                min-height: 100vh;
                display: flex;
                justify-content: center;
            }}
            .container {{
                max-width: 800px;
                width: 100%;
            }}
            .audio-controls {{
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 1000;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .audio-button {{
                background: linear-gradient(135deg, #00b4d8, #0096c7);
                color: white;
                border: none;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            }}
        </style>
    </head>
    <body>
        <!-- Embedded audio element that will play automatically but muted initially -->
        <audio id="backgroundMusic" loop>
            <source src="{audio_url}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        
        <div class="audio-controls">
            <button id="audioToggle" class="audio-button" onclick="toggleAudio()">🔊</button>
        </div>
        
        <div id="game-container">
            {html_content}
        </div>
        
        <script>
            // Variables for audio state
            let isPlaying = false;
            const audioElement = document.getElementById('backgroundMusic');
            const audioButton = document.getElementById('audioToggle');
            
            // Function to toggle audio
            function toggleAudio() {{
                if (isPlaying) {{
                    audioElement.pause();
                    audioButton.innerText = '🔇';
                }} else {{
                    // Set volume before playing
                    audioElement.volume = 0.3;
                    
                    // Play with user interaction (this is important for browser policies)
                    const playPromise = audioElement.play();
                    
                    if (playPromise !== undefined) {{
                        playPromise.then(_ => {{
                            console.log("Audio playback started successfully");
                            audioButton.innerText = '🔊';
                        }}).catch(error => {{
                            console.error("Audio playback failed:", error);
                        }});
                    }}
                }}
                
                isPlaying = !isPlaying;
            }}
            
            // Auto-start audio with a slight delay (needs user interaction first in most browsers)
            document.body.addEventListener('click', function() {{
                if (!isPlaying) {{
                    setTimeout(() => {{
                        toggleAudio();
                    }}, 1000);
                }}
            }}, {{ once: true }});
        </script>
    </body>
    </html>
    """
    
    # Display the HTML content with embedded audio
    components.html(modified_html, height=800, scrolling=True)
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
