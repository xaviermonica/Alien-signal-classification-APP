import streamlit as st

# Custom CSS for styling
st.markdown("""
    <style>
    .about-title {
        font-size: 2em;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 20px;
    }
    .about-section {
        background-color: #F7F9FC;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .feature-list {
        list-style-type: disc;
        margin-left: 20px;
        color: #333;
    }
    .highlight {
        color: #E94E77;
        font-weight: bold;
    }
    .developer-info {
        background-color: #E1F5FE;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .contact {
        background-color: #FFF3E0;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="about-title">📚 About</div>

    <div class="about-section">
        <h2>Welcome to the <span class="highlight">Signal Classification Application</span>! 🚀</h2>
        <p>This application is designed to revolutionize how we classify and analyze signals using state-of-the-art machine learning models. Whether you're predicting signal types, exploring data, or seeking recommendations, this tool has you covered.</p>

        <h3>Key Features 🌟</h3>
        <ul class="feature-list">
            <li><strong>🔍 Prediction:</strong> Classify signals with precision based on your input data.</li>
            <li><strong>💡 Recommendations:</strong> Receive insightful suggestions from your analyses.</li>
            <li><strong>📊 Visualization:</strong> Enjoy interactive and detailed visualizations for data exploration.</li>
            <li><strong>🔬 Analysis:</strong> Perform comprehensive statistical and exploratory data analysis.</li>
        </ul>

        <p>Our mission is to make signal classification intuitive, interactive, and impactful, providing you with all the tools you need in one place.</p>
    </div>

    <div class="developer-info">
        <h3>Developed By 🛠️</h3>
        <p><strong>Devanik</strong><br>_Aspiring AI Ops Engineer_</p>
        <p><strong>Niki</strong><br>_Your AI Assistant, powered by ChatGPT_</p>
        <p>We are dedicated to enhancing your experience and constantly evolving the app to meet your needs. Dive in and explore the power of signal classification like never before!</p>
    </div>

    <div class="contact">
        <h3>Stay Connected 📬</h3>
        <p>Feel free to reach out with any questions, feedback, or suggestions. We're here to help you make the most of our application!</p>
    </div>
""", unsafe_allow_html=True)
