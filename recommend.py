import streamlit as st
import pandas as pd

# Load the dataset
data_path = 'narrowband signals.csv'
data = pd.read_csv(data_path)

# Set the title with an emoji and style
st.markdown("<h1 style='text-align: center; color: #FF6347;'>✨ Recommend Signals 🌌</h1>", unsafe_allow_html=True)

# Sidebar for filtering options with custom color and emojis
st.sidebar.markdown("<h2 style='color: #4682B4;'>🔍 Filter Options</h2>", unsafe_allow_html=True)

# Signal type selector with emojis
signal_type = st.sidebar.selectbox("🎯 Choose a Signal Type", options=["🔵 Safe", "⚠️ Warning", "🌍 All"])

# Slider for Signal Frequency (with a colorized label)
st.sidebar.markdown("<h4 style='color: #32CD32;'>📡 Signal Frequency (MHz)</h4>", unsafe_allow_html=True)
min_frequency, max_frequency = st.sidebar.slider(
    "Select the frequency range", int(data["Signal Frequency(MHz)"].min()), int(data["Signal Frequency(MHz)"].max()), (1300, 1550)
)

# Slider for Signal Duration (with a colorized label)
st.sidebar.markdown("<h4 style='color: #DAA520;'>⏳ Signal Duration (seconds)</h4>", unsafe_allow_html=True)
min_duration, max_duration = st.sidebar.slider(
    "Select the duration range", int(data["Signal Duration(seconds)"].min()), int(data["Signal Duration(seconds)"].max()), (0, 15)
)

# Slider for Noise Level (with a colorized label)
st.sidebar.markdown("<h4 style='color: #FF4500;'>🔊 Maximum Noise Level</h4>", unsafe_allow_html=True)
noise_level = st.sidebar.slider(
    "Set the maximum noise level", float(data["noise"].min()), float(data["noise"].max()), 0.5
)

# Apply filters to the dataset based on user input
filtered_data = data[
    (data["Signal Frequency(MHz)"].between(min_frequency, max_frequency)) &
    (data["Signal Duration(seconds)"].between(min_duration, max_duration)) &
    (data["noise"] <= noise_level)
]

# Filter based on signal type selection
if "Safe" in signal_type:
    filtered_data = filtered_data[filtered_data["Remarks"].str.contains("Safe")]
elif "Warning" in signal_type:
    filtered_data = filtered_data[filtered_data["Remarks"].str.contains("Warning")]

# Display filtered results with a colorful header
st.markdown(f"<h3 style='color: #4169E1;'>Filtered Signals for: {signal_type} Signals</h3>", unsafe_allow_html=True)
st.dataframe(filtered_data)

# Show summary statistics in a colorful box
st.markdown("<h4 style='color: #8A2BE2;'>📊 Summary Statistics</h4>", unsafe_allow_html=True)
st.write(filtered_data.describe())

# Add recommendations with background colors and emojis
st.markdown("<h4 style='color: #FF1493;'>📝 Recommendations</h4>", unsafe_allow_html=True)

if "Safe" in signal_type:
    st.success("✅ These signals are from natural sources. No action needed.")
    st.markdown("<p style='color: #32CD32;'>You can safely proceed with analyzing these signals further. 🌿</p>", unsafe_allow_html=True)
elif "Warning" in signal_type:
    st.warning("⚠️ These signals might indicate alien or abnormal activity.")
    st.markdown("<p style='color: #FFA500;'>Proceed with caution. Further analysis and verification are required. 🛸</p>", unsafe_allow_html=True)
else:
    st.info("🌍 You have selected all signals.")
    st.markdown("<p style='color: #4682B4;'>Review the filtered signals for further analysis. 📡</p>", unsafe_allow_html=True)

# Add a footer with a fun closing message
st.markdown("<hr style='border-top: 2px solid #FF6347;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #FF6347;'>✨ Happy Exploring the Cosmos! 🚀</p>", unsafe_allow_html=True)
