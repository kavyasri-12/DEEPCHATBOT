import streamlit as st
from groq import Groq
from datetime import datetime


API_KEY = "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"

st.set_page_config(
    page_title="DeepSeek R1 Chatbot",
    layout="centered"
)

with st.sidebar:
    st.title("Chatbot settings")
    st.markdown("**Using pre-configured API key**") 

    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.slider("Max Tokens", 100, 4096, 1024)
    top_p = st.slider("Top-P", 0.0, 1.0, 1.0)
    frequency_penalty = st.slider("Frequency Penalty", 0.0, 1.0, 0.0)

st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        st.caption(f"_{message['timestamp']}_")

if prompt := st.chat_input("How can I help you?"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        st.caption(f"_{timestamp}_")

    try:
        client = Groq(api_key=API_KEY)
        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            stream=False
        )

        ai_response = response.choices[0].message.content
        timestamp = datetime.now().strftime("%H:%M:%S")

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": timestamp
        })

        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(ai_response)
            st.caption(f"_{timestamp}_")

    except Exception as e:
        st.error(f"Error generating response: {str(e)}")

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
