import streamlit as st
from pathlib import Path
from core import ChatInput
from agents.chat_agent import ChatAgent


st.set_page_config(page_title="Chat Agent UI", page_icon="🤖", layout="wide")

@st.cache_resource
def get_agent():
    return ChatAgent(env_path=Path(".env"))

agent = get_agent()

st.sidebar.title("⚙️ Chat Settings")

intent = st.sidebar.selectbox(
    "Intent",
    ["general", "search", "summarize", "analyze", "recommend"],
    index=0
)

filters = {}
with st.sidebar.expander("🔍 Filters"):
    year = st.text_input("Year Filter", value="")
    if year:
        filters["year"] = year

user_preferences = {}
with st.sidebar.expander("👤 User Preferences"):
    summary_length = st.selectbox("Summary Length", ["short", "medium", "long"], index=0)
    user_preferences["summary_length"] = summary_length

st.title("🤖 Chat Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask something..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    chat_input = ChatInput(
        query_text=prompt,
        context=[m["content"] for m in st.session_state.messages if m["role"] == "user"],
        intent=intent,
        filters=filters,
        user_preferences=user_preferences,
        documents=[]
    )

    with st.spinner("Thinking..."):
        response = agent.run(chat_input=chat_input)

    reply = response["raw_output"]

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

st.markdown("---")
