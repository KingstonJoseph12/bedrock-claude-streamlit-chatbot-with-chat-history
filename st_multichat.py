import streamlit as st
import boto3
import json
import base64
from PIL import Image
import io
import pickle
import os
from datetime import datetime

# Initialize Bedrock client
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# Function to get response from Claude (unchanged)
def get_claude_response(prompt, chat_history, images=None):
    messages = chat_history + [{"role": "user", "content": [{"type": "text", "text": prompt}]}]

    if images:
        for image in images:
            # Convert image to base64
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # Add image to the last message
            messages[-1]["content"].append(
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_str}}
            )

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 10000,
            "messages": messages
        })
    )
    return json.loads(response['body'].read())['content'][0]['text']

# Function to save chat sessions
def save_sessions(sessions):
    with open('chat_sessions.pkl', 'wb') as f:
        pickle.dump(sessions, f)

# Function to load chat sessions
def load_sessions():
    if os.path.exists('chat_sessions.pkl'):
        with open('chat_sessions.pkl', 'rb') as f:
            return pickle.load(f)
    return {}

# Streamlit app
st.title("Claude 3.5 Sonnet Multimodal Chatbot")

# Initialize or load chat sessions
if "sessions" not in st.session_state:
    st.session_state.sessions = load_sessions()

# Navigation bar
st.sidebar.title("Chat Sessions")
session_name = st.sidebar.selectbox("Select a session", list(st.session_state.sessions.keys()) + ["New Session"])

if session_name == "New Session":
    new_session_name = st.sidebar.text_input("Enter a name for the new session")
    if st.sidebar.button("Create Session") and new_session_name:
        st.session_state.sessions[new_session_name] = []
        session_name = new_session_name
        save_sessions(st.session_state.sessions)

# Use the selected session
if session_name and session_name != "New Session":
    st.session_state.current_session = st.session_state.sessions[session_name]
else:
    st.session_state.current_session = []

# Display chat messages from history on app rerun
for message in st.session_state.current_session:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], str):
            st.markdown(message["content"])
        elif isinstance(message["content"], tuple):
            for img in message["content"][0]:
                st.image(img)
            st.markdown(message["content"][1])

# Image upload
uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
images = []
if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        images.append(image)
        st.image(image, caption=f'Uploaded Image: {uploaded_file.name}', use_column_width=True)

# React to user input
if prompt := st.chat_input("What is your question?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    if images:
        st.session_state.current_session.append({"role": "user", "content": (images, prompt)})
    else:
        st.session_state.current_session.append({"role": "user", "content": prompt})

    # Prepare chat history for Claude
    claude_chat_history = [
        {"role": msg["role"], "content": [{"type": "text", "text": msg["content"]}] if isinstance(msg["content"], str) else [{"type": "text", "text": msg["content"][1]}]}
        for msg in st.session_state.current_session[:-1]
    ]

    # Get Claude's response
    response = get_claude_response(prompt, claude_chat_history, images if images else None)

    # Display Claude's response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add Claude's response to chat history
    st.session_state.current_session.append({"role": "assistant", "content": response})

    # Save the updated session
    st.session_state.sessions[session_name] = st.session_state.current_session
    save_sessions(st.session_state.sessions)

# Add a sidebar with information
st.sidebar.title("About")
st.sidebar.info("This is a multimodal chatbot powered by Claude 3.5 Sonnet via Amazon Bedrock. You can ask questions about text and uploaded images!")

# Optional: Add a clear chat button
if st.sidebar.button("Clear Current Chat"):
    st.session_state.current_session = []
    st.session_state.sessions[session_name] = []
    save_sessions(st.session_state.sessions)

# Optional: Add a delete session button
if st.sidebar.button("Delete Current Session"):
    if session_name in st.session_state.sessions:
        del st.session_state.sessions[session_name]
        save_sessions(st.session_state.sessions)
        st.experimental_rerun()
