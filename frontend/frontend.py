import streamlit as st
import requests

# Page configuration
st.set_page_config(page_title="Sentiment Analyzer", page_icon="📊", layout="centered")

# App Header
st.title("📊 Sentiment Analysis Dashboard")
st.markdown("Enter a text phrase below to analyze its sentiment value.")

# FastAPI endpoint configuration
FASTAPI_URL = "https://backend-production-7e6cc.up.railway.app/predict"  # Change '/predict' to your exact route path

# User Input Form
with st.form(key="sentiment_form"):
    user_text = st.text_area("Input Text", placeholder="Type your text here (e.g., 'Im good')...", height=100)
    submit_button = st.form_submit_button(label="Analyze Sentiment")

# Handle Form Submission
if submit_button:
    if not user_text.strip():
        st.warning("⚠️ Please enter some text before submitting.")
    else:
        with st.spinner("Analyzing text schema and storing record..."):
            try:
                # Payload matches your exact Pydantic structural format (excluding the auto-increment ID)
                payload = {"input": user_text}
                
                # Make HTTP POST request to your FastAPI backend
                response = requests.post(FASTAPI_URL, json=payload, timeout=10)
                
                if response.status_code == 200:
                    st.success("🎉 Analysis Successful!")
                    
                    # Display the JSON result returned by your FastAPI backend
                    result = response.json()
                    st.json(result)
                elif response.status_code == 422:
                    st.error("❌ 422 Validation Error: The server rejected the request schema structure.")
                    st.write(response.json())
                else:
                    st.error(f"❌ Server returned error code: {response.status_code}")
                    st.write(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error("🚫 Could not connect to the backend server. Make sure your FastAPI server is running at http://127.0.0.1:8000")
