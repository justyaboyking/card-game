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

# Simplified function to play audio in the background
def autoplay_audio(file_url, audio_id="streamlit_audio"):
    audio_html = f"""
        <div id="audio-container" style="text-align: center; margin: 10px 0;">
            <button id="manual-play-button" style="background: linear-gradient(135deg, #00b4d8, #0096c7); color: white; border: none; border-radius: 30px; padding: 10px 20px; font-size: 16px; cursor: pointer; margin: 5px;">
                🎵 Play Background Music
            </button>
        </div>
        <audio id="{audio_id}" loop style="display:none;">
            <source src="{file_url}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        <script>
            document.addEventListener('DOMContentLoaded', function() {{  
                const audio = document.getElementById('{audio_id}');
                const playButton = document.getElementById('manual-play-button');
                
                // Make audio element accessible globally for mute button
                window.streamlitAudio = audio;
                
                // Setup play button - always require manual interaction
                if (playButton) {{
                    playButton.addEventListener('click', function() {{
                        if (audio) {{
                            audio.volume = 0.5;
                            audio.play()
                                .then(() => {{
                                    playButton.textContent = '🎵 Music Playing';
                                    setTimeout(() => {{
                                        document.getElementById('audio-container').style.display = 'none';
                                    }}, 3000);
                                }})
                                .catch(e => {{
                                    console.error('Play failed:', e);
                                    playButton.textContent = '🎵 Try Again';
                                }});
                        }}
                    }});
                }}
            }});
        </script>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

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
        height: 88vh;
        border: none;
    }
    /* Hide audio controls when not active */
    .audio-player {
        margin-bottom: 10px;
    }
    /* Make audio player look nicer */
    audio {
        border-radius: 30px;
        background-color: rgba(0, 180, 216, 0.1);
    }
    /* Hide Streamlit elements we don't need */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Set the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Autoplay background music (hidden)
# Convert local audio file to base64 for embedding
def get_base64_audio(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            if len(data) < 1000:  # Check if file is too small (likely invalid)
                st.warning(f"The audio file at {file_path} appears to be invalid or too small ({len(data)} bytes). Please replace it with a valid MP3 file.")
                return None
            encoded_data = base64.b64encode(data).decode()
            return encoded_data
    except Exception as e:
        st.error(f"Error loading audio file: {str(e)}")
        return None

# Simplified audio loading - try to use one of the available audio files
shadows_shuffle_path = os.path.join(current_dir, "Shadows Shuffle.mp3")
music_file_path = os.path.join(current_dir, "background_music.mp3")

# Try to load one of the audio files
audio_url = None

# First try Shadows Shuffle.mp3
if os.path.exists(shadows_shuffle_path) and os.path.getsize(shadows_shuffle_path) > 1000:
    audio_base64 = get_base64_audio(shadows_shuffle_path)
    if audio_base64:
        audio_url = f"data:audio/mp3;base64,{audio_base64}"

# If that didn't work, try background_music.mp3
if not audio_url and os.path.exists(music_file_path) and os.path.getsize(music_file_path) > 1000:
    audio_base64 = get_base64_audio(music_file_path)
    if audio_base64:
        audio_url = f"data:audio/mp3;base64,{audio_base64}"

# Play the audio if we found a valid file
if audio_url:
    autoplay_audio(audio_url)
else:
    st.error("Could not load any audio files. Please ensure valid MP3 files are available in the application directory.")

# Set the HTML file path (current_dir is already defined above)
html_file_path = os.path.join(current_dir, "game tst.html")

# Read the HTML file with error handling
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Remove audio element completely
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
    
    # Add main menu options and mute button
    st.session_state.active_tab = st.session_state.get('active_tab', 'game')

    # Create tabs for main menu options
    col1, col2, col3, col4, col5 = st.columns([3, 3, 3, 3, 1])

    with col1:
        if st.button("🎮 Play Game", key="play_game", use_container_width=True):
            st.session_state.active_tab = 'game'
            st.rerun()

    with col2:
        if st.button("⚙️ Settings", key="settings", use_container_width=True):
            st.session_state.active_tab = 'settings'
            st.rerun()

    with col3:
        if st.button("📋 Rules", key="rules", use_container_width=True):
            st.session_state.active_tab = 'rules'
            st.rerun()
            
    with col4:
        if st.button("ℹ️ About", key="about", use_container_width=True):
            st.session_state.active_tab = 'about'
            st.rerun()

    with col5:
        if st.button("🔊 Mute", key="mute_button"):
            # This doesn't directly control audio - we use JavaScript for that
            st.session_state.muted = not st.session_state.get('muted', False)
            st.rerun()
    
    # JavaScript to control audio muting - simplified version
    mute_state = st.session_state.get('muted', False)
    mute_icon = "🔇" if mute_state else "🔊"
    mute_text = "Unmute" if mute_state else "Mute"
    
    # Update button text and control audio
    st.markdown(f"""
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            // Update mute button text
            const buttons = document.querySelectorAll('button');
            for (let button of buttons) {{
                if (button.innerText.includes('Mute') || button.innerText.includes('Unmute')) {{
                    button.innerText = '{mute_icon} {mute_text}';
                }}
            }}
            
            // Set audio muted state if audio element exists
            if (window.streamlitAudio) {{
                window.streamlitAudio.muted = {str(mute_state).lower()};
                console.log('Audio mute state set to: {str(mute_state).lower()}');
            }}
        }});
    </script>
    """, unsafe_allow_html=True)
    
    # Display content based on active tab
    if st.session_state.active_tab == 'game':
        # Display the game HTML content
        components.html(html_content, height=750, scrolling=True)
    
    elif st.session_state.active_tab == 'settings':
        st.markdown("""<h2 style='color:#00b4d8;'>Game Settings</h2>""", unsafe_allow_html=True)
        st.markdown("""<div style='background-color:rgba(255,255,255,0.05);border-radius:16px;padding:20px;'>""", unsafe_allow_html=True)
        
        # Player names
        col1, col2 = st.columns(2)
        with col1:
            player1 = st.text_input("Player 1 Name", value="Player 1")
        with col2:
            player2 = st.text_input("Player 2 Name", value="Player 2")
        
        # Max cards selection
        max_cards = st.slider("Maximum Cards to Select", min_value=1, max_value=10, value=10)
        
        # Apply settings button
        if st.button("Apply Settings", key="apply_settings"):
            # Add JavaScript to update the game's settings
            st.markdown(f"""
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    // Set values in the game's input fields
                    if (document.getElementById('player1Name')) {{
                        document.getElementById('player1Name').value = "{player1}";
                    }}
                    if (document.getElementById('player2Name')) {{
                        document.getElementById('player2Name').value = "{player2}";
                    }}
                    if (document.getElementById('maxCards')) {{
                        document.getElementById('maxCards').value = {max_cards};
                    }}
                }});
            </script>
            """, unsafe_allow_html=True)
            st.success("Settings applied! Return to the game to start playing.")
        
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    elif st.session_state.active_tab == 'rules':
        st.markdown("""<h2 style='color:#00b4d8;'>How to Play</h2>""", unsafe_allow_html=True)
        st.markdown("""<div style='background-color:rgba(255,255,255,0.05);border-radius:16px;padding:20px;'>""", unsafe_allow_html=True)
        
        st.markdown("""
        ### Card Bluff Roulette Rules
        
        #### Basic Gameplay:
        1. Each player gets 10 cards and there's one center card.
        2. The active player selects cards from their hand and clicks "Ready".
        3. The opponent then guesses if the selected cards match the center card's suit.
        4. If the active player bluffs (claims match when they don't) and is caught, they get random cards equal to the number they played.
        5. If the guess is wrong, the guessing player faces the Mine Challenge.
        
        #### Mine Challenge:
        - Each player starts with their own set of 6 diamonds.
        - If you click a safe diamond, it is removed from your set and the round immediately ends as safe.
        - If you click the lose diamond, you lose the game and return to the start screen.
        
        #### Winning the Game:
        - You win if you empty your hand of cards.
        - You win if your opponent clicks the lose diamond during their Mine Challenge.
        """)
        
        st.markdown("""</div>""", unsafe_allow_html=True)
    
    elif st.session_state.active_tab == 'about':
        st.markdown("""<h2 style='color:#00b4d8;'>About Card Bluff Roulette</h2>""", unsafe_allow_html=True)
        st.markdown("""<div style='background-color:rgba(255,255,255,0.05);border-radius:16px;padding:20px;'>""", unsafe_allow_html=True)
        
        st.markdown("""
        ### Card Bluff Roulette with Mine Challenge
        
        This game combines elements of card bluffing with a diamond mine challenge for an exciting twist on traditional card games.
        
        #### Features:
        - Beautiful card animations and visual effects
        - Engaging gameplay that combines strategy and luck
        - Background music to enhance the gaming experience
        - Customizable player names and game settings
        
        #### How to Use This App:
        - Use the menu buttons at the top to navigate between different sections
        - Click on "Play Game" to start playing
        - Adjust your preferences in the "Settings" section
        - Learn how to play in the "Rules" section
        
        Enjoy the game!
        """)
        
        st.markdown("""</div>""", unsafe_allow_html=True)
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
