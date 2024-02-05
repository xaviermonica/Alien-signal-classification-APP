import streamlit as st

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
    # Set the page configuration
    st.set_page_config(page_title="Signal Classification App", page_icon="📡🛸", layout="wide")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    # Load the selected page
    page_file = PAGES[selection]
    with open(page_file) as f:
        exec(f.read(), globals())

if __name__ == "__main__":
    main()
