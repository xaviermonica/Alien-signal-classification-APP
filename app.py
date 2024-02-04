import streamlit as st
import pandas as pd
# Define pages and their corresponding functions
PAGES = {
    "🚀 Predict": "predict.py",
    "✨ Recommend": "recommend.py",
    "📊 Visualize": "visualize.py",
    "🔍 Analyze": "analyze.py",
    "🔭 Insights": "insights.py",
    "📝 Feedback": "feedback.py",
    "📚 About": "about.py",
}

def main():
    st.set_page_config(page_title="Signal Classification App", page_icon="📡🛸", layout="wide")
    
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    # Load the selected page
    with open(PAGES[selection]) as f:
        exec(f.read())

if __name__ == "__main__":
    main()
