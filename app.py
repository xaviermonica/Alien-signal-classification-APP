import streamlit as st

# Define pages and their corresponding script filenames
PAGES = {
    "🚀 Predict": "predict.py",
    "✨ Recommend": "recommend.py",
    "📊 Visualize": "visualize.py",
    "🔍 Analyze": "analyze.py",
    "🔭 Insights": "insights.py",
    "📝 Feedback": "feedback.py",
    "📚 About": "about.py",
}

def load_page(page_file):
    with open(page_file) as f:
        exec(f.read(), globals())

def main():
    # Set the page configuration
    st.set_page_config(page_title="Signal Classification App", page_icon="📡🛸", layout="wide")
    
    # Custom header
    st.markdown("""
        <style>
        .header {
            background-color: #1f77b4; /* Blue */
            padding: 10px;
            text-align: center;
            color: white;
            border-radius: 5px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        </style>
        <div class="header">
            <h1>Signal Classification App</h1>
            <p>Your gateway to analyzing and predicting signals 🚀</p>
        </div>
    """, unsafe_allow_html=True)
    

    # Sidebar for navigation with a dropdown menu
    st.sidebar.title("Navigation")
    selection = st.sidebar.selectbox("Select a page", list(PAGES.keys()), key="sidebar")
    
    # Display loading spinner while loading the page
    with st.spinner(f"Loading {selection}..."):
        page_file = PAGES[selection]
        load_page(page_file)
    st.image('bermuda-triangle-mystery-event.jpg')
    # Footer
    st.markdown("""
        <style>
        .footer {
            padding: 10px;
            text-align: center;
            background-color: #f0f0f0;
            border-top: 1px solid #ddd;
            color: #333;
        }
        </style>
        <div class="footer">
            <p>&copy; 2024 Signal Classification App</p>
            <p>Follow me on <a href="https://www.linkedin.com/in/devanik/" target="_blank">Linkedin</a> | <a href="https://github.com/Devanik21" target="_blank">GitHub</a></p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
