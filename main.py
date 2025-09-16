import streamlit as st
import requests
from PIL import Image, ImageOps

st.set_page_config(page_title="Leaf Disease Detection", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
* { font-family: 'Poppins', sans-serif; }
            
.stApp { background: #fafaf7; }
            
.hero { text-align: center; margin-bottom: 2rem; }
            
.hero h1 { font-size: 3rem; font-weight: 700; color: #2e7d32; margin-bottom: 0.5rem; }
            
.hero p { font-size: 1.2rem; color: #555; }
            
.upload-card { background: #fff; border-radius: 20px; padding: 2rem; box-shadow: 0 4px 16px rgba(0,0,0,0.05); text-align: center; margin: auto; width: 350px; transition: all 0.3s ease; }
            
.upload-card:hover { transform: translateY(-4px); box-shadow: 0 8px 20px rgba(0,0,0,0.08); }
            
.result-card { background: #fff; border-radius: 20px; padding: 1rem; margin: 0 0 1.5rem; width: 100%; box-shadow: 0 6px 18px rgba(0,0,0,0.05); }
            
.stButton>button { background: transparent; color: #2e7d32; font-weight: 600; border-radius: 14px; padding: 0.6em 1.5em; transition: all 0.3s ease;  border: 2px solid #4CAF50; }
            
.stButton>button:hover {transform: translateY(-2px); }
</style>
            
""", unsafe_allow_html=True)

st.markdown("""
<div class='hero'>
    <h1>Leaf Disease Detector</h1>
    <p>Upload a leaf image and get AI-powered disease detection with insights & treatments</p>
</div>
""", unsafe_allow_html=True)

api_url = "http://localhost:8000/"

uploaded_file = st.file_uploader("Upload Leaf Image", type=["jpg", "jpeg", "png","bmp", "tiff", "tif", "gif", "webp"])
image_to_display = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    fixed_width = 380
    fixed_height = 280
    image = ImageOps.contain(image, (fixed_width, fixed_height))
    image_to_display = image

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.image(image, width=fixed_width)
        detect_clicked = st.button("Detect Disease", key="detect_btn")

    with col2:
        results_placeholder = st.container()


    if detect_clicked:
        with st.spinner("Analyzing..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(f"{api_url}/disease-detection-file", files=files, timeout=30)

                if response.status_code == 200:
                    result = response.json()

                    with results_placeholder:
                        if result.get("disease_type") == "invalid_image":
                            st.error("Invalid Image: Please upload a leaf photo for analysis.")

                        elif result.get("disease_type") == "healthy":
                            st.success(f"Healthy Leaf.. Confidence: {result.get('confidence','N/A')}%")

                        else:
                           
                            st.markdown("""
                            <style>
                            .main-card { background: #fff;  border: 2px solid #4CAF50;  border-radius: 20px; padding: 25px; text-align: center;margin-bottom: 25px; box-shadow: 0 6px 12px rgba(0,0,0,0.08);}

                           .main-card h1 { color: #2e7d32; font-size: 2rem;margin-bottom: 10px; font-weight: 700; }
                                        
                           .badge { display: inline-block; padding: 6px 12px; margin: 5px; font-size: 0.9rem; font-weight: 600;color: #2e7d32;  border: 2px solid #4CAF50; border-radius: 10px; background: transparent; }

                            .section-card { background:#ffffff; border-radius:20px; padding:20px; box-shadow:0 10px 25px rgba(0,0,0,0.08); margin-bottom:15px; }
                                        
                            .section-title { font-weight:600; color:#00796b; margin-bottom:8px; font-size:1rem; }
                                        
                            .section-list { padding-left:1.2rem; font-size:0.95rem; margin:0; }
                            </style>
                            """, unsafe_allow_html=True)

                            st.markdown(f"""
                            <div class='main-card'>
                                <h1>{result.get('disease_name','Unknown Disease')}</h1>
                                <div>
                                    <span class='badge'>Type: {str(result.get('disease_type','N/A')).capitalize()}</span>
                                    <span class='badge'>Confidence: {result.get('confidence','N/A')}%</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            for title, items in [("Symptoms", result.get("symptoms", [])),
                                                 ("Possible Causes", result.get("possible_causes", [])),
                                                 ("Treatment", result.get("treatment", []))]:
                                if items:
                                    st.markdown(f"""
                                    <div class='section-card'>
                                        <div class='section-title'>{title}</div>
                                        <ul class='section-list'>
                                            {''.join([f"<li>{i}</li>" for i in items])}
                                        </ul>
                                    </div>
                                    """, unsafe_allow_html=True)

                else:
                    with results_placeholder:
                        st.error(f"API Error: {response.status_code}")
                        st.write(response.text)

            except Exception as e:
                with results_placeholder:
                    st.error(f"Error: {str(e)}")
