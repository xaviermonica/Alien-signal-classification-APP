import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set page configuration with vibrant emojis

# Custom CSS for a modern and colorful look
st.markdown("""
    <style>
    .reportview-container {
        background-color: #f4f7fa;
        color: black;
    }
    .sidebar .sidebar-content {
        background-color: #d6e4f0;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #003d66;
        font-family: 'Arial';
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        border: 2px solid white;
    }
    .stTextInput>div>input {
        background-color: #e1e1e1;
        border-radius: 10px;
    }
    .stDataFrame {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title with emojis for added appeal
st.title("🔍✨ Advanced Data Analysis Dashboard")

# Introductory text with enhanced Markdown formatting and emoji
st.markdown("""
    Welcome to the **🌟 Advanced Data Analysis** section! Here's what you can do:
    - 📊 Perform detailed **statistical analysis**.
    - 🔗 Visualize **correlations** and **distributions** dynamically.
    - 🧠 Run custom **Pandas code** for further exploration.
    ---
""")

# Sidebar section for file upload with emoji
st.sidebar.header("📂 Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("🔍 Choose a CSV file", type=["csv"])

# If a file is uploaded
if uploaded_file is not None:
    # Load the data
    try:
        data = pd.read_csv(uploaded_file)
        st.subheader("📊 Dataset Overview")
        st.write(f"**Rows and Columns**: {data.shape[0]} rows, {data.shape[1]} columns")
        
        # Display a preview of the dataset
        st.write("🔎 **Data Preview:**")
        st.dataframe(data.head(10))  # Show the first 10 rows with a scrollable table

        # Show summary statistics with enhanced formatting and cool emoji
        if st.checkbox("📊 Show Statistical Summary", value=True):
            st.write(data.describe().T.style.format("{:.2f}").background_gradient(cmap="coolwarm"))
        
        # Filter numeric columns for correlation analysis
        numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()

        if numeric_columns:
            st.subheader("📈 Correlation Heatmap 🔗")
            selected_columns = st.multiselect("🎯 Select numeric features for correlation", numeric_columns, default=numeric_columns)

            # Show correlation heatmap only if two or more columns are selected
            if len(selected_columns) > 1:
                corr = data[selected_columns].corr()
                mask = np.triu(np.ones_like(corr, dtype=bool))  # Mask to show only one triangle of the heatmap
                
                # Plot correlation heatmap
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(corr, annot=True, cmap='coolwarm', mask=mask, ax=ax, linewidths=.5, cbar_kws={"shrink": .75})
                ax.set_title("💡 Correlation Heatmap", fontsize=15)
                st.pyplot(fig)
            else:
                st.warning("⚠️ Please select at least two numeric features for correlation analysis.")
        else:
            st.warning("⚠️ No numeric columns available for correlation analysis.")
        
        # Interactive analysis section with emoji
        st.subheader("🔬 Interactive Feature Distribution")
        selected_feature = st.selectbox("🔎 Select a feature for distribution analysis", data.columns)

        # Plot based on the selected feature type
        if pd.api.types.is_numeric_dtype(data[selected_feature]):
            # Plot distribution for numeric features
            fig, ax = plt.subplots()
            sns.histplot(data[selected_feature], kde=True, ax=ax, color="purple")
            ax.set_title(f"📊 Distribution of {selected_feature}", fontsize=15)
            st.pyplot(fig)
        else:
            # Plot countplot for categorical features
            fig, ax = plt.subplots()
            sns.countplot(x=data[selected_feature], ax=ax, palette="Set2")
            ax.set_title(f"🔢 Count Plot of {selected_feature}", fontsize=15)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Allow user to enter custom Pandas code for advanced analysis
        st.sidebar.subheader("📝 Run Custom Analysis")
        custom_code = st.sidebar.text_area("✍️ Enter your custom Pandas code here:", "data.head()")
        
        st.subheader("🛠️ Custom Analysis Output")
        # Display results of custom code
        try:
            result = eval(custom_code)
            if isinstance(result, pd.DataFrame):
                st.dataframe(result)  # Show DataFrame output in a scrollable table
            else:
                st.write(result)
        except Exception as e:
            st.error(f"❌ Error in custom code: {e}")

    except Exception as e:
        st.error(f"❌ Failed to load the dataset. Error: {e}")
else:
    st.info("📂 Please upload a dataset to begin.")
