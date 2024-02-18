import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px

st.title("📊 Narrowband Signal Visualizations")

# Load the narrowband signals data
data = pd.read_csv("narrowband signals.csv")

# Display the dataset
st.write("### Dataset Overview")
st.dataframe(data.head())

# ---- Bar Plot ----
st.write("### Bar Plot")
barplot_columns = st.multiselect(
    "Choose one feature to visualize on Y-axis for the Bar Plot and 'Stars Type' will be on X-axis:",
    ['brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)'],
    default=['brightpixel']
)

if len(barplot_columns) == 1:
    st.write(f"### Bar Plot of {barplot_columns[0]}")
    fig, ax = plt.subplots()
    sns.barplot(x='Stars Type', y=barplot_columns[0], data=data, ax=ax, palette='plasma')
    ax.set_title(f'Bar Plot of {barplot_columns[0]} by Stars Type', fontsize=16)
    ax.set_xlabel('Stars Type', fontsize=14)
    ax.set_ylabel(barplot_columns[0], fontsize=14)
    st.pyplot(fig)
else:
    st.error("Please select exactly 1 feature for the Bar Plot.")

# ---- Correlation Heatmap ----
st.write("### Correlation Heatmap")
heatmap_columns = st.multiselect(
    "Choose at least 2 features for the Correlation Heatmap:",
    ['brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)'],
    default=['brightpixel', 'narrowband']
)

if len(heatmap_columns) >= 2:
    st.write(f"### Correlation Heatmap for {', '.join(heatmap_columns)}")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(data[heatmap_columns].corr(), annot=True, cmap='viridis', ax=ax, linewidths=.5)
    ax.set_title('Correlation Heatmap', fontsize=16)
    st.pyplot(fig)
else:
    st.error("Please select at least 2 features for the Correlation Heatmap.")

# ---- Scatter Plot: Signal Frequency vs Signal Duration ----
st.write("### Scatter Plot: Signal Frequency vs Signal Duration")
scatter_columns = st.multiselect(
    "Choose 2 columns for X and Y axes:",
    ['Signal Frequency(MHz)', 'Signal Duration(seconds)'],
    default=['Signal Frequency(MHz)', 'Signal Duration(seconds)']
)

if len(scatter_columns) == 2:
    st.write(f"### Scatter Plot: {scatter_columns[0]} vs {scatter_columns[1]}")
    fig, ax = plt.subplots()
    sns.scatterplot(x=scatter_columns[0], y=scatter_columns[1], hue='Stars Type', data=data, ax=ax, palette='Set1')
    ax.set_title(f'Scatter Plot: {scatter_columns[0]} vs {scatter_columns[1]}', fontsize=16)
    ax.set_xlabel(scatter_columns[0], fontsize=14)
    ax.set_ylabel(scatter_columns[1], fontsize=14)
    st.pyplot(fig)
else:
    st.error("Please select exactly 2 columns for the Scatter Plot.")

# ---- Sunburst Plot 1 ----
st.write("### Sunburst Plot: Stars Type and Remarks")
sunburst_columns_1 = st.multiselect(
    "Choose at least 2 columns for Sunburst Plot 1:",
    ['Stars Type', 'brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)', 'Remarks'],
    default=['Stars Type', 'Remarks']
)

if len(sunburst_columns_1) >= 2:
    fig_sunburst_1 = px.sunburst(data, path=sunburst_columns_1, color='Signal Frequency(MHz)')
    st.plotly_chart(fig_sunburst_1)
else:
    st.error("Please select at least 2 columns for Sunburst Plot 1.")

# ---- Sunburst Plot 2 ----
st.write("### Sunburst Plot: Stars Type and Signal Frequency")
sunburst_columns_2 = st.multiselect(
    "Choose at least 2 columns for Sunburst Plot 2:",
    ['Stars Type', 'brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)', 'Remarks'],
    default=['Stars Type', 'Signal Frequency(MHz)']
)

if len(sunburst_columns_2) >= 2:
    fig_sunburst_2 = px.sunburst(data, path=sunburst_columns_2, color='Signal Duration(seconds)')
    st.plotly_chart(fig_sunburst_2)
else:
    st.error("Please select at least 2 columns for Sunburst Plot 2.")

# ---- Sunburst Plot 3 ----
st.write("### Sunburst Plot: Stars Type and Brightpixel")
sunburst_columns_3 = st.multiselect(
    "Choose at least 2 columns for Sunburst Plot 3:",
    ['Stars Type', 'brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)', 'Remarks'],
    default=['Stars Type', 'narrowband']
)

