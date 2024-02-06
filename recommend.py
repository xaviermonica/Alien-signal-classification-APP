import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
data_path = 'narrowband signals.csv'
data = pd.read_csv(data_path)

# Custom CSS for pro look
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 36px;
        color: #FF6347;
        font-weight: bold;
    }
    .sidebar-header {
        font-size: 20px;
        color: #4682B4;
        font-weight: bold;
    }
    .custom-box {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        color: #FF6347;
        font-weight: bold;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Title with custom CSS
st.markdown("<h1 class='main-title'>✨ Recommend Signals 🌌</h1>", unsafe_allow_html=True)

# Sidebar filtering with advanced options
st.sidebar.markdown("<h2 class='sidebar-header'>🔍 Filter Options</h2>", unsafe_allow_html=True)

# Select multiple signal types
signal_types = st.sidebar.multiselect(
    "🎯 Select Signal Types", options=["Safe", "Warning", "All"], default=["Safe", "Warning"]
)

# Slider for frequency range with tooltip
st.sidebar.slider(
    "📡 Select Frequency Range (MHz)", 
    int(data["Signal Frequency(MHz)"].min()), 
    int(data["Signal Frequency(MHz)"].max()), 
    (1300, 1550), 
    help="Adjust the slider to filter signals based on frequency."
)

# Duration with expander for advanced info
with st.sidebar.expander("⏳ Advanced Duration Filtering"):
    min_duration, max_duration = st.slider(
        "Select the Duration Range (seconds)", 
        int(data["Signal Duration(seconds)"].min()), 
        int(data["Signal Duration(seconds)"].max()), 
        (0, 15)
    )

# Slider for noise level with color
noise_level = st.sidebar.slider(
    "🔊 Maximum Noise Level", 
    float(data["noise"].min()), 
    float(data["noise"].max()), 
    0.5, 
    help="Set the maximum acceptable noise level for signals."
)
# Slider for frequency range with tooltip
min_frequency, max_frequency = st.sidebar.slider(
    "📡 Select Frequency Range (MHz)", 
    int(data["Signal Frequency(MHz)"].min()), 
    int(data["Signal Frequency(MHz)"].max()), 
    (1300, 1550), 
    help="Adjust the slider to filter signals based on frequency."
)

# Filter data based on user inputs
filtered_data = data[
    (data["Signal Frequency(MHz)"].between(min_frequency, max_frequency)) &
    (data["Signal Duration(seconds)"].between(min_duration, max_duration)) &
    (data["noise"] <= noise_level)
]

# Filter by selected signal types
if "Safe" in signal_types:
    filtered_data = filtered_data[filtered_data["Remarks"].str.contains("Safe")]
elif "Warning" in signal_types:
    filtered_data = filtered_data[filtered_data["Remarks"].str.contains("Warning")]

# Display filtered data with expandable section for more details
with st.expander("📋 Filtered Signals Data"):
    st.dataframe(filtered_data)

# Interactive scatter plot for signal visualization
st.markdown("<h3 style='color: #4169E1;'>📊 Signal Visualization</h3>", unsafe_allow_html=True)
chart_choice = st.selectbox(
    "Choose a visualization type:", 
    ["Frequency vs Noise", "Duration vs Noise", "Frequency vs Duration"]
)

# Dynamic charts based on user selection
if chart_choice == "Frequency vs Noise":
    fig = px.scatter(filtered_data, x="Signal Frequency(MHz)", y="noise", color="Remarks", 
                     title="Signal Frequency vs Noise Levels", labels={"noise": "Noise Level"})
elif chart_choice == "Duration vs Noise":
    fig = px.scatter(filtered_data, x="Signal Duration(seconds)", y="noise", color="Remarks", 
                     title="Signal Duration vs Noise Levels", labels={"noise": "Noise Level"})
else:
    fig = px.scatter(filtered_data, x="Signal Frequency(MHz)", y="Signal Duration(seconds)", color="Remarks", 
                     title="Signal Frequency vs Duration", labels={"Signal Duration(seconds)": "Duration (s)"})

st.plotly_chart(fig, use_container_width=True)

# Dynamic recommendations section
st.markdown("<h3 style='color: #FF1493;'>📝 Recommendations</h3>", unsafe_allow_html=True)
if "Safe" in signal_types:
    st.success("✅ These signals are from natural sources. No action needed.")
    st.markdown("<p style='color: #32CD32;'>Proceed with further analysis. 🌿</p>", unsafe_allow_html=True)
if "Warning" in signal_types:
    st.warning("⚠️ These signals might indicate alien or abnormal activity.")
    st.markdown("<p style='color: #FFA500;'>Proceed with caution. Further verification required. 🛸</p>", unsafe_allow_html=True)

# Footer with custom CSS
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p class='footer'>✨ Happy Exploring the Cosmos! 🚀</p>", unsafe_allow_html=True)
