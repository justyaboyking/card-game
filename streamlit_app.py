import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Card Bluff Roulette",
    page_icon="🃏",
    layout="wide"
)

st.title("Card Bluff Roulette with Mine Challenge")

# Read the HTML file
with open("game tst.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Display the HTML content using a custom component
components.html(html_content, height=800, scrolling=False)

# Add some information below the game
st.markdown("---")
st.markdown("### How to Play")
st.markdown("""
- Each player gets 10 cards and there's one center card.
- The active player selects cards from their hand and clicks "Ready".
- The opponent then guesses if the selected cards match the center card's suit.
- If the guess is wrong, the guessing player faces the Mine Challenge.
- Each player starts with their own set of 6 diamonds for the Mine Challenge.
- If you click a safe diamond, it is removed from your set and the round immediately ends as safe.
- If you click the lose diamond, you lose the game and return to the start screen.
- You also win if you empty your hand of cards.
""")