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

# 1. Boxplot for 'brightpixel' across 'Stars Type'
st.write("### Boxplot of Brightpixel vs. Stars Type")
fig, ax = plt.subplots()
sns.boxplot(x='Stars Type', y='brightpixel', data=data, ax=ax)
st.pyplot(fig)

# 2. Violin plot for 'narrowband' distribution by 'Stars Type'
st.write("### Violin Plot of Narrowband vs. Stars Type")
fig, ax = plt.subplots()
sns.violinplot(x='Stars Type', y='narrowband', data=data, ax=ax)
st.pyplot(fig)

# 3. Pairplot for all features (reduced for simplicity)
st.write("### Pairplot of Selected Features")
fig = sns.pairplot(data[['brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Stars Type']], hue='Stars Type')
st.pyplot(fig)

# 4. Histogram for 'Signal Frequency(MHz)'
st.write("### Histogram of Signal Frequency (MHz)")
fig, ax = plt.subplots()
sns.histplot(data['Signal Frequency(MHz)'], bins=20, kde=True, ax=ax)
st.pyplot(fig)

# 5. Line plot for Signal Frequency over Signal Duration
st.write("### Line Plot: Signal Frequency vs. Signal Duration")
fig, ax = plt.subplots()
sns.lineplot(x='Signal Duration(seconds)', y='Signal Frequency(MHz)', data=data, ax=ax)
st.pyplot(fig)

# 6. Heatmap of 'Signal Frequency(MHz)' vs 'Signal Duration(seconds)' using 'brightpixel' as intensity
st.write("### Heatmap of Signal Frequency and Signal Duration (Brightness Intensity)")
fig, ax = plt.subplots()
sns.heatmap(data.pivot_table(values='brightpixel', index='Signal Frequency(MHz)', columns='Signal Duration(seconds)'), cmap="Blues", ax=ax)
st.pyplot(fig)

# 7. KDE plot for 'narrowband' vs 'narrowbanddrd'
st.write("### KDE Plot of Narrowband vs Narrowbanddrd")
fig, ax = plt.subplots()
sns.kdeplot(x='narrowband', y='narrowbanddrd', data=data, ax=ax, cmap="Reds", shade=True)
st.pyplot(fig)

# 8. Swarm plot for 'noise' vs. 'Stars Type'
st.write("### Swarm Plot of Noise vs. Stars Type")
fig, ax = plt.subplots()
sns.swarmplot(x='Stars Type', y='noise', data=data, ax=ax)
st.pyplot(fig)

# 9. Strip plot for 'Signal Frequency(MHz)' vs. 'Stars Type'
st.write("### Strip Plot of Signal Frequency(MHz) vs. Stars Type")
fig, ax = plt.subplots()
sns.stripplot(x='Stars Type', y='Signal Frequency(MHz)', data=data, ax=ax)
st.pyplot(fig)

# 10. Joint plot for 'brightpixel' vs. 'noise'
st.write("### Joint Plot of Brightpixel vs. Noise")
fig = sns.jointplot(x='brightpixel', y='noise', data=data, kind="hex", color="g")
st.pyplot(fig)