if len(sunburst_columns_3) >= 2:
    fig_sunburst_3 = px.sunburst(data, path=sunburst_columns_3, color='brightpixel')
    st.plotly_chart(fig_sunburst_3)
else:
    st.error("Please select at least 2 columns for Sunburst Plot 3.")

# ---- Boxplot ----
st.write("### Boxplot of Brightpixel vs. Stars Type")
fig, ax = plt.subplots()
sns.boxplot(x='Stars Type', y='brightpixel', data=data, ax=ax, palette='pastel')
ax.set_title('Boxplot of Brightpixel by Stars Type', fontsize=16)
ax.set_xlabel('Stars Type', fontsize=14)
ax.set_ylabel('Brightpixel', fontsize=14)
st.pyplot(fig)

# ---- Violin Plot ----
st.write("### Violin Plot of Narrowband vs. Stars Type")
fig, ax = plt.subplots()
sns.violinplot(x='Stars Type', y='narrowband', data=data, ax=ax, palette='muted')
ax.set_title('Violin Plot of Narrowband by Stars Type', fontsize=16)
ax.set_xlabel('Stars Type', fontsize=14)
ax.set_ylabel('Narrowband', fontsize=14)
st.pyplot(fig)

# ---- Pairplot ----
st.write("### Pairplot of Selected Features")
pairplot_columns = st.multiselect(
    "Choose features for Pairplot (at least 2):",
    ['brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)', 'Stars Type'],
    default=['brightpixel', 'narrowband', 'narrowbanddrd', 'noise']
)

# Ensure 'Stars Type' is included for hue if it is selected
hue = 'Stars Type' if 'Stars Type' in pairplot_columns else None

if len(pairplot_columns) >= 2:
    st.write(f"### Pairplot of {', '.join(pairplot_columns)}")
    fig = sns.pairplot(data[pairplot_columns], hue=hue, palette='husl')
    st.pyplot(fig)
else:
    st.error("Please select at least 2 features for the Pairplot.")

# ---- Histogram ----
st.write("### Histogram of Signal Frequency (MHz)")
fig, ax = plt.subplots()
sns.histplot(data['Signal Frequency(MHz)'], bins=20, kde=True, ax=ax, color='skyblue')
ax.set_title('Histogram of Signal Frequency (MHz)', fontsize=16)
ax.set_xlabel('Signal Frequency (MHz)', fontsize=14)
ax.set_ylabel('Frequency', fontsize=14)
st.pyplot(fig)

# ---- Line Plot ----
st.write("### Line Plot: Signal Frequency vs. Signal Duration")
fig, ax = plt.subplots()
sns.lineplot(x='Signal Duration(seconds)', y='Signal Frequency(MHz)', data=data, ax=ax, color='orange')
ax.set_title('Line Plot: Signal Frequency vs. Signal Duration', fontsize=16)
ax.set_xlabel('Signal Duration (seconds)', fontsize=14)
ax.set_ylabel('Signal Frequency (MHz)', fontsize=14)
st.pyplot(fig)

# ---- Heatmap ----
st.write("### Heatmap of Signal Frequency and Signal Duration (Brightness Intensity)")
fig, ax = plt.subplots()
sns.heatmap(data.pivot_table(values='brightpixel', index='Signal Frequency(MHz)', columns='Signal Duration(seconds)'), cmap="Blues", ax=ax, linewidths=.5)
ax.set_title('Heatmap of Brightness Intensity by Signal Frequency and Duration', fontsize=16)
st.pyplot(fig)

# ---- KDE Plot ----
st.write("### KDE Plot of Narrowband vs Narrowbanddrd")
fig, ax = plt.subplots()
sns.kdeplot(x='narrowband', y='narrowbanddrd', data=data, ax=ax, cmap="Reds", shade=True)
ax.set_title('KDE Plot of Narrowband vs Narrowbanddrd', fontsize=16)
ax.set_xlabel('Narrowband', fontsize=14)
ax.set_ylabel('Narrowbanddrd', fontsize=14)
st.pyplot(fig)

# ---- Swarm Plot ----
st.write("### Swarm Plot of Noise vs. Stars Type")
fig, ax = plt.subplots()
sns.swarmplot(x='Stars Type', y='noise', data=data, ax=ax, palette='Set2')
ax.set_title('Swarm Plot of Noise by Stars Type', fontsize=16)
ax.set_xlabel('Stars Type', fontsize=14)
ax.set_ylabel('Noise', fontsize=14)
st.pyplot(fig)

