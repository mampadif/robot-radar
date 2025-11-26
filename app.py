import streamlit as st
import textstat
import plotly.graph_objects as go
import re
import numpy as np
import time

# --- AFFILIATE LINKS ---
# Replace these with your actual affiliate links if you have them
LINK_UNDETECTABLE = "https://undetectable.ai/?via=YOUR_ID"
LINK_ORIGINALITY = "https://originality.ai/?ref=YOUR_ID"
LINK_QUILLBOT = "https://quillbot.com/?ref=YOUR_ID"

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Robot Radar - AI Content Detector", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INIT ---
if 'text_input' not in st.session_state:
    st.session_state.text_input = ""

# --- CUSTOM CSS ---
# This CSS ensures the app looks good and fixes the "white text on white background" issue
st.markdown("""
<style>
    /* Main Header Styling */
    .main-header { 
        font-size: 3.5rem; 
        text-align: center; 
        font-weight: 800; 
        margin-bottom: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header { 
        text-align: center; 
        font-size: 1.2rem; 
        color: #888; 
        margin-bottom: 2rem; 
    }

    /* Card Styling - Fixed for Dark Mode */
    /* This forces the text color to be dark grey (#333) so it's visible on the white background */
    .score-card { 
        text-align: center; padding: 25px; background: white;
        border-radius: 15px; margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); border-left: 5px solid;
        color: #333333 !important; 
    }
    .metric-card {
        background: white; padding: 20px; border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); text-align: center; margin: 10px 0;
        color: #333333 !important;
    }
    
    /* Force Headers inside cards to be black */
    .metric-card h3, .score-card h3 {
        color: #000000 !important;
        margin-bottom: 10px;
    }
    .metric-card p, .score-card p {
        color: #333333 !important;
        margin: 5px 0;
    }
    .metric-card strong {
        color: #000000 !important;
    }

    /* Buttons */
    .stButton > button { width: 100%; font-weight: 600; }
    
    .cta-button { 
        display: block; width: 100%; padding: 15px; margin: 10px 0;
        text-align: center; color: white !important; text-decoration: none; 
        font-weight: bold; border-radius: 8px; font-size: 1.1rem;
        transition: all 0.3s ease; border: none; cursor: pointer;
    }
    .cta-button:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); }
    .btn-humanize { background: linear-gradient(135deg, #8E24AA, #AB47BC); }
    .btn-verify { background: linear-gradient(135deg, #2E7D32, #4CAF50); }
    .btn-improve { background: linear-gradient(135deg, #1565C0, #42A5F5); }
</style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def clear_text():
    st.session_state.text_input = ""

def load_sample(sample_type):
    samples = {
        "AI": "Artificial intelligence is a rapidly evolving field of computer science. It involves creating systems that can perform tasks requiring human intelligence. These tasks include visual perception, speech recognition, and decision-making. Machine learning is a subset of AI that focuses on data analysis.",
        "Human": "I honestly hate waking up early. It's the worst. Yesterday? I broke a coffee mug. Snap. Just like that. It hit the floor and I just stood there staring at it for five minutes because, honestly, what else can you do at 6 AM?"
    }
    st.session_state.text_input = samples[sample_type]

# --- ANALYSIS LOGIC ---
def advanced_analysis(text):
    if len(text.split()) < 30: return None
    
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s) > 1]
    words = text.split()
    
    if not sentences: return None
    
    sentence_lengths = [len(s.split()) for s in sentences]
    flesch_grade = textstat.flesch_kincaid_grade(text)
    sentence_variance = np.std(sentence_lengths)
    complex_word_ratio = len([w for w in words if len(w) > 6]) / len(words)
    
    # Heuristic scoring logic
    ai_score = 40 
    if sentence_variance < 4: ai_score += 30
    elif sentence_variance < 7: ai_score += 15
    
    if 8 <= flesch_grade <= 12: ai_score += 10
    if complex_word_ratio < 0.15: ai_score += 10
    
    return {
        "score": min(max(ai_score, 5), 98),
        "flesch_grade": round(flesch_grade, 1),
        "sentence_variance": round(sentence_variance, 1),
        "complex_word_ratio": round(complex_word_ratio * 100, 1),
        "word_count": len(words)
    }

# --- UI LAYOUT ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="main-header">🤖 Robot Radar</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Advanced AI Content Detector & Humanizer</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1])

with col_left:
    # Text Area
    user_text = st.text_area(
        "Paste content below:", 
        height=250, 
        placeholder="Enter text here to analyze patterns...",
        key="text_input"
    )
    
    # Buttons using Callbacks
    b1, b2, b3 = st.columns([1, 1, 1])
    with b1:
        st.button("🗑️ Clear", on_click=clear_text)
    with b2:
        st.button("📝 Load AI Sample", on_click=load_sample, args=("AI",))
    with b3:
        st.button("👤 Load Human Sample", on_click=load_sample, args=("Human",))
    
    st.markdown("###") 
    analyze_clicked = st.button("🔍 ANALYZE CONTENT", type="primary", use_container_width=True)

with col_right:
    # Information Card (Now visible in Dark Mode!)
    st.markdown("""
    <div class="metric-card">
        <h3>📊 How It Works</h3>
        <p><strong>Burstiness:</strong> Sentence variety</p>
        <p><strong>Perplexity:</strong> Word complexity</p>
        <p><strong>Patterns:</strong> Robotic signatures</p>
    </div>
    """, unsafe_allow_html=True)

# --- RESULTS ---
if analyze_clicked and user_text:
    with st.spinner("Scanning patterns..."):
        time.sleep(0.8)
        results = advanced_analysis(user_text)
    
    if results:
        score = results['score']
        
        if score > 70: color, status, emoji = "#dc3545", "LIKELY AI-GENERATED", "🚨"
        elif score > 40: color, status, emoji = "#ffc107", "SUSPICIOUS / MIXED", "⚠️"
        else: color, status, emoji = "#28a745", "LIKELY HUMAN", "✅"
        
        # Gauge Chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number", value = score,
            title = {'text': f"AI Probability<br><span style='font-size:0.8em;color:{color}'>{status}</span>"},
            gauge = {
                'axis': {'range': [0, 100]}, 'bar': {'color': color},
                'steps': [{'range': [0, 40], 'color': "#d4edda"}, {'range': [40, 70], 'color': "#fff3cd"}, {'range': [70, 100], 'color': "#f8d7da"}],
                'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': score}
            }
        ))
        fig.update_layout(height=350, margin=dict(t=80, b=20, l=30, r=30))
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Burstiness", results['sentence_variance'])
        m2.metric("Grade Level", results['flesch_grade'])
        m3.metric("Complexity", f"{results['complex_word_ratio']}%")
        m4.metric("Word Count", results['word_count'])
        
        # Recommendation
        if score > 50:
            st.error(f"**{emoji} High AI Patterns Detected**")
            st.markdown(f"""
            <div class="score-card" style="border-left-color: {color};">
                <h3>🚨 Don't get penalized by Google.</h3>
                <p>Your content lacks human variance.</p>
                <a href="{LINK_UNDETECTABLE}" target="_blank" class="cta-button btn-humanize">✨ Humanize with Undetectable.ai</a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success(f"**{emoji} Natural Writing Detected**")
            st.markdown(f"""
            <div class="score-card" style="border-left-color: {color};">
                <h3>✅ Looks Good!</h3>
                <p>Great flow. Want a second opinion?</p>
                <a href="{LINK_ORIGINALITY}" target="_blank" class="cta-button btn-verify">🛡️ Verify with Originality.ai</a>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.error("❌ Text is too short. Please provide at least 30 words.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔍 About Robot Radar")
    st.info("This tool analyzes text patterns to detect robotic writing styles.")
    st.markdown("---")
    st.subheader("🔗 Resources")
    st.markdown(f"- [Humanize AI]({LINK_UNDETECTABLE})")
    st.markdown(f"- [Verify Originality]({LINK_ORIGINALITY})")
    st.markdown(f"- [Improve Grammar]({LINK_QUILLBOT})")