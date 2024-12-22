import streamlit as st
import requests
from io import BytesIO

st.title("Data Cleaning Recommendation Tool")

st.write("Upload a CSV file and provide optional instructions to generate tailored data cleaning steps.")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
user_instructions = st.text_area("User Instructions (Optional)", "")

if uploaded_file:
    if st.button("Generate Cleaning Steps"):
        with st.spinner("Processing..."):
            try:
                # Send file and instructions to Flask API
                files = {"file": ("uploaded_file.csv", BytesIO(uploaded_file.getvalue()), "text/csv")}
                data = {"instructions": user_instructions}
                response = requests.post("http://127.0.0.1:5000/recommend_steps", files=files, data=data)

                if response.status_code == 200:
                    steps = response.json()["steps"]
                    st.success("Steps generated successfully!")
                    st.write("### Recommended Steps")
                    st.text(steps)
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed to connect to the API: {e}")