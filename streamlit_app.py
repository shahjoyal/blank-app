import streamlit as st

# Set the title of the app
st.title("Looking for Jobfy?")

# Display message
st.write("The website you are looking for is here! Click the button below to visit Jobfy.")

# Button to redirect to Jobfy app
if st.button("Go to Jobfy"):
    st.markdown("<meta http-equiv='refresh' content='0; URL=https://jobfy-app.streamlit.app/'>", unsafe_allow_html=True)
