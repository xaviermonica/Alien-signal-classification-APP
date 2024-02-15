import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.title("📊 Narrowband Signal Visualizations")

# Load the narrowband signals data
data = pd.read_csv("narrowband_signals.csv")

# Display the dataset
st.write("### Dataset Overview")
st.dataframe(data.head())

# Dropdown for selecting feature to visualize
feature = st.selectbox(
    "Select a feature to visualize",
    ['brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)']
)

# Bar plot for selected feature
st.write(f"### Bar Plot of {feature}")
fig, ax = plt.subplots()
sns.barplot(x='Stars Type', y=feature, data=data, ax=ax)
st.pyplot(fig)

# Correlation heatmap
st.write("### Correlation Heatmap")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(data[['brightpixel', 'narrowband', 'narrowbanddrd', 'noise']].corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Scatter plot for signal frequency vs signal duration
st.write("### Signal Frequency vs Signal Duration")
fig, ax = plt.subplots()
sns.scatterplot(x='Signal Frequency(MHz)', y='Signal Duration(seconds)', hue='Stars Type', data=data, ax=ax)
st.pyplot(fig)
