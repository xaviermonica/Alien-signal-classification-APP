import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

st.title("🔭 Advanced Insights")

# Load the dataset
data = pd.read_csv("narrowband signals.csv")

# ---- Dataset Overview ----
st.write("### Dataset Overview")
st.dataframe(data.describe())
st.write(f"#### Total Rows: {len(data)}")
st.write(f"#### Total Columns: {len(data.columns)}")

# ---- Data Aggregation and Grouping ----
st.write("### Data Aggregation and Grouping")
group_by_column = st.selectbox("Choose column to group by:", data.columns)
agg_function = st.selectbox("Choose aggregation function:", ["Mean", "Sum", "Median", "Count"])
if st.button("Apply Aggregation"):
    try:
        if agg_function == "Mean":
            grouped_data = data.groupby(group_by_column).mean()
        elif agg_function == "Sum":
            grouped_data = data.groupby(group_by_column).sum()
        elif agg_function == "Median":
            grouped_data = data.groupby(group_by_column).median()
        elif agg_function == "Count":
            grouped_data = data.groupby(group_by_column).size().reset_index(name='Count')

        st.write(f"#### Aggregated Data by {group_by_column} ({agg_function})")
        st.dataframe(grouped_data)
    except Exception as e:
        st.error(f"Error applying aggregation: {e}")

# ---- Data Distribution ----
st.write("### Data Distribution")
distribution_columns = st.multiselect(
    "Choose columns to check distribution:",
    data.columns,
    default=[data.columns[0]]
)

for col in distribution_columns:
    st.write(f"#### Distribution of {col}")
    fig, ax = plt.subplots()
    sns.histplot(data[col].dropna(), kde=True, color='teal', ax=ax)
    ax.set_title(f'Distribution of {col}', fontsize=16)
    st.pyplot(fig)

# ---- Data Skewness ----
st.write("### Data Skewness")
skewness_columns = st.multiselect(
    "Choose columns to check skewness:",
    data.columns,
    default=[data.columns[0]]
)

for col in skewness_columns:
    skewness = stats.skew(data[col].dropna())
    st.write(f"#### Skewness of {col}: {skewness:.2f}")

# ---- Correlation Analysis ----
st.write("### Correlation Analysis")
correlation_columns = st.multiselect(
    "Choose columns for correlation analysis:",
    data.columns,
    default=[data.columns[0], data.columns[1]]
)

if len(correlation_columns) >= 2:
    st.write(f"#### Correlation Matrix for {', '.join(correlation_columns)}")
    corr_matrix = data[correlation_columns].corr()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax, linewidths=.5)
    ax.set_title('Correlation Matrix', fontsize=16)
    st.pyplot(fig)
else:
    st.error("Please select at least two columns for correlation analysis.")

# ---- Outliers Detection ----
st.write("### Outliers Detection")
outlier_columns = st.multiselect(
    "Choose columns to detect outliers:",
    data.columns,
    default=[data.columns[0]]
)

threshold = st.slider("Set Z-Score Threshold:", 1.5, 5.0, 3.0)

for col in outlier_columns:
    st.write(f"#### Outliers in {col}")
    z_scores = np.abs(stats.zscore(data[col].dropna()))
    outliers = data[col][z_scores > threshold]
    st.write(f"Number of outliers: {len(outliers)}")
    if not outliers.empty:
        st.write(outliers)

# ---- Principal Component Analysis (PCA) ----
st.write("### Principal Component Analysis (PCA)")
pca_columns = st.multiselect(
    "Choose columns for PCA:",
    data.columns,
    default=[data.columns[0], data.columns[1]]
)

if len(pca_columns) >= 2:
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(data[pca_columns].dropna())
    pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])

    st.write("#### PCA Results")
    fig_pca = px.scatter(pca_df, x='PC1', y='PC2', title='PCA Plot')
    st.plotly_chart(fig_pca)
    st.write(f"Explained Variance Ratio: {pca.explained_variance_ratio_}")
else:
    st.error("Please select at least two columns for PCA.")

