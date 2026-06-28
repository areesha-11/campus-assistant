import streamlit as st
from chatbot import ask_question

st.set_page_config(page_title="UCER Campus Assistant", page_icon="🎓")

st.title("🎓 UCER Campus Assistant")
st.caption("Ask me about fees, exam rules, hostel, bus registration, syllabus, and more")

# Stores both what's shown on screen AND the raw history used for memory
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_question = st.chat_input("Ask a question about UCER...")

if user_question:
    with st.chat_message("user"):
        st.markdown(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.spinner("Searching documents..."):
        # Pass the conversation history so far, so follow-ups work correctly
        answer, sources = ask_question(user_question, st.session_state.chat_history)

    with st.chat_message("assistant"):
        st.markdown(answer)
        with st.expander("Sources used"):
            for doc in sources:
                source_name = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "?")
                st.write(f"- {source_name}, page {page}")

    st.session_state.messages.append({"role": "assistant", "content": answer})

    # Save this turn into history for future follow-up questions
    st.session_state.chat_history.append((user_question, answer))