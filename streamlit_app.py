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

# Add a simple audio toggle in Streamlit
st.markdown('<div class="title">Card Bluff Roulette</div>', unsafe_allow_html=True)
st.markdown('<div class="button-container"><button id="music-toggle" class="music-button" onclick="toggleMusic()">🔊 Music On/Off</button></div>', unsafe_allow_html=True)

# Read the HTML file with error handling
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Remove the original music button
    html_content = html_content.replace('<button id="musicToggle" class="button music-button" onclick="toggleMusic()">🔊</button>', 
                                        '<!-- Music handled by Streamlit -->')
    
    # Modify the HTML to include a direct audio element that can be controlled
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
        </style>
    </head>
    <body>
        <!-- Embedded audio that's hidden but accessible via JavaScript -->
        <audio id="gameAudio" loop style="display:none;">
            <source src="https://assets.mixkit.co/music/preview/mixkit-game-level-music-689.mp3" type="audio/mpeg">
        </audio>
        
        <div id="game-container">
            {html_content}
        </div>
        
        <script>
            // Function to toggle music from outside the iframe
            function toggleMusic() {{
                const audio = document.getElementById('gameAudio');
                if (audio.paused) {{
                    audio.volume = 0.3;
                    audio.play();
                }} else {{
                    audio.pause();
                }}
            }}
            
            // Connect the Streamlit button to the audio toggle
            window.addEventListener('message', function(e) {{
                if (e.data.type === 'toggleMusic') {{
                    toggleMusic();
                }}
            }});
            
            // Make the toggle function available to parent
            window.toggleMusic = toggleMusic;
        </script>
    </body>
    </html>
    """
    
    # Add JavaScript to connect the Streamlit button to the iframe
    st.markdown("""
    <script>
        // Function to toggle music in the iframe when the button is clicked
        function toggleMusic() {
            const iframe = document.querySelector('iframe');
            if (iframe && iframe.contentWindow) {
                iframe.contentWindow.toggleMusic();
            }
        }
        
        // Connect the button to the toggle function
        document.getElementById('music-toggle').addEventListener('click', toggleMusic);
    </script>
    """, unsafe_allow_html=True)
    
    # Display the HTML content
    components.html(modified_html, height=800, scrolling=True)
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