# ---- Strip Plot ----
st.write("### Strip Plot of Signal Frequency(MHz) vs. Stars Type")
fig, ax = plt.subplots()
sns.stripplot(x='Stars Type', y='Signal Frequency(MHz)', data=data, ax=ax, palette='Set1')
ax.set_title('Strip Plot of Signal Frequency by Stars Type', fontsize=16)
ax.set_xlabel('Stars Type', fontsize=14)
ax.set_ylabel('Signal Frequency (MHz)', fontsize=14)
st.pyplot(fig)

# ---- Joint Plot ----
st.write("### Joint Plot of Brightpixel vs. Noise")
fig = sns.jointplot(x='brightpixel', y='noise', data=data, kind="hex", color="green", cmap='Greens')
fig.fig.suptitle('Joint Plot of Brightpixel vs Noise', fontsize=8)
st.pyplot(fig)

import plotly.express as px

st.write("### Radar Chart of Features by Stars Type")

# Prepare the data
data_radar = data[['Stars Type', 'brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)']].copy()

# Group by 'Stars Type' and calculate mean values
data_radar = data_radar.groupby('Stars Type').mean().reset_index()

# Convert to long format for radar chart
data_radar_long = data_radar.melt(id_vars='Stars Type', var_name='Feature', value_name='Value')

# Create radar chart
fig_radar = px.line_polar(data_radar_long, r='Value', theta='Feature', color='Stars Type', line_close=True)
fig_radar.update_layout(title='Radar Chart of Features by Stars Type')
st.plotly_chart(fig_radar)


st.write("### Treemap of Stars Type and Noise")

fig_treemap = px.treemap(data, path=['Stars Type', 'Remarks'], values='noise', color='noise', color_continuous_scale='RdBu')
fig_treemap.update_layout(title='Treemap of Stars Type and Noise')
st.plotly_chart(fig_treemap)


st.write("### Bubble Chart of Signal Frequency vs. Signal Duration")

fig_bubble = px.scatter(data, x='Signal Frequency(MHz)', y='Signal Duration(seconds)', size='brightpixel', color='Stars Type', hover_name='Remarks', size_max=60)
fig_bubble.update_layout(title='Bubble Chart of Signal Frequency vs. Signal Duration')
st.plotly_chart(fig_bubble)


st.write("### Facet Grid of Noise by Stars Type")

g = sns.FacetGrid(data, col="Stars Type", col_wrap=4, height=4, aspect=1.2)
g.map_dataframe(sns.histplot, x='noise', bins=20, kde=True)
g.set_titles(col_template="{col_name}")
g.set_axis_labels("Noise", "Frequency")
g.fig.suptitle('Noise Distribution by Stars Type', fontsize=16)
g.fig.tight_layout()
g.fig.subplots_adjust(top=0.9)
st.pyplot(g.fig)


st.write("### Hexbin Plot of Signal Frequency vs. Signal Duration")

fig, ax = plt.subplots()
hb = ax.hexbin(data['Signal Frequency(MHz)'], data['Signal Duration(seconds)'], gridsize=30, cmap='Blues')
cb = fig.colorbar(hb, ax=ax)
ax.set_xlabel('Signal Frequency (MHz)')
ax.set_ylabel('Signal Duration (seconds)')
ax.set_title('Hexbin Plot of Signal Frequency vs. Signal Duration')
st.pyplot(fig)


# Convert relevant columns to numeric, forcing errors to NaN
columns_to_convert = ['brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)']
for column in columns_to_convert:
    data[column] = pd.to_numeric(data[column], errors='coerce')


st.write("### Stacked Area Chart of Features by Stars Type")

# Ensure numeric data
data = data.copy()
for column in columns_to_convert:
    data[column] = pd.to_numeric(data[column], errors='coerce')

# Group by 'Stars Type' and calculate mean values
data_grouped = data.groupby('Stars Type').mean().reset_index()

# Convert to long format for stacked area chart
data_long = data_grouped.melt(id_vars='Stars Type', var_name='Feature', value_name='Value')

# Create stacked area chart
fig_area = px.area(data_long, x='Feature', y='Value', color='Stars Type', line_group='Stars Type', 
                   title='Stacked Area Chart of Features by Stars Type')
st.plotly_chart(fig_area)
