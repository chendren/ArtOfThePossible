import streamlit as st
import requests
import logging
import json

# Set up logging to capture detailed information
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Set your Mistral API key
api_key = "7AvIUIUqGziAHsZ2nY0RzFRAA3612qNA"
model = "mistral-large-latest"
api_url = "https://api.mistral.ai/v1/chat/completions"  # Replace with the actual API endpoint if different

# Function to interact with the Mistral bot API
def get_bot_response(user_input):
    """
    Sends a request to the Mistral bot API and returns the bot's response.

    Parameters:
    user_input (str): The user's input message.

    Returns:
    str: The bot's response or an error message.
    """
    # Prepare the message for the chatbot
    messages = [
        {
            "role": "user",
            "content": user_input,
        },
    ]

    # Prepare the request payload
    payload = {
        "model": model,
        "messages": messages
    }

    # Set the headers with the API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        # Log the payload for debugging purposes
        logging.info(f"Sending request to {api_url} with payload {json.dumps(payload)}")

        # Make the API request
        response = requests.post(api_url, json=payload, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            response_content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
            logging.info(f"Received response: {response_content}")
            return response_content
        else:
            logging.error(f"API request failed with status code {response.status_code}: {response.text}")
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        # Log any errors that occur during the request
        logging.error(f"API request failed: {e}")
        return "Sorry, I couldn't process your request at the moment. Please try again later."

# Streamlit app layout
st.title("Chat with Mistral Large Bot")

# Initialize the conversation history in the session state if it doesn't exist
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# User input box for entering messages
user_input_placeholder = st.empty()
user_input = user_input_placeholder.text_input("You:", key="user_input_initial")

# Button to send the message to the bot
if st.button("Send"):
    if user_input:
        # Append the user's input to the conversation history
        st.session_state.conversation_history.append(f"You: {user_input}")

        # Show loading spinner while processing the request
        with st.spinner('Processing your request...'):
            # Get the bot's response
            bot_response = get_bot_response(user_input)

        # Append the bot's response to the conversation history
        st.session_state.conversation_history.append(f"Bot: {bot_response}")

        # Clear the input box after sending the message
        user_input_placeholder.text_input("You:", key="user_input_cleared", value="")

# Button to clear the conversation history
if st.button("Clear Conversation"):
    st.session_state.conversation_history = []

# Display the conversation history
for message in st.session_state.conversation_history:
    st.write(message)

# Save and load conversation history
st.sidebar.title("Conversation History")

if st.sidebar.button("Save Conversation"):
    try:
        with open("conversation_history.txt", "w") as f:
            for message in st.session_state.conversation_history:
                f.write(message + "\n")
        st.sidebar.success("Conversation saved successfully!")
    except Exception as e:
        logging.error(f"Error saving conversation: {e}")
        st.sidebar.error("Error saving conversation. Please check the logs for more details.")

if st.sidebar.button("Load Conversation"):
    try:
        with open("conversation_history.txt", "r") as f:
            st.session_state.conversation_history = [line.strip() for line in f.readlines()]
        st.sidebar.success("Conversation loaded successfully!")
    except FileNotFoundError:
        st.sidebar.error("No saved conversation found.")
    except Exception as e:
        logging.error(f"Error loading conversation: {e}")
        st.sidebar.error("Error loading conversation. Please check the logs for more details.")
