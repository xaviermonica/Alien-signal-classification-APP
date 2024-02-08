import streamlit as st
import pandas as pd
import joblib

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 36px;
        color: #FF6347;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .sidebar-header {
        font-size: 20px;
        color: #4682B4;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .prediction-box {
        background-color: #1a0606;
        padding: 20px;
        border-radius: 10px;
        color: white;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .error-box {
        background-color: #ffcccb;
        padding: 20px;
        border-radius: 10px;
        color: #d8000c;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .input-section {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Attempt to load the trained model
try:
    model = joblib.load("RF_alien_signal.pkl")
except FileNotFoundError:
    st.markdown("<div class='error-box'>Model file 'RF_alien_signal.pkl' not found. Please check the file path.</div>", unsafe_allow_html=True)
    model = None
except Exception as e:
    st.markdown(f"<div class='error-box'>An error occurred while loading the model: {e}</div>", unsafe_allow_html=True)
    model = None

def app():
    if model is None:
        st.warning("Model is not loaded. Please check the error messages above.")
        return

    st.markdown("<h1 class='main-title'>🚀 Signal Classification Prediction</h1>", unsafe_allow_html=True)

    st.sidebar.header('🔧 User Input Parameters')

    # Sidebar for user input
    brightpixel = st.sidebar.slider("Bright Pixel", 0.0, 1.0, 0.5)
    narrowband = st.sidebar.slider("Narrowband", 0.0, 1.0, 0.5)
    narrowbanddrd = st.sidebar.slider("Narrowband DRD", 0.0, 1.0, 0.5)
    noise = st.sidebar.slider("Noise", 0.0, 1.0, 0.5)
    stars_type = st.sidebar.slider("Stars Type", 0, 20, 10)
    signal_frequency = st.sidebar.slider("Signal Frequency (MHz)", 1000, 2000, 1400)
    signal_duration = st.sidebar.slider("Signal Duration (seconds)", 1, 20, 10)
    signal_origin = st.sidebar.slider("Signal Origin", 0, 5, 0)

    data = {
        'brightpixel': brightpixel,
        'narrowband': narrowband,
        'narrowbanddrd': narrowbanddrd,
        'noise': noise,
        'Stars Type': stars_type,
        'Signal Frequency(MHz)': signal_frequency,
        'Signal Duration(seconds)': signal_duration,
        'Signal Origin': signal_origin
    }

    features = pd.DataFrame(data, index=[0])

    # Display user input
    st.markdown("<div class='input-section'><h2>User Input Features</h2></div>", unsafe_allow_html=True)
    st.write(features)

    if model is not None:
        # Make prediction
        prediction = model.predict(features)

        # Display the prediction result
        st.markdown("<div class='prediction-box'><h2>Prediction Result</h2></div>", unsafe_allow_html=True)
        prediction_message = (
            "📡 It's a safe signal from natural sources." 
            if prediction[0] == 'Safe : signal from natural sources' 
            else "🛸 Warning: potential alien signal detected!"
        )
        st.markdown(f"<p>{prediction_message}</p>", unsafe_allow_html=True)

# Ensure the function `app()` is called when this file is executed
if __name__ == "__main__":
    app()
