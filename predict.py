import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("RF alien signal.pkl")

def app():
    st.title("🚀 Predict")

    # User input section
    def user_input_features():
        brightpixel = st.slider("Bright Pixel", 0.0, 1.0, 0.5)
        narrowband = st.slider("Narrowband", 0.0, 1.0, 0.5)
        narrowbanddrd = st.slider("Narrowband DRD", 0.0, 1.0, 0.5)
        noise = st.slider("Noise", 0.0, 1.0, 0.5)
        stars_type = st.slider("Stars Type", 0, 20, 10)
        signal_frequency = st.slider("Signal Frequency (MHz)", 1000, 2000, 1400)
        signal_duration = st.slider("Signal Duration (seconds)", 1, 20, 10)
        signal_origin = st.slider("Signal Origin", 0, 5, 0)

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
    prediction = model.predict(input_df)

    # Display the prediction result
    st.subheader('Prediction Result')
    prediction_message = "📡 It's a safe signal from natural sources." if prediction[0] == 'Safe : signal from natural sources' else "🛸 Warning: potential alien signal detected!"
    st.markdown(f"<div class='prediction-box'>{prediction_message}</div>", unsafe_allow_html=True)

# Ensure the function `app()` is called when this file is executed
if __name__ == "__main__":
    app()
