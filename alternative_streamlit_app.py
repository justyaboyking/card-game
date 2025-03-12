import streamlit as st

st.set_page_config(
    page_title="Card Bluff Roulette",
    page_icon="🃏"
)

st.title("Card Bluff Roulette with Mine Challenge")

st.markdown("""
## Play the Game
Click the button below to play the game in a new tab:
""")

# Replace with your actual GitHub Pages URL once deployed
github_pages_url = "https://yourusername.github.io/your-repo-name/"
st.markdown(f"[Play Card Bluff Roulette]({github_pages_url})")

st.markdown("---")
st.markdown("### How to Play")
# Game instructions here

## Step 4: Push Everything to GitHub

1. Make sure you have these files in your repository:
   - `game tst.html` (your game file)
   - `streamlit_app.py` (the Streamlit wrapper)
   - `requirements.txt` (dependencies)

2. Push these files to your GitHub repository

## Step 5: Deploy on Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch, and the main file (`streamlit_app.py`)
5. Click "Deploy"

Streamlit Cloud will automatically install the dependencies from your requirements.txt file and run your app.

## Alternative Approach

If you encounter issues with the HTML component in Streamlit, you could also:

1. Convert your game to a pure JavaScript/HTML application
2. Deploy it on GitHub Pages
3. Create a Streamlit app that simply links to your GitHub Pages URL

This would be a simpler approach if you're having trouble with the HTML component in Streamlit.