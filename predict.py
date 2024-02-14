import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Add custom CSS for styling
st.markdown("""
    <style>
    .title {
        color: #1f77b4; /* Blue */
    }
    .sidebar .sidebar-content {
        background-color: #f0f8ff; /* Light blue */
        border-radius: 10px;
        padding: 20px;
    }
    .stSubheader {
        color: #ff7f0e; /* Orange */
    }
    .stWrite {
        background-color: #e6f9ff; /* Light cyan */
        padding: 10px;
        border-radius: 5px;
    }
    .prediction-box {
        border-radius: 10px;
        padding: 15px;
        color: #333;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .safe {
        background-color: #d4edda; /* Light green */
    }
    .alert {
        background-color: #f8d7da; /* Light red */
    }
    </style>
""", unsafe_allow_html=True)

# Attempt to load the trained model
try:
    model = joblib.load("RF alien signal.pkl")
except FileNotFoundError:
    st.error("🚨 Model file 'RF alien signal.pkl' not found. Please check the file path.")
    model = None
except Exception as e:
    st.error(f"⚠️ An error occurred while loading the model: {e}")
    model = None

def app():
    if model is None:
        st.warning("⚠️ Model is not loaded. Please check the error messages above.")
        return

    st.title("🚀 Predict", anchor="title")

    # Sidebar for user input
    st.sidebar.header('🛠️ User Input Parameters')
    
    brightpixel = st.sidebar.slider("🌟 Bright Pixel", 0.0, 1.0, 0.5)
    narrowband = st.sidebar.slider("📶 Narrowband", 0.0, 1.0, 0.5)
    narrowbanddrd = st.sidebar.slider("📈 Narrowband DRD", 0.0, 1.0, 0.5)
    noise = st.sidebar.slider("🔊 Noise", 0.0, 1.0, 0.5)
    stars_type = st.sidebar.slider("🌌 Stars Type", 0, 20, 10)
    signal_frequency = st.sidebar.slider("📡 Signal Frequency (MHz)", 1000, 2000, 1400)
    signal_duration = st.sidebar.slider("⏳ Signal Duration (seconds)", 1, 20, 10)
    signal_origin = st.sidebar.slider("🌍 Signal Origin", 0, 5, 0)

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

    # Display user input
    st.subheader('📝 User Input Features')
    st.write(features, key="write", unsafe_allow_html=True)
    # Add button to make prediction
    if st.button('🔍 Make Prediction'):
        if model is not None:
            # Make prediction
            prediction = model.predict(features)

            # Display the prediction result
            st.subheader('🔮 Prediction Result')
            prediction_message = "📡 It's a safe signal from natural sources." if prediction[0] == 'Safe : signal from natural sources' else "🛸 Warning: potential alien signal detected!"
            prediction_class = 'safe' if prediction[0] == 'Safe : signal from natural sources' else 'alert'
            st.markdown(f"<div class='prediction-box {prediction_class}'>{prediction_message}</div>", unsafe_allow_html=True)
            
            # Add feedback section

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Normalize the 'Signal Frequency (MHz)' for visualization
scaled_data = data.copy()
scaled_data['Signal Frequency(MHz)'] = np.log10(scaled_data['Signal Frequency(MHz)'])  # Log scaling

# Plot input values
 # Plot input values
    st.subheader('📊 Input Value Visualization')
    fig, ax = plt.subplots()
    sns.barplot(x=list(data.keys()), y=list(data.values()), ax=ax, palette="viridis")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig)

# Ensure the function `app()` is called when this file is executed
if __name__ == "__main__":
    app()
