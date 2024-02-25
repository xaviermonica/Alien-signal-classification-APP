import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set page configuration with an attractive layout
st.set_page_config(page_title="Advanced Data Analysis", layout="wide")

# Custom CSS for a modern, attractive design with animations
st.markdown("""
    <style>
    /* Set background for app */
    .reportview-container {
        background: linear-gradient(135deg, #e0f7fa, #ffffff);
        color: black;
        font-family: 'Helvetica', sans-serif;
    }

    /* Style sidebar background */
    .sidebar .sidebar-content {
        background-color: #e3f2fd;
        border-right: 2px solid #90caf9;
        color: black;
    }

    /* Style headings with bold and color */
    h1, h2, h3, h4, h5, h6 {
        color: #64b5f6;
        font-weight: 700;
        font-family: 'Arial', sans-serif;
    }

    /* Style buttons with smooth hover animations */
    .stButton>button {
        background-color: #0277bd;
        color: white;
        border-radius: 10px;
        font-size: 18px;
        padding: 10px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #01579b;
        transform: scale(1.05);
    }

    /* Add box shadow to DataFrame */
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    }

    /* Style text input and multiselect for better user experience */
    .stTextInput>div>input, .stMultiSelect>div {
        background-color: #e1f5fe;
        border-radius: 10px;
        padding: 10px;
    }

    /* Highlight table cells */
    .highlight-cell {
        animation: highlight 1s ease;
    }

    @keyframes highlight {
        0% { background-color: #b3e5fc; }
        100% { background-color: transparent; }
    }
    </style>
    """, unsafe_allow_html=True)

# Title with a modern look and emoji
st.title("📊🌟 Advanced Data Analysis Dashboard")

# Introductory text with cleaner Markdown formatting
st.markdown("""
    ### Welcome to the **Advanced Data Analysis** section! 🎉
    Here's what you can explore:
    - 📊 Perform detailed **statistical analysis**.
    - 🔗 Visualize **correlations** and **distributions**.
    - 🧠 Run custom **Pandas code** to gain more insights.
    ---
""")

# Sidebar section for file upload with emoji and smooth interaction
st.sidebar.header("📂 Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file to begin your analysis", type=["csv"])

# If a file is uploaded
if uploaded_file is not None:
    try:
        # Load data and display it with animations
        data = pd.read_csv(uploaded_file)
        st.subheader("🔍 Dataset Overview")
        st.write(f"📏 **Rows and Columns**: {data.shape[0]} rows, {data.shape[1]} columns")
        
        st.write("🔎 **Data Preview:**")
        st.dataframe(data.head(10))  # Show the first 10 rows

        # Add cool summary statistics with better styling and emojis
        if st.checkbox("📊 Show Statistical Summary", value=True):
            styled_df = data.describe().T.style.format("{:.2f}").background_gradient(cmap="coolwarm")
            st.write(styled_df)
        
        # Filter numeric columns for correlation heatmap
        numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()

        if numeric_columns:
            st.subheader("📈 Correlation Heatmap 🔗")
            selected_columns = st.multiselect("🎯 Select numeric features for correlation analysis", numeric_columns, default=numeric_columns)

            if len(selected_columns) > 1:
                corr = data[selected_columns].corr()
                mask = np.triu(np.ones_like(corr, dtype=bool))  # Mask to show only one triangle of the heatmap
                
                # Plot correlation heatmap
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.heatmap(corr, annot=True, cmap='coolwarm', mask=mask, ax=ax, linewidths=0.5, cbar_kws={"shrink": 0.75})
                ax.set_title("💡 Correlation Heatmap", fontsize=18)
                st.pyplot(fig)
            else:
                st.warning("⚠️ Please select at least two numeric features for correlation.")
        else:
            st.warning("⚠️ No numeric columns available for correlation analysis.")
        
        # Add interactive distribution analysis with smooth visuals
        st.subheader("🔬 Explore Feature Distribution")
        selected_feature = st.selectbox("📊 Select a feature for analysis", data.columns)

        # Numeric and categorical feature-based plots
        if pd.api.types.is_numeric_dtype(data[selected_feature]):
            fig, ax = plt.subplots()
            sns.histplot(data[selected_feature], kde=True, ax=ax, color="#0288d1")
            ax.set_title(f"📊 Distribution of {selected_feature}", fontsize=15)
            st.pyplot(fig)
        else:
            fig, ax = plt.subplots()
            sns.countplot(x=data[selected_feature], ax=ax, palette="Set2")
            ax.set_title(f"📊 Count Plot of {selected_feature}", fontsize=15)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Allow custom Pandas code execution with enhanced styling
        st.sidebar.subheader("📝 Custom Analysis Tool")
        custom_code = st.sidebar.text_area("✍️ Write your custom Pandas code:", "data.head()")

        st.subheader("🛠️ Custom Code Output")
        try:
            result = eval(custom_code)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)  # Display DataFrame with better UI
            else:
                st.write(result)
        except Exception as e:
            st.error(f"❌ Error in custom code: {e}")

    except Exception as e:
        st.error(f"❌ Error loading the dataset: {e}")
else:
    st.info("📂 Please upload a CSV dataset to get started.")
