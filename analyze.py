import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page title with icon
st.title("🔍 Advanced Data Analysis")

# Description with improved formatting
st.markdown("""
    This section allows you to conduct **detailed data analysis** on your dataset. You can explore statistical summaries, 
    visualize distributions, and perform interactive analysis.
""")

# Upload dataset option
st.sidebar.header("Upload Your Dataset 📂")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# Check if a file is uploaded
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.subheader("📊 Data Overview")
    
    # Show first few rows of the dataset
    st.write("**Data Preview**:")
    st.dataframe(data.head())
    
    # Show summary statistics
    st.write("**Statistical Summary**:")
    st.write(data.describe())

    # Automatically select only numeric columns for correlation heatmap
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    if len(numeric_columns) > 1:
        st.subheader("📈 Correlation Heatmap")
        selected_columns = st.multiselect("Select numeric features for correlation", numeric_columns, default=numeric_columns)
        
        # Compute and plot heatmap if multiple columns are selected
        if len(selected_columns) > 1:
            corr = data[selected_columns].corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Please select at least two features for the correlation heatmap.")
    else:
        st.warning("No numeric columns available for correlation analysis.")

    # Show interactive analysis options
    st.subheader("🔬 Interactive Analysis")
    
    # Select columns for comparison
    selected_feature = st.selectbox("Select a feature for distribution analysis:", data.columns)
    
    # Plot selected feature distribution
    fig, ax = plt.subplots()
    sns.histplot(data[selected_feature], kde=True, ax=ax)
    ax.set_title(f"Distribution of {selected_feature}")
    st.pyplot(fig)
    
    # Allow user to input custom analysis
    st.sidebar.subheader("Customize Analysis ✍️")
    custom_code = st.sidebar.text_area("Enter your custom Pandas code:", "data.head()")
    
    try:
        st.subheader("🔧 Custom Analysis Output")
        st.write(eval(custom_code))
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.write("📂 Please upload a dataset to begin.")
