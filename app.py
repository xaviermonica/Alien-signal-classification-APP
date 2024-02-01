import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("C:\\imp\\ml JUPYTER\\MY ML PROJECTS(BOOK)\\3.Deep learning\\ANN\\Recreation\\space\\Alien signal\\RF alien signal.pkl")
# Title of the web app
st.set_page_config(page_title="Signal Classification App", page_icon="📡🛸", layout="wide")
st.title("Signal Classification App")

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f0f4f8;
            font-family: 'Arial', sans-serif;
        }
        .sidebar .sidebar-content {
            background-color: #f7f7f7;
        }
        .css-1lcbmhc {
            overflow: auto;
        }
        .stButton button {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #0056b3;
        }
        .prediction-box {
            background-color: #333;
            border: 1px solid #fff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
         .note-box {
            background-color: #333; /* Dark background */
            color: #fff; /* White text color */
            border: 1px solid #444; /* Slightly lighter border */
            border-radius: 10px;
            padding: 10px;
            margin-top: 20px;
        }
        .icon {
            font-size: 24px;
            vertical-align: middle;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar for user input
st.sidebar.header("Input Features")

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

# Get user input
input_df = user_input_features()

# Display user input
st.subheader('User Input Features')
st.write(input_df)

# Make prediction
prediction = model.predict(input_df)

# Display the prediction result
st.subheader('Prediction Result')

# Customize the prediction message
prediction_message = ""
if prediction[0] == 'Safe : signal from natural sources':
    prediction_message = "📡 It's a safe signal from natural sources."
else:
    prediction_message = "🛸 Warning: potential alien signal detected!"

st.markdown(f"<div class='prediction-box'>{prediction_message}</div>", unsafe_allow_html=True)

# Add more details or a description below the result
st.markdown("""
<div class="note-box">
    <strong>Note:</strong> The classification is based on the model's analysis of features such as bright pixel, narrowband, narrowband DRD, noise, stars type, signal frequency, duration, and origin.
</div>
""", unsafe_allow_html=True)
