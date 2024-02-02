import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.title("📊 Visualize")

# Example visualization
st.write("Here you can add visualizations related to your data. For example, you can plot histograms, scatter plots, etc.")

# Create dummy data for example
data = pd.DataFrame({
    'Feature': ['A', 'B', 'C', 'D'],
    'Value': [10, 20, 15, 30]
})

# Plot
fig, ax = plt.subplots()
sns.barplot(x='Feature', y='Value', data=data, ax=ax)
st.pyplot(fig)
