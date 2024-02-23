import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy import stats
from statsmodels.formula.api import ols
import statsmodels.api as sm
st.title("📊 Advanced Data Analysis of Narrowband Signals")

# Load the narrowband signals data
data = pd.read_csv("narrowband signals.csv")

# Display the dataset
st.write("### Dataset Overview")
st.dataframe(data.describe())

# ---- Descriptive Statistics ----
st.write("### Descriptive Statistics")
if st.checkbox("Show Descriptive Statistics"):
    st.write(data.describe(include='all'))

# ---- Missing Data Analysis ----
st.write("### Missing Data Analysis")
missing_data = data.isnull().sum().sort_values(ascending=False)
missing_data = missing_data[missing_data > 0]

if not missing_data.empty:
    fig, ax = plt.subplots()
    sns.barplot(x=missing_data.index, y=missing_data.values, palette='flare', ax=ax)
    ax.set_title('Missing Data by Feature', fontsize=16)
    ax.set_ylabel('Number of Missing Values', fontsize=14)
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.success("No missing data found!")


# ---- Data Cleaning ----
st.write("### Data Cleaning")
if st.checkbox("Show Data Cleaning Options"):
    st.write("#### Handle Missing Values")
    missing_action = st.selectbox("Choose action for missing values:", ["None", "Drop", "Fill"])
    if missing_action == "Drop":
        data = data.dropna()
    elif missing_action == "Fill":
        fill_value = st.text_input("Enter value to fill missing data:", "0")
        data = data.fillna(fill_value)
    
    st.write("#### Remove Duplicates")
    if st.checkbox("Remove duplicate rows"):
        data = data.drop_duplicates()
    
    st.write("Updated Dataset Overview")
    st.dataframe(data.describe())



# ---- Feature Engineering ----
st.write("### Feature Engineering")
feature_name = st.text_input("Enter new feature name:")
if st.button("Create New Feature"):
    # Example: Creating a new feature as the sum of 'brightpixel' and 'narrowband'
    if 'brightpixel' in data.columns and 'narrowband' in data.columns:
        data[feature_name] = data['brightpixel'] + data['narrowband']
        st.write(f"New feature '{feature_name}' created.")
    st.write("Updated Dataset Overview")
    st.dataframe(data.describe())



# ---- Custom Data Filters ----
st.write("### Custom Data Filters")
filter_column = st.selectbox("Choose column to filter:", data.columns)
filter_value = st.text_input(f"Enter value for {filter_column}:")
if st.button("Apply Filter"):
    filtered_data = data[data[filter_column].astype(str).str.contains(filter_value, na=False)]
    st.write("Filtered Dataset Overview")
    st.dataframe(filtered_data.describe())

# ---- Data Aggregation and Grouping ----
st.write("### Data Aggregation and Grouping")
group_by_column = st.selectbox("Choose column to group by:", data.columns)
agg_function = st.selectbox("Choose aggregation function:", ["Mean", "Sum", "Median", "Count"])
if st.button("Apply Aggregation"):
    if agg_function == "Mean":
        grouped_data = data.groupby(group_by_column).mean()
    elif agg_function == "Sum":
        grouped_data = data.groupby(group_by_column).sum()
    elif agg_function == "Median":
        grouped_data = data.groupby(group_by_column).median()
    elif agg_function == "Count":
        grouped_data = data.groupby(group_by_column).size()
    
    st.write(f"#### Aggregated Data by {group_by_column} ({agg_function})")
    st.dataframe(grouped_data)


# ---- Pairwise Feature Comparison ----
st.write("### Pairwise Feature Comparison")
comparison_columns = st.multiselect(
    "Choose columns for pairwise comparison:",
    ['brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)']
)

if len(comparison_columns) > 1:
    st.write("#### Pairwise Scatter Plots")
    for i in range(len(comparison_columns)):
        for j in range(i + 1, len(comparison_columns)):
            fig = px.scatter(data, x=comparison_columns[i], y=comparison_columns[j], color='Stars Type', title=f"{comparison_columns[i]} vs {comparison_columns[j]}")
            st.plotly_chart(fig)
else:
    st.error("Please select more than one column for pairwise comparison.")


# ---- Time Series Analysis ----
st.write("### Time Series Analysis")
time_column = st.selectbox("Choose time column:", [col for col in data.columns if 'time' in col.lower()])
value_column = st.selectbox("Choose value column:", [col for col in data.columns if col != time_column])

if time_column and value_column:
    data[time_column] = pd.to_datetime(data[time_column], errors='coerce')
    fig, ax = plt.subplots()
    data.plot(x=time_column, y=value_column, ax=ax)
    ax.set_title(f'Time Series of {value_column}')
    st.pyplot(fig)
else:
    st.error("Please select both time and value columns for time series analysis.")


# ---- Clustering Analysis ----
st.write("### Clustering Analysis")
from sklearn.cluster import KMeans

clustering_columns = st.multiselect(
    "Choose columns for clustering:",
    ['brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)']
)
n_clusters = st.slider("Choose number of clusters:", 2, 10, 3)

