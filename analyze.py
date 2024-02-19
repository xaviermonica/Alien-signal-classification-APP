import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set page configuration
st.set_page_config(page_title="Advanced Data Analysis", page_icon="🔍", layout="wide")

# Custom CSS for professional look
st.markdown("""
    <style>
    .reportview-container {
        background-color: #f0f2f6;
        color: black;
    }
    .sidebar .sidebar-content {
        background-color: #e1e8ed;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #004466;
    }
    .stButton>button {
        color: white;
        background-color: #005a78;
    }
    .stTextInput>div>input {
        background-color: #e6e6e6;
    }
    </style>
    """, unsafe_allow_html=True)

# Page title with a stylish header
st.title("🔍 Advanced Data Analysis")

# Introductory text with enhanced Markdown formatting
st.markdown("""
    Welcome to the **Advanced Data Analysis** section! Use this tool to:
    - Perform detailed **statistical analysis**.
    - Visualize **correlations** and **distributions** dynamically.
    - Run custom **Pandas code** for further exploration.
    ---
""")

# Sidebar file upload section
st.sidebar.header("Upload Your Dataset 📂")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# If a file is uploaded
if uploaded_file is not None:
    # Load the data
    try:
        data = pd.read_csv(uploaded_file)
        st.subheader("📊 Data Overview")
        st.write(f"**Dataset Dimensions**: {data.shape[0]} rows, {data.shape[1]} columns")
        
        # Display a preview of the dataset with better formatting
        st.write("**Data Preview:**")
        st.dataframe(data.head(10))  # Show the first 10 rows with a scrollable table
        
        # Show summary statistics with conditional formatting
        if st.checkbox("Show Statistical Summary 📊", value=True):
            st.write(data.describe().T.style.format("{:.2f}").background_gradient(cmap="Blues"))
        
        # Filter numeric columns for correlation analysis
        numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        if numeric_columns:
            st.subheader("📈 Correlation Heatmap")
            selected_columns = st.multiselect("Select numeric features for correlation", numeric_columns, default=numeric_columns)
            
            # Show correlation heatmap only if two or more columns are selected
            if len(selected_columns) > 1:
                corr = data[selected_columns].corr()
                mask = np.triu(np.ones_like(corr, dtype=bool))  # Mask to show only one triangle of the heatmap
                
                # Plot correlation heatmap
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(corr, annot=True, cmap='coolwarm', mask=mask, ax=ax, linewidths=.5, cbar_kws={"shrink": .75})
                ax.set_title("Correlation Heatmap", fontsize=15)
                st.pyplot(fig)
            else:
                st.warning("Please select at least two numeric features for correlation analysis.")
        else:
            st.warning("No numeric columns available for correlation analysis.")
        
        # Add interactive analysis section
        st.subheader("🔬 Interactive Feature Distribution")
        selected_feature = st.selectbox("Select a feature for distribution analysis", data.columns)
        
        # Plot based on the selected feature type
        if pd.api.types.is_numeric_dtype(data[selected_feature]):
            # Plot distribution for numeric features
            fig, ax = plt.subplots()
            sns.histplot(data[selected_feature], kde=True, ax=ax, color="blue")
            ax.set_title(f"Distribution of {selected_feature}", fontsize=15)
            st.pyplot(fig)
        else:
            # Plot countplot for categorical features
            fig, ax = plt.subplots()
            sns.countplot(x=data[selected_feature], ax=ax, palette="Set2")
            ax.set_title(f"Count Plot of {selected_feature}", fontsize=15)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Allow user to enter custom Pandas code for more advanced analysis
        st.sidebar.subheader("Run Custom Analysis ✍️")
        custom_code = st.sidebar.text_area("Enter your custom Pandas code here:", "data.head()")
        
        st.subheader("🔧 Custom Analysis Output")
        # Display results of custom code
        try:
            result = eval(custom_code)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)  # Show DataFrame output in a scrollable table
            else:
                st.write(result)
        except Exception as e:
            st.error(f"Error in custom code: {e}")

    except Exception as e:
        st.error(f"Failed to load the dataset. Error: {e}")
else:
    st.info("Please upload a dataset to begin.")
