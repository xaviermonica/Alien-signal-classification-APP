import streamlit as st

st.title("📝 Feedback")

# Feedback form
st.write("We value your feedback! Please share your thoughts or suggestions below:")

feedback = st.text_area("Your Feedback", "")
if st.button("Submit"):
    st.write("Thank you for your feedback!")
