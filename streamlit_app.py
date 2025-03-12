import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(
    page_title="Card Bluff Roulette",
    page_icon="🃏",
    layout="wide"
)

# Remove the title since it's already in the game
# st.title("Card Bluff Roulette with Mine Challenge")

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(current_dir, "game tst.html")

# Read the HTML file with error handling
try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Display the HTML content using a custom component
    # Increase height to show the full game
    components.html(html_content, height=900, scrolling=False)
    
except FileNotFoundError:
    st.error(f"Could not find the game file at {html_file_path}")
    st.info("Make sure 'game tst.html' is in the same directory as this script.")
    
except Exception as e:
    st.error(f"An error occurred: {str(e)}")

# Remove the duplicate instructions section
# st.markdown("---")
# st.markdown("### How to Play")
# st.markdown("""
# - Each player gets 10 cards and there's one center card.
# - The active player selects cards from their hand and clicks "Ready".
# - The opponent then guesses if the selected cards match the center card's suit.
# - If the guess is wrong, the guessing player faces the Mine Challenge.
# - Each player starts with their own set of 6 diamonds for the Mine Challenge.
# - If you click a safe diamond, it is removed from your set and the round immediately ends as safe.
# - If you click the lose diamond, you lose the game and return to the start screen.
# - You also win if you empty your hand of cards.
# """)
