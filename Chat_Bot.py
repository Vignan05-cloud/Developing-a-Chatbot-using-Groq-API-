import streamlit as st
import openai  # Import OpenAI library
from SECRET_KEY import GROQ_API_KEY as Api

# Set up OpenAI client for Groq API
client = openai.OpenAI(
    api_key= Api,  # Replace with your actual Groq API Key
    base_url="https://api.groq.com/openai/v1"  # Set Groq API base
)

# Streamlit UI
st.title("🤖 Groq Chatbot using OpenAI Library (v1.0+)")
st.markdown("Chat with an AI model powered by Groq API using OpenAI's latest library!")

# Clear Chat Button
if st.button("🗑 Clear Chat"):
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
    st.session_state.total_input_tokens = 0
    st.session_state.total_output_tokens = 0
    st.rerun()  # Refresh UI

# Initialize chat history & token counters
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
if "total_input_tokens" not in st.session_state:
    st.session_state.total_input_tokens = 0
if "total_output_tokens" not in st.session_state:
    st.session_state.total_output_tokens = 0

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":  # Do not display system message
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User Input
user_input = st.chat_input("Ask me anything...")
if user_input:
    # Append user message to session
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call Groq API using OpenAI's latest client format
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Use a supported Groq model
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=200,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        # Get AI response
        ai_response = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens

        # Update token count
        st.session_state.total_input_tokens += input_tokens
        st.session_state.total_output_tokens += output_tokens

        # Append assistant response
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.markdown(ai_response)

    except openai.OpenAIError as e:
        st.error(f"API Error: {e}")  # Show API errors

# Display Token Usage
st.sidebar.subheader("📊 Token Usage")
st.sidebar.write(f"🔹 *Total Input Tokens:* {st.session_state.total_input_tokens}")
st.sidebar.write(f"🔹 *Total Output Tokens:* {st.session_state.total_output_tokens}")