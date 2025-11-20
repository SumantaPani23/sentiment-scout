import streamlit as st
import google.generativeai as genai
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="SentimentScout",
    page_icon="🔍",
    layout="centered"
)

# 1. The Hero Image
st.image("https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?auto=format&fit=crop&w=800&q=80", use_container_width=True)

# Title and Description
st.title("🔍 SentimentScout")
st.markdown("Analyze the sentiment of your text using Google's Gemini AI.")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    st.markdown("[Get your API key here](https://aistudio.google.com/app/apikey)")
    st.info("Please enter your own API key. It is free and ensures your data privacy.")

# Initialize session state to remember the result
if 'result' not in st.session_state:
    st.session_state.result = None
if 'analyzed_text' not in st.session_state:
    st.session_state.analyzed_text = ""

# Main App Logic
if not api_key:
    st.warning("Please enter your Gemini API Key in the sidebar to start.")
else:
    # Configure the model
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # User Input
        user_text = st.text_area("Enter text to analyze:", height=150, placeholder="Type something here...")
        
        # Button to trigger analysis
        if st.button("Analyze Sentiment", type="primary"):
            if not user_text:
                st.error("Please enter some text to analyze.")
            else:
                with st.spinner("Scouting for sentiment..."):
                    try:
                        # Prompt for Gemini
                        prompt = f"""
                        Analyze the sentiment of the following text. 
                        Provide the result in this format:
                        Sentiment: [Positive/Negative/Neutral]
                        Confidence: [High/Medium/Low]
                        Explanation: [Brief explanation]
                        
                        Text: {user_text}
                        """
                        
                        response = model.generate_content(prompt)
                        # Save to session state so it doesn't disappear
                        st.session_state.result = response.text
                        st.session_state.analyzed_text = user_text
                        
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        st.info("Make sure your API Key is valid.")

        # Display Result (if one exists in memory)
        if st.session_state.result:
            st.markdown("---")
            result_text = st.session_state.result
            
            # Emotional Special Effects
            if "Sentiment: Positive" in result_text:
                st.balloons()
                st.success("Positive Vibes Detected! 🎈")
            elif "Sentiment: Negative" in result_text:
                st.snow()
                st.error("Negative Sentiment Detected. ❄️")
            else:
                st.info("Neutral Sentiment Detected. 😐")
            
            st.write(result_text)

            # --- REVIEW SYSTEM ---
            st.markdown("---")
            st.write("📝 **How was this analysis?**")
            col1, col2, col3 = st.columns([1, 1, 4]) # Columns for layout
            
            with col1:
                if st.button("👍 Good"):
                    st.toast("Thanks for the positive feedback! 🚀")
            
            with col2:
                if st.button("👎 Poor"):
                    st.toast("Thanks! We'll try to improve. 🔧")

    except Exception as e:
        st.error(f"Configuration Error: {e}")

# Footer
st.markdown("---")
st.caption("Sumanta Pani")