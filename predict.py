import streamlit as st
import os
import joblib

# Path to the model file
model_path = "RF_alien_signal.pkl"

# Check if the model file exists
if not os.path.isfile(model_path):
    st.markdown(f"<div class='error-box'>Model file '{model_path}' not found. Please check the file path.</div>", unsafe_allow_html=True)
    st.write("Current directory contents:")
    st.write(os.listdir('.'))
    model = None
else:
    try:
        model = joblib.load(model_path)
    except Exception as e:
        st.markdown(f"<div class='error-box'>An error occurred while loading the model: {e}</div>", unsafe_allow_html=True)
        model = None

def app():
    if model is None:
        st.warning("Model is not loaded. Please check the error messages above.")
        return

    st.markdown("<h1 class='main-title'>🚀 Signal Classification Prediction</h1>", unsafe_allow_html=True)

    # Sidebar for user input
    st.sidebar.header('🔧 User Input Parameters')

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
