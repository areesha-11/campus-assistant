import streamlit as st
from chatbot import ask_question

st.set_page_config(page_title="UCER Campus Assistant", page_icon="🎓")

# ---- Sidebar ----
with st.sidebar:
    st.title("About")
    st.write("**UCER Campus Assistant**")
    st.write("AI-powered chatbot using RAG technology")
    st.write("**Knowledge base:**")
    st.write("- 10 UCER/AKTU documents")
    st.write("- 103 pages")
    st.write("- 363 searchable chunks")
    st.write("**Tech stack:**")
    st.write("- LangChain + ChromaDB")
    st.write("- Google Gemini API")
    st.write("- Streamlit")

    st.divider()

    # Clear chat button
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# ---- Main UI ----
st.title("🎓 UCER Campus Assistant")
st.caption("Ask me about fees, exam rules, hostel, bus registration, syllabus, and more")

# Example questions hint
st.info("💡 Try asking: 'What is the hostel fee?' or 'What subjects are in semester 5?' or 'What is the bus fee?'")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_question = st.chat_input("Ask a question about UCER...")

if user_question:
    # Show user question
    with st.chat_message("user"):
        st.markdown(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    # Get answer from backend
    with st.spinner("Searching documents..."):
        answer, sources = ask_question(user_question, st.session_state.chat_history)

    # Show assistant answer
    with st.chat_message("assistant"):
        st.markdown(answer)
        with st.expander("Sources used"):
            for doc in sources:
                source_name = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "?")
                st.write(f"- {source_name}, page {page}")

    st.session_state.messages.append({"role": "assistant", "content": answer})

    # Save to chat history for memory
    st.session_state.chat_history.append((user_question, answer))