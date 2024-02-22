import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy import stats

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
st.write("### ANOVA: Analysis of Variance by 'Stars Type'")
anova_columns = st.multiselect(
    "Choose a feature for ANOVA (dependent variable):",
    ['brightpixel', 'narrowband', 'narrowbanddrd', 'noise', 'Signal Frequency(MHz)', 'Signal Duration(seconds)']
)

if anova_columns:
    from statsmodels.formula.api import ols
    import statsmodels.api as sm

    for col in anova_columns:
        model = ols(f'{col} ~ C(`Stars Type`)', data=data).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        st.write(f"#### ANOVA Results for {col}")
        st.write(anova_table)
else:
    st.error("Please select at least one column for ANOVA analysis.")

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
