import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset
data_path = 'narrowband signals.csv'
data = pd.read_csv(data_path)

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
    .chart-title {
        color: #4169E1;
        font-size: 24px;
        margin-bottom: 10px;
    }
    .recommendation-title {
        color: #FF1493;
        font-size: 24px;
        margin-bottom: 10px;
    }
    .data-summary {
        font-size: 18px;
        color: #4682B4;
    }
    .feedback-form {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
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
min_frequency, max_frequency = st.sidebar.slider(
    "📡 Select Frequency Range (MHz)", 
    int(data["Signal Frequency(MHz)"].min()), 
    int(data["Signal Frequency(MHz)"].max()), 
    (1300, 1550), 
    help="Adjust the slider to filter signals based on frequency range."
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

# Filter data based on user inputs
filtered_data = data[
    (data["Signal Frequency(MHz)"].between(min_frequency, max_frequency)) &
    (data["Signal Duration(seconds)"].between(min_duration, max_duration)) &
    (data["noise"] <= noise_level)
]

# Filter by selected signal types
if "Safe" in signal_types:
    filtered_data = filtered_data[filtered_data["Remarks"].str.contains("Safe")]
if "Warning" in signal_types:
    filtered_data = filtered_data[filtered_data["Remarks"].str.contains("Warning")]

# Display filtered data with expandable section for more details
with st.expander("📋 Filtered Signals Data"):
    st.dataframe(filtered_data)

# Data Summary
if not filtered_data.empty:
    st.markdown("<div class='data-summary'>📊 Data Summary</div>", unsafe_allow_html=True)
    st.write(f"**Number of signals:** {filtered_data.shape[0]}")
    st.write(f"**Average Signal Frequency (MHz):** {filtered_data['Signal Frequency(MHz)'].mean():.2f}")
    st.write(f"**Average Signal Duration (seconds):** {filtered_data['Signal Duration(seconds)'].mean():.2f}")
    st.write(f"**Average Noise Level:** {filtered_data['noise'].mean():.2f}")

# Download filtered data
st.markdown("<div class='custom-box'><h3>📥 Download Filtered Data</h3></div>", unsafe_allow_html=True)
csv = filtered_data.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='filtered_narrowband_signals.csv',
    mime='text/csv'
)

# Interactive scatter plot for signal visualization
st.markdown("<div class='chart-title'>📊 Signal Visualization</div>", unsafe_allow_html=True)
chart_choice = st.selectbox(
    "Choose a visualization type:", 
    ["Frequency vs Noise", "Duration vs Noise", "Frequency vs Duration", "3D Scatter"]
)

# Dynamic charts based on user selection
if chart_choice == "Frequency vs Noise":
    fig = px.scatter(filtered_data, x="Signal Frequency(MHz)", y="noise", color="Remarks", 
                     title="Signal Frequency vs Noise Levels", labels={"noise": "Noise Level"})
elif chart_choice == "Duration vs Noise":
    fig = px.scatter(filtered_data, x="Signal Duration(seconds)", y="noise", color="Remarks", 
                     title="Signal Duration vs Noise Levels", labels={"noise": "Noise Level"})
elif chart_choice == "Frequency vs Duration":
    fig = px.scatter(filtered_data, x="Signal Frequency(MHz)", y="Signal Duration(seconds)", color="Remarks", 
                     title="Signal Frequency vs Duration", labels={"Signal Duration(seconds)": "Duration (s)"})
else:
    fig = go.Figure(data=[go.Scatter3d(
        x=filtered_data["Signal Frequency(MHz)"],
        y=filtered_data["Signal Duration(seconds)"],
        z=filtered_data["noise"],
        mode='markers',
        marker=dict(size=5, color=filtered_data["noise"], colorscale='Viridis', colorbar=dict(title='Noise Level')),
        text=filtered_data["Remarks"]
    )])
    fig.update_layout(
        title="3D Scatter Plot of Frequency, Duration, and Noise",
        scene=dict(
            xaxis_title='Signal Frequency (MHz)',
            yaxis_title='Signal Duration (seconds)',
            zaxis_title='Noise Level'
        )
    )

st.plotly_chart(fig, use_container_width=True)

# Feedback Form
st.markdown("<div class='feedback-form'><h3>📝 Provide Your Feedback</h3></div>", unsafe_allow_html=True)
with st.form(key='feedback_form'):
    st.text_input("Your Name", "")
    st.text_area("Your Feedback", "")
    st.form_submit_button("Submit Feedback")

# Dynamic recommendations section
st.markdown("<div class='recommendation-title'>📝 Recommendations</div>", unsafe_allow_html=True)
if "Safe" in signal_types:
    st.success("✅ These signals are from natural sources. No action needed.")
    st.markdown("<p style='color: #32CD32;'>Proceed with further analysis. 🌿</p>", unsafe_allow_html=True)
if "Warning" in signal_types:
    st.warning("⚠️ These signals might indicate alien or abnormal activity.")
    st.markdown("<p style='color: #FFA500;'>Proceed with caution. Further verification required. 🛸</p>", unsafe_allow_html=True)

# Footer with custom CSS
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p class='footer'>✨ Happy Exploring the Cosmos! 🚀</p>", unsafe_allow_html=True)
