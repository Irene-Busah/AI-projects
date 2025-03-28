import streamlit as st # type: ignore
import joblib # type: ignore
from PIL import Image # type: ignore

# Setting the page configuration (title, icon, layout)
st.set_page_config(
    page_title="Medical Condition Classifier",
    page_icon="💉",
    layout="wide"
)

# Loading the model & vectorizer (as before)
model = joblib.load("logistic_model.pkl")
vectorizer = joblib.load("count_vectorizer.pkl")

# 3. Add custom styling with Markdown or HTML
st.markdown("""
    <style>
    /* Make the main text a bit bigger */   
    .reportview-container .markdown-text-container {
        font-size: 1.1rem;
    }
    /* Customize the sidebar */
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }
    /* Center the title */
    .main .block-container{
        max-width: 1200px;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

st.image("health_banner.jpg", use_column_width=True)

# Main Title
st.title("Medical Condition Text Classifier")

# creating a two-column layout
col1, col2 = st.columns([2, 1], gap="large")

# Left Column - Text Input
with col1:
    st.subheader("Enter Your Medical Review")
    user_input = st.text_area(
        "Type or paste your text here...",
        height=200
    )

    if st.button("Predict"):
        # Transform input & predict
        transformed_input = vectorizer.transform([user_input])
        prediction = model.predict(transformed_input)
        st.success(f"**Predicted Condition:** {prediction[0]}")

# Right Column - Some information or instructions
with col2:
    st.subheader("Instructions")
    st.write("""
    1. Paste or type your medical review on the left.
    2. Click **Predict** to see the classification result.
    3. The model is trained on medical reviews to distinguish among
       conditions like Depression, Birth Control, Diabetes, and High Blood Pressure.
    """)
    st.info("Note: This model is for demonstration purposes only.")

# 7. Expanders for Additional Info (optional)
with st.expander("View Model Details"):
    st.write("**Model:** Logistic Regression\n\n**Vectorizer:** CountVectorizer\n\n**Accuracy:** ~97.88%")

# 8. Footer or Additional Branding
st.markdown("""
---
*Built with [Streamlit](https://streamlit.io/)*
""")
