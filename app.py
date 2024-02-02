import streamlit as st

# Set up the sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", [
    "🚀 Predict",
    "✨ Recommend",
    "📊 Visualize",
    "🔍 Analyze",
    "🔭 Insights",
    "📝 Feedback",
    "📚 About"
])

# Load the selected page
if page == "🚀 Predict":
    import predict
elif page == "✨ Recommend":
    import recommend
elif page == "📊 Visualize":
    import visualize
elif page == "🔍 Analyze":
    import analyze
elif page == "🔭 Insights":
    import insights
elif page == "📝 Feedback":
    import feedback
elif page == "📚 About":
    import about
