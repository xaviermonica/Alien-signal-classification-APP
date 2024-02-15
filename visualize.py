import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px

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

# ---- 10 Other Visualizations ----
# (Refer to the previous code for additional visualizations)

# Sunburst Plot 1: User input columns
st.write("### Sunburst Plot 1")
columns_1 = st.multiselect(
    "Choose columns for Sunburst Plot 1 (choose 2 or more):",
    ['Stars Type', 'brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)', 'Remarks'],
    default=['Stars Type', 'Remarks']
)

if len(columns_1) >= 2:
    fig_sunburst_1 = px.sunburst(data, path=columns_1)
    st.plotly_chart(fig_sunburst_1)
else:
    st.write("Please select at least 2 columns for the Sunburst plot.")

# Sunburst Plot 2: User input columns
st.write("### Sunburst Plot 2")
columns_2 = st.multiselect(
    "Choose columns for Sunburst Plot 2 (choose 2 or more):",
    ['Stars Type', 'brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)', 'Remarks'],
    default=['Stars Type', 'Signal Frequency(MHz)']
)

if len(columns_2) >= 2:
    fig_sunburst_2 = px.sunburst(data, path=columns_2)
    st.plotly_chart(fig_sunburst_2)
else:
    st.write("Please select at least 2 columns for the Sunburst plot.")

# Sunburst Plot 3: User input columns
st.write("### Sunburst Plot 3")
columns_3 = st.multiselect(
    "Choose columns for Sunburst Plot 3 (choose 2 or more):",
    ['Stars Type', 'brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)', 'Remarks'],
    default=['Stars Type', 'narrowband']
)

if len(columns_3) >= 2:
    fig_sunburst_3 = px.sunburst(data, path=columns_3)
    st.plotly_chart(fig_sunburst_3)
else:
    st.write("Please select at least 2 columns for the Sunburst plot.")
