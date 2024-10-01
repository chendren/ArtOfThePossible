import os
import gradio as gr
import requests

# Set your Mistral API key
api_key = "YOUR KEY GOES HERE"
model = "mistral-large-latest"
api_url = "https://api.mistral.ai/v1/chat/completions"  # Replace with the actual API endpoint if different

def chatbot_response(user_input):
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

    # Make the API request
    response = requests.post(api_url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        response_content = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return response_content
    else:
        return f"Error: {response.status_code} - {response.text}"

# Create the Gradio interface
iface = gr.Interface(
    fn=chatbot_response,
    inputs="text",
    outputs="text",
    title="Mistral Chatbot",
    description="Ask the chatbot anything!"
)

# Launch the Gradio app
iface.launch()
