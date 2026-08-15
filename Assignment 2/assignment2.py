import streamlit as st
from google import genai
import os 
from dotenv import load_dotenv

st.set_page_config(
    page_title="AI Multiverse",
    page_icon="🌌",
    layout="centered"
)

st.title("The AI Multiverse")
st.write(
    "Talk to different AI personalities from across the multiverse. "
    "Choose a character, type a message, and see how they respond!"
)
st.caption(
    "Built using Streamlit and Google Gemini API."
)

st.divider()

# using side panel for personality selection
with st.sidebar:
    st.header("Chat Settings")

    personality = st.selectbox(
        "Choose a Personality",
        [
            "🟢 Master Yoda",
            "🔴 Deadpool",
            "🏴‍☠️ Captain Jack Sparrow",
            "🎤 Stand-up Comedian",
            "🕵️ Sherlock Holmes",
        ],
        index= None,
        placeholder= "Select from the list"
    )

    st.divider()

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()


load_dotenv()

client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# displaying previous conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# taking user's input
user_message = st.chat_input("Type your message...")

# handling errors
if not personality:
    st.write("Please choose a personality from the side-bar first.")
    
elif not user_message:
    st.write("Please type a message to start conversing with the character.")

else:
    # saving user's message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )
    # displaying user's message
    with st.chat_message("user"):
        st.markdown(user_message)

    # setting the prompt
    ai_instructions = f"""
        You are {personality}.
        Reply naturally while staying completely in character.
        Keep your responses engaging and consistent with the selected personality.
        User:
        {user_message}
        """
    
    try:
        # sending the prompt to gemini and getting response
        with st.spinner("Your character is typing..."):
            response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents=ai_instructions
            )

            # saving ai's response
            ai_response = response.text
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": ai_response
                }
            )

            # displaying ai's response
            with st.chat_message("assistant"):
                st.markdown(ai_response)
    
    except Exception:
        st.error("Unable to connect to Gemini. Please try again.")