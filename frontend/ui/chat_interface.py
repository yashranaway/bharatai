import streamlit as st
from datetime import datetime
import json
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the NLP service
from ai.nlp_service import nlp_service

def chat_interface():
    # Create a container for the chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                st.caption(f"{message['timestamp']}")
        
        # Spacer to push input to bottom
        st.write("")
        st.write("")
        st.write("")
    
    # Fixed input area at the bottom
    with st.container():
        # Create a form for the chat input
        with st.form("chat_form", clear_on_submit=True):
            # Use columns to align the input and button
            col1, col2 = st.columns([4, 1])
            
            with col1:
                user_input = st.text_input(
                    "Type your message about Kirana store operations...",
                    label_visibility="collapsed",
                    placeholder="Type your message about Kirana store operations..."
                )
            
            with col2:
                submit_button = st.form_submit_button("Send 📤")
            
            # Process the input when submitted
            if submit_button and user_input:
                process_and_respond(user_input)

def process_and_respond(user_input):
    """
    Process user input and generate response
    """
    # Add user message to chat history
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user", 
        "content": user_input,
        "timestamp": timestamp
    })
    
    # Process the user input with NLP and generate response
    response = nlp_service.generate_response(user_input)
    bot_timestamp = datetime.now().strftime("%H:%M")
    
    # Add bot response to chat history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response,
        "timestamp": bot_timestamp
    })
    
    # Rerun to update the UI
    st.rerun()