# ---- Feature Importance (Random Forest) ----
st.write("### Feature Importance using Random Forest")
if st.checkbox("Run Random Forest Feature Importance Analysis"):
    try:
        label_encoder = LabelEncoder()
        data['Stars Type Encoded'] = label_encoder.fit_transform(data['Stars Type'])

        X = data.drop(columns=['Stars Type', 'Remarks', 'Stars Type Encoded']).dropna()
        y = data['Stars Type Encoded'].dropna()

        rf = RandomForestClassifier(n_estimators=100)
        rf.fit(X, y)

        feature_importance = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)

        st.write("#### Feature Importance")
        fig, ax = plt.subplots()
        sns.barplot(x=feature_importance.index, y=feature_importance.values, ax=ax, palette='viridis')
        ax.set_title('Feature Importance from Random Forest', fontsize=16)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error in Random Forest Analysis: {e}")

# ---- Hypothesis Testing ----
st.write("### Hypothesis Testing")
t_test_columns = st.multiselect(
    "Choose two columns for T-Test:",
    data.columns
)

if len(t_test_columns) == 2:
    t_stat, p_val = stats.ttest_ind(data[t_test_columns[0]].dropna(), data[t_test_columns[1]].dropna())
    st.write(f"**T-Test Result**: T-Statistic = {t_stat:.2f}, P-Value = {p_val:.5f}")
    if p_val < 0.05:
        st.success(f"The difference between {t_test_columns[0]} and {t_test_columns[1]} is statistically significant.")
    else:
        st.info(f"No significant difference between {t_test_columns[0]} and {t_test_columns[1]}.")
else:
    st.error("Please select exactly two columns for the T-Test.")

# ---- Custom Visualizations ----
st.write("### Custom Visualizations")
custom_plot_type = st.selectbox("Choose plot type:", ["Bar Chart", "Line Chart", "Box Plot"])

if custom_plot_type == "Bar Chart":
    bar_x = st.selectbox("Choose X-axis column for Bar Chart:", data.columns)
    bar_y = st.selectbox("Choose Y-axis column for Bar Chart:", data.columns)
    if st.button("Generate Bar Chart"):
        fig, ax = plt.subplots()
        sns.barplot(x=bar_x, y=bar_y, data=data, ax=ax, palette='pastel')
        ax.set_title('Bar Chart', fontsize=16)
        st.pyplot(fig)

elif custom_plot_type == "Line Chart":
    line_x = st.selectbox("Choose X-axis column for Line Chart:", data.columns)
    line_y = st.selectbox("Choose Y-axis column for Line Chart:", data.columns)
    if st.button("Generate Line Chart"):
        fig, ax = plt.subplots()
        sns.lineplot(x=line_x, y=line_y, data=data, ax=ax, marker='o')
        ax.set_title('Line Chart', fontsize=16)
        st.pyplot(fig)

elif custom_plot_type == "Box Plot":
    box_x = st.selectbox("Choose X-axis column for Box Plot:", data.columns)
    box_y = st.selectbox("Choose Y-axis column for Box Plot:", data.columns)
    if st.button("Generate Box Plot"):
        fig, ax = plt.subplots()
        sns.boxplot(x=box_x, y=box_y, data=data, ax=ax, palette='coolwarm')
        ax.set_title('Box Plot', fontsize=16)
        st.pyplot(fig)

# ---- Summary & Key Insights ----
st.write("### Summary & Key Insights")
st.write("""
- **Data Aggregation and Grouping**: Allows you to summarize the data by different aggregation functions like mean, sum, median, and count.
- **Data Distribution**: Visualizes the distribution of selected columns with histograms and density plots.
- **Data Skewness**: Provides insight into the skewness of data, helping to understand the distribution's asymmetry.
- **Correlation Analysis**: Shows relationships between selected columns using correlation matrices.
- **Outlier Detection**: Identifies and displays outliers using the Z-score method.
- **Principal Component Analysis (PCA)**: Reduces data dimensionality and visualizes principal components.
- **Feature Importance**: Ranks features by their importance in predicting the target variable using Random Forest.
- **Hypothesis Testing**: Compares two columns to test for statistically significant differences using the T-Test.
- **Custom Visualizations**: Allows users to create bar charts, line charts, and box plots for any columns in the dataset.
""")
