import streamlit as st
import os

# Set full page width and remove padding
st.set_page_config(
    page_title="Wiskunde Huiswerk Helper",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS to improve layout
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    .stApp {
        background-color: #f5f7f9;
    }
    /* Chat styling */
    .user-message {
        background-color: #e1f5fe;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin: 10px 0;
    }
    .ai-message {
        background-color: #f0f2f6;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'current_page' not in st.session_state:
    st.session_state.current_page = None

# Title
st.title("Wiskunde Huiswerk Helper")

# Page selector in the sidebar
with st.sidebar:
    st.header("Pagina Selectie")
    
    # Page range for the workbook
    page_range = list(range(208, 222))  # Pages 208-221
    
    selected_page = st.selectbox(
        "Selecteer een pagina om te bestuderen",
        page_range,
        index=0 if not st.session_state.current_page else page_range.index(st.session_state.current_page)
    )
    
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        # Add a system message when page changes
        st.session_state.messages.append({
            "role": "assistant", 
            "content": f"Je hebt pagina {selected_page} geselecteerd. Welke opgave wil je behandelen?"
        })
    
    st.markdown("---")
    
    st.markdown("""
    ### Wiskunde Onderwerpen
    
    De helper kan je assisteren met:
    - Lineaire verbanden
    - Formules en vergelijkingen
    - Grafieken interpreteren
    - Tabellen invullen
    - Toepassingsproblemen
    - Stijgende/dalende verbanden
    """)

# Main chat interface
st.header(f"Wiskunde Opgaven - Pagina {st.session_state.current_page}")

# Display intro message if no messages yet
if not st.session_state.messages:
    st.info("Selecteer een pagina in het linkermenu en stel je vraag over een specifieke opgave. De AI zal je helpen met stapsgewijze uitleg.")
    # Add initial message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Welke pagina('s) van je wiskunde werkboek wil je behandelen? (pagina 208-221)"
    })

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='ai-message'>{message['content']}</div>", unsafe_allow_html=True)

# Input for user questions
user_input = st.text_input("Stel je vraag of geef een opdrachtnummer op", key="user_input")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Process and respond based on the user input
    if user_input.lower().startswith("pagina"):
        # Extract page number from input
        try:
            page_num = int(user_input.lower().replace("pagina", "").strip())
            if 208 <= page_num <= 221:
                st.session_state.current_page = page_num
                ai_response = f"Ik help je nu met pagina {page_num}. Welke opgave wil je behandelen?"
            else:
                ai_response = f"Pagina {page_num} ligt buiten het bereik van dit werkboek (pagina 208-221)."
        except:
            ai_response = "Ik kon het paginanummer niet herkennen. Probeer bijvoorbeeld 'pagina 210'."
    
    # Check if input is just a number (opgave number)
    elif user_input.isdigit():
        exercise_num = int(user_input)
        ai_response = f"Ik ga je helpen met opgave {exercise_num} op pagina {st.session_state.current_page}. "
        ai_response += "Laten we deze stap voor stap aanpakken. Wat is de specifieke vraag bij deze opgave?"
    
    # Check if input asks for a specific sub-question (e.g., "12a" or "opgave 14b")
    elif any(char.isdigit() for char in user_input) and any(char.isalpha() for char in user_input):
        # Simple extraction of numbers and letters - this could be improved
        exercise_parts = ''.join(c for c in user_input if c.isdigit() or c.isalpha())
        ai_response = f"Ik ga je helpen met opgave {exercise_parts} op pagina {st.session_state.current_page}. "
        ai_response += "Laten we deze stap voor stap analyseren op basis van het werkboek."
        
    # General responses based on keywords
    elif "formule" in user_input.lower():
        ai_response = "Om de juiste formule te vinden, moeten we eerst bepalen welk type verband we hebben. "
        ai_response += "Bij een lineair verband gebruiken we y = ax + b, waar a de richtingscoëfficiënt is en b het snijpunt met de y-as."
    
    elif "tabel" in user_input.lower():
        ai_response = "Om een tabel in te vullen bij een lineair verband, beginnen we met het identificeren van de formule. "
        ai_response += "Daarna vullen we systematisch de waarden in door voor elke x-waarde de bijbehorende y-waarde te berekenen."
    
    elif "grafiek" in user_input.lower():
        ai_response = "Voor het analyseren van een grafiek kijken we naar de vorm. "
        ai_response += "Een rechte lijn duidt op een lineair verband, waarbij de helling aangeeft of het een stijgend of dalend verband is."
    
    # Default response
    else:
        ai_response = f"Ik kan je helpen met de opgaven op pagina {st.session_state.current_page}. "
        ai_response += "Geef aan welke specifieke opgave je wilt behandelen, bijvoorbeeld '12a' of 'opgave 3b'."
    
    # Add AI response to chat
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    # Rerun to update the UI
    st.experimental_rerun()

# Footer info
st.markdown("---")
st.info("Deze app helpt je met het oplossen van wiskundeopgaven uit je werkboek. Voor het beste resultaat, geef de exacte opgave of deelvraag op.")
