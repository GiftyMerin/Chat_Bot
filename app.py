import streamlit as st
from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Load environment variables from .env
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖",
    layout="centered",
)

# Initialize the model once
@st.cache_resource
def get_llm():
    return ChatOpenRouter(
        model="openrouter/free",
        temperature=0.7,
        max_tokens=500,
    )

llm = get_llm()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("Settings")
    st.caption("Powered by LangChain + OpenRouter")

    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main interface
st.title("🤖 My AI Chatbot")
st.caption("Ask me anything. I'm here to help!")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input at the bottom
if prompt := st.chat_input("Type your message here..."):

    # Display and store the user's message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Build conversation history for LangChain
    history = [SystemMessage(
        content="You are a helpful AI assistant. "
                "Answer clearly and concisely."
    )]

    for message in st.session_state.messages:
        if message["role"] == "user":
            history.append(HumanMessage(content=message["content"]))
        else:
            history.append(AIMessage(content=message["content"]))

    # Generate the response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = llm.invoke(history)
                answer = str(response.content)

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                })

            except Exception as e:
                st.error(f"Something went wrong: {e}")