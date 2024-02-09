import streamlit as st
import pandas as pd
import joblib

# Add custom CSS for styling
st.markdown("""
    <style>
    .prediction-box {
        background-color: #f2f2f2;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .sidebar .sidebar-content {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 20px;
    }
    .stTitle {
        color: #007bff;
    }
    .stSubheader {
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# Attempt to load the trained model
try:
    model = joblib.load("RF alien signal.pkl")
except FileNotFoundError:
    st.error("Model file 'RF alien signal.pkl' not found. Please check the file path.")
    model = None
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
    model = None

def app():
    if model is None:
        st.warning("Model is not loaded. Please check the error messages above.")
        return

    st.title("🚀 Predict")

    # Sidebar for user input with a background color
    st.sidebar.header('User Input Parameters')
    
    brightpixel = st.sidebar.slider("Bright Pixel", 0.0, 1.0, 0.5)
    narrowband = st.sidebar.slider("Narrowband", 0.0, 1.0, 0.5)
    narrowbanddrd = st.sidebar.slider("Narrowband DRD", 0.0, 1.0, 0.5)
    noise = st.sidebar.slider("Noise", 0.0, 1.0, 0.5)
    stars_type = st.sidebar.slider("Stars Type", 0, 20, 10)
    signal_frequency = st.sidebar.slider("Signal Frequency (MHz)", 1000, 2000, 1400)
    signal_duration = st.sidebar.slider("Signal Duration (seconds)", 1, 20, 10)
    

    # Update the feature names to match those used during model training
    data = {
        'brightpixel': brightpixel,
        'narrowband': narrowband,
        'narrowbanddrd': narrowbanddrd,
        'noise': noise,
        'Stars Type': stars_type,
        'Signal Frequency(MHz)': signal_frequency,
        'Signal Duration(seconds)': signal_duration,
        
    }

    features = pd.DataFrame(data, index=[0])

    # Display user input with a stylish box
    st.subheader('User Input Features')
    st.write(features)

    if model is not None:
        try:
            # Make prediction
            prediction = model.predict(features)

            # Display the prediction result with different colors
            st.subheader('Prediction Result')
            prediction_message = "📡 It's a safe signal from natural sources." if prediction[0] == 'Safe : signal from natural sources' else "🛸 Warning: potential alien signal detected!"
            prediction_color = "#d4edda" if prediction[0] == 'Safe : signal from natural sources' else "#f8d7da"
            st.markdown(f"""
                <div class='prediction-box' style='background-color: {prediction_color};'>
                    {prediction_message}
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")

# Ensure the function `app()` is called when this file is executed
if __name__ == "__main__":
    app()
