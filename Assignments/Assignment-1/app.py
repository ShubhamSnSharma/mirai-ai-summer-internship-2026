# TASK 1
import streamlit as st

st.title("The Identity Echo")
st.write(
    "Send your identity across the network. "
    "Fill in your name and message, then click **Send**."
)
st.caption("This application validates user input and estimates AI token usage.")

st.divider()

# TASK 2
user_name = st.text_input("👤 Enter Your Name")
user_message = st.text_input("💬 Enter Your Message")

# TASK 3
if st.button("Send Transmission"):
    # TASK 4
    if not user_name:
        st.error("Please provide your name.")

    elif not user_message:
        st.warning("Please type a message to transmit.")

    else:
        st.divider()
        # TASK 5
        st.success(
            f"""
        ✅ Transmission Successful!
        
        Greetings, {user_name} 

        We received your message:

        > {user_message}
        """
        )

        # Advanced Challenge
        characters = len(user_message)

        token_count = round(characters / 4, 2)   # 1 token = 4 characters

        st.info(
            f"""
        ### System Check

        **Characters:** {characters}

        **Estimated Tokens:** {token_count}
        """
        )


st.divider()

st.caption("Built with ❤️ using Streamlit • MirAI Summer Internship 2026")
