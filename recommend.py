import streamlit as st
import pandas as pd

# Load the dataset
data_path = 'narrowband signals.csv'
data = pd.read_csv(data_path)

st.title("✨ Recommend")

# Select a signal type for recommendations
signal_type = st.selectbox("Choose a signal type for recommendations", options=["Safe", "Warning"])

# Filter data based on the selected signal type
filtered_data = data[data["Remarks"].str.contains(signal_type)]

# Display filtered data
st.write(f"Displaying {signal_type} signals:")
st.dataframe(filtered_data)

# Provide recommendations based on the selected signal type
if signal_type == "Safe":
    st.success("These signals are from natural sources. No action needed.")
    st.write("Recommendation: You can safely proceed with analyzing the signal further.")
else:
    st.warning("These signals might indicate alien or abnormal activity.")
    st.write("Recommendation: Proceed with caution. Further analysis and verification required.")
