import streamlit as st
import pandas as pd

# Load the dataset
data_path = 'narrowband signals.csv'
data = pd.read_csv(data_path)

st.title("✨ Recommend")

# Sidebar for filtering options
st.sidebar.header("🔍 Filter Options")

# Select signal type for recommendations
signal_type = st.sidebar.selectbox("Choose a signal type", options=["Safe", "Warning", "All"])

# Filter by signal frequency
min_frequency, max_frequency = st.sidebar.slider(
    "Signal Frequency Range (MHz)", int(data["Signal Frequency(MHz)"].min()), int(data["Signal Frequency(MHz)"].max()), (1300, 1550)
)

# Filter by signal duration
min_duration, max_duration = st.sidebar.slider(
    "Signal Duration (seconds)", int(data["Signal Duration(seconds)"].min()), int(data["Signal Duration(seconds)"].max()), (0, 15)
)

# Filter by noise level
noise_level = st.sidebar.slider(
    "Maximum Noise Level", float(data["noise"].min()), float(data["noise"].max()), 0.5
)

# Filtering data based on user input
filtered_data = data[
    (data["Signal Frequency(MHz)"].between(min_frequency, max_frequency)) &
    (data["Signal Duration(seconds)"].between(min_duration, max_duration)) &
    (data["noise"] <= noise_level)
]

# Further filter by signal type
if signal_type != "All":
    filtered_data = filtered_data[filtered_data["Remarks"].str.contains(signal_type)]

# Display the filtered data
st.write(f"Displaying signals based on your filters ({signal_type} signals):")
st.dataframe(filtered_data)

# Show summary statistics of filtered data
st.write("### Summary Statistics:")
st.write(filtered_data.describe())

# Provide recommendations based on filtered data
if signal_type == "Safe":
    st.success("These signals are from natural sources. No action needed.")
    st.write("Recommendation: You can safely proceed with analyzing these signals further.")
elif signal_type == "Warning":
    st.warning("These signals might indicate alien or abnormal activity.")
    st.write("Recommendation: Proceed with caution. Further analysis and verification are required.")
else:
    st.info("No specific recommendation for the selected signal types.")
