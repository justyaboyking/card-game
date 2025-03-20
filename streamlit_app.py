import streamlit as st
import os
import base64
import tempfile
from PyPDF2 import PdfReader
from PIL import Image
import io

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
    .pdf-page {
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-radius: 5px;
        overflow: hidden;
    }
    .page-number {
        background-color: #f0f2f6;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
        margin-bottom: 5px;
        display: inline-block;
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

# Function to extract images from PDF
def extract_images_from_pdf(pdf_file):
    pdf_pages = {}
    
    # Create a temporary file to save the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(pdf_file.read())
        pdf_path = tmp_file.name
    
    # Open the PDF with PyPDF2
    with open(pdf_path, 'rb') as f:
        pdf = PdfReader(f)
        for i, page in enumerate(pdf.pages):
            page_number = i + 1
            # Convert the page to an image
            # For simplicity, we'll just store the PDF page itself
            pdf_pages[page_number] = page
    
    # Remove the temporary file
    os.unlink(pdf_path)
    
    return pdf_pages

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'pdf_pages' not in st.session_state:
    st.session_state.pdf_pages = None

if 'current_page' not in st.session_state:
    st.session_state.current_page = None

# Main layout with two columns
col1, col2 = st.columns([2, 3])

with col1:
    st.header("Wiskunde Pagina's")
    
    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload je wiskunde PDF", type="pdf")
    
    if uploaded_file is not None:
        # Extract pages from PDF
        if st.session_state.pdf_pages is None:
            with st.spinner('PDF verwerken...'):
                st.session_state.pdf_pages = extract_images_from_pdf(uploaded_file)
            st.success(f"{len(st.session_state.pdf_pages)} pagina's geëxtraheerd!")
        
        # Page selector
        page_numbers = list(st.session_state.pdf_pages.keys())
        selected_page = st.selectbox(
            "Selecteer een pagina",
            page_numbers,
            index=0 if not st.session_state.current_page else page_numbers.index(st.session_state.current_page)
        )
        
        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page
        
        # Display the selected page
        if st.session_state.current_page:
            st.markdown(f"<div class='page-number'>Pagina {st.session_state.current_page}</div>", unsafe_allow_html=True)
            
            # Convert PDF page to image and display
            page = st.session_state.pdf_pages[st.session_state.current_page]
            
            # For demonstration, we're just showing a placeholder
            # In a full implementation, you'd convert PDF page to image
            st.markdown(f"<div class='pdf-page'>PDF pagina {st.session_state.current_page} inhoud</div>", unsafe_allow_html=True)

with col2:
    st.header("Wiskunde Huiswerk Helper")
    
    # Display intro message
    if not st.session_state.messages:
        st.info("Upload je wiskunde PDF en selecteer een pagina om te beginnen. De AI zal je helpen met het oplossen van de opgaven.")
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ai-message'>{message['content']}</div>", unsafe_allow_html=True)
    
    # Input for user questions
    user_input = st.text_input("Stel je vraag of typ 'start' om te beginnen met de huidige pagina", key="user_input")
    
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Process and respond based on the AI prompt
        if user_input.lower() == "start" and st.session_state.current_page:
            ai_response = f"Ik ga je helpen met de opgaven op pagina {st.session_state.current_page}. Welke opgave wil je behandelen?"
        elif user_input.lower().startswith("pagina"):
            # Extract page number from input
            try:
                page_num = int(user_input.lower().replace("pagina", "").strip())
                if page_num in st.session_state.pdf_pages:
                    st.session_state.current_page = page_num
                    ai_response = f"Ik heb pagina {page_num} geopend. Welke opgave wil je behandelen?"
                else:
                    ai_response = f"Pagina {page_num} is niet beschikbaar in de geüploade PDF."
            except:
                ai_response = "Ik kon het paginanummer niet herkennen. Probeer bijvoorbeeld 'pagina 210'."
        else:
            # This is where the actual AI response would be generated based on the prompt
            # For this implementation, we'll simulate a response
            if st.session_state.current_page:
                ai_response = f"Hier is mijn uitleg voor je vraag over pagina {st.session_state.current_page}:\n\n"
                ai_response += "Voor deze opdracht moet je het lineaire verband tussen de gegeven variabelen vinden. "
                ai_response += "De formule heeft de vorm y = ax + b, waarbij we a en b moeten bepalen uit de gegeven data."
            else:
                ai_response = "Upload eerst een PDF en selecteer een pagina om te beginnen."
        
        # Add AI response to chat
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Rerun to update the UI
        st.experimental_rerun()

# Add the AI prompt reference
with st.sidebar:
    st.header("AI Prompt Referentie")
    
    # Display the prompt that the AI would use
    st.markdown("""
    ### Wiskunde Huiswerk Helper Prompt
    
    De AI gebruikt de volgende instructies om je te helpen:
    
    1. Identificeer de specifieke opdrachten op de geselecteerde pagina
    2. Voor elke opdracht:
       - Leest de vraag zorgvuldig
       - Geeft een volledige, stapsgewijze oplossing
       - Legt de wiskundige concepten duidelijk uit
       - Toont alle berekeningen
       - Presenteert het antwoord in de juiste vorm
    
    3. De AI is getraind om te werken met:
       - Lineaire verbanden
       - Formules en vergelijkingen
       - Grafieken interpreteren en opstellen
       - Tabellen invullen
       - Toepassingsproblemen (kosten, tijd, afstand, etc.)
       - Stijgende, dalende of constante verbanden
    
    Om te beginnen, selecteer een pagina en typ 'start' in het tekstvak.
    """)
