import streamlit as st
import pandas as pd
import joblib

# Load the trained model
try:
    model = joblib.load("RF alien signal.pkl")
except FileNotFoundError:
    st.error("Error: The model file 'RF alien signal.pkl' was not found.")
    model = None

st.title("🚀 Predict")

# User input section in the sidebar
def user_input_features():
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
        'Signal Origin ': signal_origin
    }

    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# Display user input
st.subheader('User Input Features')
st.write(input_df)

# Make prediction
if model:
    try:
        prediction = model.predict(input_df)
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
        prediction = [None]
else:
    prediction = [None]

# Display the prediction result
st.subheader('Prediction Result')
if prediction[0] is not None:
    prediction_message = "📡 It's a safe signal from natural sources." if prediction[0] == 'Safe : signal from natural sources' else "🛸 Warning: potential alien signal detected!"
    st.markdown(f"<div class='prediction-box'>{prediction_message}</div>", unsafe_allow_html=True)
else:
    st.error("Unable to make a prediction. Please check the model and input data.")
