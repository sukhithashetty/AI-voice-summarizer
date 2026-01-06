import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# 1. PAGE CONFIG
st.set_page_config(page_title="VocalDistiller Pro", layout="wide")

# 2. STATE MANAGEMENT FOR THEME
if 'theme' not in st.session_state:
    st.session_state.theme = 'Light'

def toggle_theme():
    st.session_state.theme = 'Dark' if st.session_state.theme == 'Light' else 'Light'

# 3. DYNAMIC CSS BASED ON THEME
bg_color = "#ffffff" if st.session_state.theme == 'Light' else "#0e1117"
dot_color = "#000000" if st.session_state.theme == 'Light' else "#444444"
text_color = "#000000" if st.session_state.theme == 'Light' else "#ffffff"
box_bg = "#ffffff" if st.session_state.theme == 'Light' else "#1a1c23"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&display=swap');

    .stApp {{
        background-color: {bg_color};
        background-image: radial-gradient({dot_color} 2px, transparent 2px);
        background-size: 40px 40px;
        color: {text_color};
    }}

    /* Bento Box Styling */
    .bento-box {{
        border: 6px solid #000;
        padding: 25px;
        box-shadow: 10px 10px 0px #000;
        margin-bottom: 20px;
        background-color: {box_bg};
        background-image: radial-gradient(rgba(0,0,0,0.05) 1px, transparent 0);
        background-size: 4px 4px;
        color: {text_color};
    }}

    /* Theme Colors */
    .yellow-cell {{ background-color: #FFEF00; color: #000; }}
    .magenta-cell {{ background-color: #FF00FF; color: #fff; }}
    .cyan-cell {{ background-color: #00DBFF; color: #000; }}
    
    .pop-header {{
        font-family: 'Archivo Black', sans-serif;
        font-size: 4.5rem;
        text-align: center;
        color: #FFEF00; 
        -webkit-text-stroke: 2.5px #000;
        text-shadow: 6px 6px 0px #FF00FF, 10px 10px 0px #00DBFF;
        line-height: 1.1;
        margin-bottom: 20px;
    }}

    /* Status Indicators */
    .status-pill {{
        display: inline-block;
        padding: 2px 12px;
        border: 3px solid #000;
        font-weight: bold;
        background: #00FF00;
        color: #000;
        margin-bottom: 10px;
    }}

    /* Buttons */
    div.stButton > button, div.stDownloadButton > button {{
        background-color: #000;
        color: #00DBFF;
        border: none;
        width: 100%;
        height: 50px;
        font-family: 'Archivo Black', sans-serif;
        box-shadow: 5px 5px 0px #FF00FF;
        transition: 0.1s;
    }}

    div.stButton > button:hover {{
        transform: translate(3px, 3px);
        box-shadow: 0px 0px 0px #000;
        color: #FFEF00;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. BACKEND SETUP
load_dotenv()
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception:
    st.error("API Key Missing! Check your .env file.")

# 5. HEADER & THEME TOGGLE
col_t1, col_t2 = st.columns([4, 1])
with col_t1:
    st.markdown("<h1 class='pop-header'>VOCAL DISTILLER PRO</h1>", unsafe_allow_html=True)
with col_t2:
    st.button(f"🌓 {st.session_state.theme} MODE", on_click=toggle_theme)

# 6. BENTO GRID LAYOUT
col_l, col_r = st.columns([1, 1.4], gap="large")

with col_l:
    # --- DASHBOARD ---
    st.markdown('<div class="bento-box magenta-cell"><h3>📊 DASHBOARD</h3>', unsafe_allow_html=True)
    st.markdown('<div class="status-pill">NEURAL LINK: ACTIVE</div>', unsafe_allow_html=True)
    
    st.write("**System Health**")
    st.caption("Latency: 140ms | Uptime: 99.9%")
    
    st.write("**Usage Monitor**")
    st.progress(0.65) # Simulated monthly quota
    st.caption("65% of monthly AI tokens used")
    
    st.markdown("<hr style='border:1px solid black'>", unsafe_allow_html=True)
    st.write("📂 **Recent Artifacts**")
    st.write("• Product_Sync_Jan.mp3")
    st.write("• Research_Notes_04.wav")
    
    if st.button("RESET SESSION"):
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- UPLOAD ---
    st.markdown('<div class="bento-box yellow-cell"><h3>🎙️ CAPTURE</h3>', unsafe_allow_html=True)
    audio_file = st.file_uploader("Upload", type=["mp3", "wav", "m4a"], label_visibility="collapsed")
    if audio_file:
        st.audio(audio_file)
    st.markdown('</div>', unsafe_allow_html=True)

with col_r:
    # --- SETTINGS ---
    st.markdown('<div class="bento-box white-cell"><h3>⚙️ ENGINE CONFIG</h3>', unsafe_allow_html=True)
    
    s1, s2 = st.columns(2)
    with s1:
        model = st.selectbox("AI Model", ["Llama 3.3 Versatile", "Whisper Large v3"])
        lang = st.selectbox("Target Language", ["English", "Hindi", "Kannada", "Spanish"])
    with s2:
        creativity = st.select_slider("Creativity (Temp)", options=["Linear", "Balanced", "Creative"])
        tone = st.radio("Tone", ["Academic", "Executive", "Simple"], horizontal=True)
    
    analyze_btn = st.button("🚀 INITIATE DISTILLATION")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- RESULTS ---
    st.markdown('<div class="bento-box cyan-cell"><h3>✨ DISTILLED INSIGHTS</h3>', unsafe_allow_html=True)
    
    if audio_file and analyze_btn:
        with st.status("🧬 Sequencing Data...", expanded=True) as status:
            try:
                audio_content = audio_file.read()
                transcription = client.audio.transcriptions.create(
                    file=(audio_file.name, audio_content),
                    model="whisper-large-v3-turbo"
                )
                
                # Dynamic instructions based on settings
                prompt = f"Act as a professional analyst. Summarize this in {lang} with an {tone} tone. Creativity level: {creativity}. Text: {transcription.text}"
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                summary = response.choices[0].message.content
                status.update(label="Sequence Complete!", state="complete")
                
                st.markdown(f'<div style="background:white; border:3px solid #000; padding:20px; color:#000; font-family:monospace; font-weight:bold;">{summary}</div>', unsafe_allow_html=True)
                st.download_button("💾 EXPORT TO .TXT", data=summary, file_name="distilled_notes.txt")

            except Exception as e:
                st.error(f"Engine Failure: {e}")
    else:
        st.info("System Ready. Awaiting Source Data.")
    st.markdown('</div>', unsafe_allow_html=True)