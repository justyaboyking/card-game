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

# Function to autoplay audio in the background with fallback for mobile/incognito
def autoplay_audio(file_url, audio_id="streamlit_audio"):
    audio_html = f"""
        <div id="audio-container" style="text-align: center; margin-bottom: 10px; display: none;">
            <button id="manual-play-button" style="background: linear-gradient(135deg, #00b4d8, #0096c7); color: white; border: none; border-radius: 30px; padding: 8px 16px; font-size: 14px; cursor: pointer; margin: 5px;">
                🎵 Play Background Music
            </button>
            <span id="audio-status" style="font-size: 12px; color: #aaa;"></span>
        </div>
        <audio id="{audio_id}" autoplay loop style="display:none;">
            <source src="{file_url}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        <script>
            // Check for mobile devices
            function isMobile() {{
                return /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent);
            }}

            // Check if likely in incognito mode (not 100% reliable)
            function isLikelyIncognito() {{
                return !window.localStorage || !window.indexedDB;
            }}

            // Show the manual play button with a given message
            function showPlayButton(message) {{
                const container = document.getElementById('audio-container');
                const status = document.getElementById('audio-status');
                if (container) {{
                    container.style.display = 'block';
                }}
                if (status && message) {{
                    status.textContent = message;
                }}
            }}

            document.addEventListener('DOMContentLoaded', function() {{
                const audio = document.getElementById('{audio_id}');
                let autoplaySuccessful = false;
                
                // Expose audio element for mute control if needed
                window.streamlitAudio = audio;
                
                // Setup manual play button
                const playButton = document.getElementById('manual-play-button');
                if (playButton) {{
                    playButton.addEventListener('click', function() {{
                        if (audio) {{
                            audio.play()
                                .then(() => {{
                                    autoplaySuccessful = true;
                                    showPlayButton('✓ Music playing');
                                    setTimeout(() => {{
                                        document.getElementById('audio-container').style.display = 'none';
                                    }}, 3000);
                                }})
                                .catch(e => {{
                                    console.error('Manual play failed:', e);
                                    showPlayButton('⚠️ Browser blocked audio - try clicking again');
                                }});
                        }}
                    }});
                }}
                
                // On mobile devices or if in incognito mode, show play button immediately
                if (isMobile() || isLikelyIncognito()) {{
                    showPlayButton('Tap to play background music');
                }}
                
                // Attempt autoplay on desktop
                audio.play()
                    .then(() => {{
                        autoplaySuccessful = true;
                        console.log('Autoplay successful');
                    }})
                    .catch(e => {{
                        console.log('Initial audio play failed, will retry:', e);
                        showPlayButton('Click to play background music');
                        // Retry after a short delay
                        setTimeout(() => {{
                            audio.play()
                                .then(() => {{
                                    autoplaySuccessful = true;
                                    document.getElementById('audio-container').style.display = 'none';
                                }})
                                .catch(e => {{
                                    console.log('Second audio play attempt failed:', e);
                                }});
                        }}, 2000);
                    }});
                
                // Monitor audio state and attempt restart if stopped
                setInterval(() => {{
                    if (audio && autoplaySuccessful && (audio.paused || audio.ended) && !audio.muted) {{
                        console.log('Audio stopped, attempting to restart');
                        audio.play().catch(e => {{
                            console.log('Restart failed:', e);
                            autoplaySuccessful = false;
                            showPlayButton('Music stopped - click to resume');
                        }});
                    }}
                }}, 5000);
            }});
        </script>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# Apply custom CSS to maximize space and style the page
st.markdown("""
<style>
    .main .block-container {
        padding: 1rem;
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
    /* Hide audio controls when not active */
    .audio-player {
        margin-bottom: 10px;
    }
    /* Style the audio element */
    audio {
        border-radius: 30px;
        background-color: rgba(0, 180, 216, 0.1);
    }
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Set the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Convert local audio file to base64 for embedding
def get_base64_audio(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            if len(data) < 1000:  # Ensure file is valid
                st.warning(f"The audio file at {file_path} appears to be invalid or too small ({len(data)} bytes).")
                return None
            encoded_data = base64.b64encode(data).decode()
            return encoded_data
    except Exception as e:
        st.error(f"Error loading audio file: {str(e)}")
        return None

# Use "Shadows Shuffle.mp3" as the primary audio file, fallback to "background_music.mp3" if needed
shadows_shuffle_path = os.path.join(current_dir, "Shadows Shuffle.mp3")
music_file_path = os.path.join(current_dir, "background_music.mp3")

if os.path.exists(shadows_shuffle_path) and os.path.getsize(shadows_shuffle_path) > 1000:
    audio_base64 = get_base64_audio(shadows_shuffle_path)
    if audio_base64:
        audio_url = f"data:audio/mp3;base64,{audio_base64}"
        autoplay_audio(audio_url)
    else:
        if os.path.exists(music_file_path) and os.path.getsize(music_file_path) > 1000:
            audio_base64 = get_base64_audio(music_file_path)
            if audio_base64:
                audio_url = f"data:audio/mp3;base64,{audio_base64}"
                autoplay_audio(audio_url)
            else:
                st.error("Could not load local MP3 files. Please ensure valid MP3 files are available.")
        else:
            st.error("Local MP3 files not found or invalid. Please add valid MP3 files to the application directory.")
else:
    if os.path.exists(music_file_path) and os.path.getsize(music_file_path) > 1000:
        audio_base64 = get_base64_audio(music_file_path)
        if audio_base64:
            audio_url = f"data:audio/mp3;base64,{audio_base64}"
            autoplay_audio(audio_url)
        else:
            st.error("Could not load local MP3 file. Please ensure a valid MP3 file is available.")
    else:
        if not os.path.exists(music_file_path):
            st.error("Local MP3 files not found. Please add MP3 files to the application directory.")
        elif os.path.getsize(music_file_path) <= 1000:
            st.error(f"The MP3 file is too small ({os.path.getsize(music_file_path)} bytes) and appears to be invalid.")

# Set the HTML file path (for your game)
html_file_path = os.path.join(current_dir, "game tst.html")

# Read and display the HTML file with error handling
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Remove any existing audio element with id "backgroundMusic"
    html_content = re.sub(r'<audio[^>]*id=["\']backgroundMusic["\'][^>]*>.*?</audio>', '', html_content, flags=re.DOTALL)
    # Remove the music toggle button if present
    html_content = re.sub(r'<button id="musicToggle"[^>]*>.*?</button>', '', html_content, flags=re.DOTALL)
    
    # Override toggle functions to prevent audio errors
    music_toggle_fix = '''
    <script>
      window.toggleMusic = function() { return false; };
      const originalSaveNamesAndStartGame = window.saveNamesAndStartGame;
      window.saveNamesAndStartGame = function() {
        const name1 = document.getElementById('player1Name').value || "Player 1";
        const name2 = document.getElementById('player2Name').value || "Player 2";
        gameState.playerNames = [name1, name2];
        const max = parseInt(document.getElementById('maxCards').value);
        gameState.maxCards = (max && max > 0 && max <= 10) ? max : 10;
        startGame();
      };
    </script>
    '''
    
    html_content = html_content.replace('</body>', f'{music_toggle_fix}</body>')
    
    # Optional mute button setup (adjust state as needed)
    col1, col2 = st.columns([10, 1])
    with col2:
        if st.button("🔊 Mute", key="mute_button"):
            st.session_state.muted = not st.session_state.get('muted', False)
            st.rerun()
    
    mute_state = st.session_state.get('muted', False)
    mute_icon = "🔇" if mute_state else "🔊"
    mute_text = "Unmute" if mute_state else "Mute"
    
    st.markdown(f"""
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const buttons = document.querySelectorAll('button');
            for (let button of buttons) {{
                if (button.innerText.includes('Mute') || button.innerText.includes('Unmute')) {{
                    button.innerText = '{mute_icon} {mute_text}';
                }}
            }}
            if (window.streamlitAudio) {{
                window.streamlitAudio.muted = {str(mute_state).lower()};
            }}
        }});
    </script>
    """, unsafe_allow_html=True)
    
    components.html(html_content, height=750, scrolling=True)
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