if len(clustering_columns) > 1:
    st.write("#### K-Means Clustering")
    kmeans = KMeans(n_clusters=n_clusters)
    clusters = kmeans.fit_predict(data[clustering_columns].dropna())
    data['Cluster'] = np.nan
    data.loc[data[clustering_columns].dropna().index, 'Cluster'] = clusters
    
    fig = px.scatter(data, x=clustering_columns[0], y=clustering_columns[1], color='Cluster', title=f'K-Means Clustering with {n_clusters} Clusters')
    st.plotly_chart(fig)
else:
    st.error("Please select more than one column for clustering.")



# ---- Save and Download Processed Data ----
st.write("### Save and Download Processed Data")
if st.button("Download Processed Data"):
    processed_data_path = "processed_data.csv"
    data.to_csv(processed_data_path, index=False)
    st.markdown(f"[Download processed data](./{processed_data_path})")

# ---- Data Distribution & Skewness ----
st.write("### Data Distribution & Skewness")
distribution_columns = st.multiselect(
    "Choose columns to check distribution and skewness:",
    ['brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)'],
    default=['brightpixel', 'narrowband']
)

if distribution_columns:
    for col in distribution_columns:
        st.write(f"#### Distribution of {col}")
        fig, ax = plt.subplots()
        sns.histplot(data[col], kde=True, color='teal', ax=ax)
        ax.set_title(f'Distribution of {col}', fontsize=16)
        st.pyplot(fig)

        # Calculate skewness
        skewness = stats.skew(data[col].dropna())
        st.write(f"Skewness of {col}: **{skewness:.2f}**")
else:
    st.error("Please select at least one column to analyze distribution and skewness.")

# ---- Outliers Detection ----
st.write("### Outliers Detection (Z-Score Method)")
outlier_columns = st.multiselect(
    "Choose columns to detect outliers:",
    ['brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)'],
    default=['brightpixel', 'narrowband']
)

threshold = st.slider("Set Z-Score Threshold:", 1.5, 5.0, 3.0)

if outlier_columns:
    for col in outlier_columns:
        z_scores = np.abs(stats.zscore(data[col].dropna()))
        outliers = data[col][z_scores > threshold]
        st.write(f"#### {col}: {len(outliers)} outliers found")
        if not outliers.empty:
            st.write(outliers)
else:
    st.error("Please select at least one column for outlier detection.")

# ---- Correlation Analysis ----
st.write("### Correlation Matrix with Statistical Significance")
correlation_columns = st.multiselect(
    "Choose columns for correlation analysis:",
    ['brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)'],
    default=['brightpixel', 'narrowband', 'narrowbanddrd']
)

if len(correlation_columns) >= 2:
    st.write(f"#### Correlation Matrix for {', '.join(correlation_columns)}")
    corr_matrix = data[correlation_columns].corr()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax, linewidths=.5)
    ax.set_title('Correlation Matrix', fontsize=16)
    st.pyplot(fig)

    st.write("#### P-Values Matrix")
    p_values_matrix = pd.DataFrame(np.zeros(corr_matrix.shape), columns=corr_matrix.columns, index=corr_matrix.index)
    for row in correlation_columns:
        for col in correlation_columns:
            p_value = stats.pearsonr(data[row].dropna(), data[col].dropna())[1]
            p_values_matrix.loc[row, col] = p_value
    st.write(p_values_matrix)
else:
    st.error("Please select at least two columns for correlation analysis.")

# ---- Hypothesis Testing (T-Test) ----
st.write("### Hypothesis Testing: T-Test Between Features")
t_test_columns = st.multiselect(
    "Choose two columns for T-Test:",
    ['brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)']
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

# ---- PCA (Principal Component Analysis) ----
st.write("### Principal Component Analysis (PCA)")
pca_columns = st.multiselect(
    "Choose columns for PCA:",
    ['brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)'],
    default=['brightpixel', 'narrowband', 'narrowbanddrd']
)

if len(pca_columns) >= 2:
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(data[pca_columns].dropna())
    pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])

    st.write("#### PCA Results")
    fig_pca = px.scatter(pca_df, x='PC1', y='PC2', title='PCA Plot')
    st.plotly_chart(fig_pca)

    st.write(f"Explained Variance Ratio: {pca.explained_variance_ratio_}")
else:
    st.error("Please select at least two columns for PCA.")


# ---- ANOVA (Analysis of Variance) ----

# ---- Feature Importance (Random Forest) ----
st.write("### Feature Importance using Random Forest")
if st.checkbox("Run Random Forest Feature Importance Analysis"):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder

    # Encode 'Stars Type' as target variable
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


# ---- Machine Learning Model Training ----
st.write("### Machine Learning Model Training")
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

target_column = st.selectbox("Choose target column:", ['Stars Type'])
features = st.multiselect("Choose feature columns:", [col for col in data.columns if col != target_column])

if len(features) > 0 and target_column:
    X = data[features].dropna()
    y = data[target_column].dropna()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    
    st.write("#### Model Performance")
    st.text(classification_report(y_test, predictions))
else:
    st.error("Please select feature and target columns for model training.")

# ---- Summary & Insights ----
st.write("### Summary & Key Insights")
st.write("""
- Comprehensive statistical analysis reveals key insights into the dataset.
- Correlation matrix highlights strong linear relationships between various signal properties.
- PCA helps in reducing dimensionality and identifying principal components.
- Outlier detection shows where the anomalies are in the dataset.
- Hypothesis testing indicates statistically significant differences between features.
- Random Forest ranks feature importance, indicating which features most influence 'Stars Type'.
""")
