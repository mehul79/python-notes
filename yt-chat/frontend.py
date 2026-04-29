import streamlit as st

# ---------------------------
# Session State Initialization
# ---------------------------
if "video_processed" not in st.session_state:
    st.session_state.video_processed = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None


# ---------------------------
# Sidebar - Chats
# ---------------------------
st.sidebar.title("💬 Chats")

# ➕ New Chat (RESET FLOW)
if st.sidebar.button("➕ New Chat"):
    st.session_state.video_processed = False
    st.session_state.current_chat = None
    st.rerun()

# Show existing chats
for chat in st.session_state.chat_history:
    if st.sidebar.button(chat):
        st.session_state.current_chat = chat
        st.session_state.video_processed = True


# ---------------------------
# Main UI
# ---------------------------
st.title("🎥 YouTube Chat App")

# ---------------------------
# Step 1: Enter Video
# ---------------------------
if not st.session_state.video_processed:
    yt_code = st.text_input("Enter YouTube Video Code:")

    if st.button("Process Video"):
        if yt_code.strip():
            # 🔧 Stub processing
            st.session_state.video_processed = True

            # Create new chat AFTER processing
            new_chat = f"Chat {len(st.session_state.chat_history) + 1}"
            st.session_state.chat_history[new_chat] = []
            st.session_state.current_chat = new_chat

            st.success("Video processed! Start chatting below.")
            st.rerun()
        else:
            st.warning("Please enter a valid video code.")

# ---------------------------
# Step 2: Chat UI
# ---------------------------
else:
    if st.session_state.current_chat is None:
        st.info("Process a video to start chatting.")
    else:
        messages = st.session_state.chat_history[st.session_state.current_chat]

        # Show chat messages
        for msg in messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Bottom input (ChatGPT style)
        prompt = st.chat_input("Ask something about the video...")

        if prompt:
            # Save user message
            messages.append({"role": "user", "content": prompt})

            # 🔧 Stub response
            response = f"(Stub Answer) You asked: {prompt}"

            messages.append({"role": "assistant", "content": response})

            # Save back
            st.session_state.chat_history[st.session_state.current_chat] = messages

            st.rerun()