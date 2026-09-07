"""
AI Video Assistant — Streamlit UI (self-contained)
----------------------------------------------------
This file contains your original main.py pipeline logic (untouched,
just the CLI __main__ block replaced with a Streamlit UI) plus a
techy web UI on top of it.
"""

import os
import tempfile
import streamlit as st

from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.RAG_engine import build_rag_chain, ask_question

load_dotenv()


# ========================================================================
# ORIGINAL PIPELINE LOGIC (unchanged from main.py)
# ========================================================================
def run_pipeline(source: str, language: str = "english") -> dict:
    print("starting AI Video Assistant")

    chunks = process_input(source)

    transcript = transcribe_all(chunks, language)
    print(f"raw transcription (first 300 characters ) {transcript[:300]}")

    title = generate_title(transcript)

    summary = summarize(transcript)

    action_item = extract_action_items(transcript)

    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)

    rag_chain = build_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_item,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }


# ========================================================================
# STREAMLIT UI (replaces the old CLI `if __name__ == "__main__":` block)
# ========================================================================

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------- Techy dark theme CSS ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(0, 255, 200, 0.06), transparent 40%),
        radial-gradient(circle at 85% 30%, rgba(120, 80, 255, 0.08), transparent 45%),
        #05070d;
    color: #e6f1ff;
}

#MainMenu, footer, header {visibility: hidden;}

.hero {
    padding: 2.2rem 2rem 1.6rem 2rem;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(0,255,200,0.08), rgba(120,80,255,0.10));
    border: 1px solid rgba(0,255,200,0.25);
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute; inset: 0;
    background: repeating-linear-gradient(90deg, rgba(255,255,255,0.02) 0px, rgba(255,255,255,0.02) 1px, transparent 1px, transparent 40px);
    pointer-events: none;
}
.hero h1 {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0;
    background: linear-gradient(90deg, #00ffc8, #7c5cff, #00b3ff);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    color: #93a4bd;
    font-size: 0.95rem;
    margin-top: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
}
.badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    padding: 3px 10px;
    border-radius: 20px;
    background: rgba(0,255,200,0.12);
    border: 1px solid rgba(0,255,200,0.4);
    color: #00ffc8;
    margin-right: 6px;
    letter-spacing: 0.5px;
}

.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.3rem 1.4rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(6px);
}
.card h3 {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.95rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #00ffc8;
    margin-top: 0;
    margin-bottom: 0.7rem;
}
.card p, .card li {
    color: #cdd9ea;
    font-size: 0.92rem;
    line-height: 1.55;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: rgba(255,255,255,0.02);
    padding: 6px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.06);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace;
    border-radius: 8px;
    color: #93a4bd;
    padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, rgba(0,255,200,0.18), rgba(120,80,255,0.18)) !important;
    color: #00ffc8 !important;
}

.stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #e6f1ff !important;
    border-radius: 10px !important;
    font-family: 'JetBrains Mono', monospace;
}
[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.03);
    border: 1.5px dashed rgba(0,255,200,0.35) !important;
    border-radius: 14px;
}

.stButton button {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    letter-spacing: 0.5px;
    background: linear-gradient(90deg, #00ffc8, #00b3ff);
    color: #04121a;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.4rem;
    transition: 0.2s ease;
    box-shadow: 0 0 18px rgba(0,255,200,0.25);
}
.stButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 0 26px rgba(0,255,200,0.45);
}

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
}

.section-label {
    font-family: 'JetBrains Mono', monospace;
    color: #7c5cff;
    font-size: 0.8rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 1.6rem 0 0.6rem 0;
    border-left: 3px solid #7c5cff;
    padding-left: 10px;
}

[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace;
    color: #00ffc8;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------- Session state ----------------------------
for key, default in {
    "result": None,
    "chat_history": [],
    "processing": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ---------------------------- Hero header ----------------------------
st.markdown("""
<div class="hero">
    <span class="badge">● ONLINE</span>
    <span class="badge">RAG-POWERED</span>
    <span class="badge">MULTI-LANGUAGE</span>
    <h1>🎛️ AI VIDEO ASSISTANT</h1>
    <p>&gt; transcribe // summarize // extract action items // chat with your meeting</p>
</div>
""", unsafe_allow_html=True)


# ---------------------------- Input section ----------------------------
st.markdown('<div class="section-label">01 // SOURCE INPUT</div>', unsafe_allow_html=True)

col_main, col_side = st.columns([2.2, 1])

with col_main:
    tab_link, tab_upload = st.tabs(["🔗  YouTube Link", "📁  Upload Video File"])

    source_path = None

    with tab_link:
        yt_url = st.text_input(
            "YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
            label_visibility="collapsed",
        )
        if yt_url:
            source_path = yt_url.strip()

    with tab_upload:
        uploaded_file = st.file_uploader(
            "Upload a video/audio file",
            type=["mp4", "mov", "mkv", "avi", "mp3", "wav", "m4a"],
            label_visibility="collapsed",
        )
        if uploaded_file is not None:
            tmp_dir = tempfile.gettempdir()
            tmp_path = os.path.join(tmp_dir, uploaded_file.name)
            with open(tmp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            source_path = tmp_path
            st.success(f"Loaded: {uploaded_file.name}")

with col_side:
    language = st.selectbox(
        "Language",
        options=["english", "hinglish"],
        format_func=lambda x: "🇬🇧 English" if x == "english" else "🇮🇳 Hinglish",
    )
    st.markdown("<br>", unsafe_allow_html=True)
    run_clicked = st.button("▶  RUN PIPELINE", use_container_width=True, disabled=not source_path)
    if not source_path:
        st.caption("↑ Provide a YouTube link or upload a file to enable this.")


# ---------------------------- Run pipeline ----------------------------
if run_clicked and source_path:
    st.session_state.processing = True
    with st.status("Running AI Video Assistant pipeline...", expanded=True) as status:
        st.write("📥 Processing input & chunking media...")
        st.write("🗣️ Transcribing audio...")
        st.write("🧠 Generating title, summary, action items, decisions, questions...")
        st.write("🔍 Building RAG chain for chat...")
        try:
            result = run_pipeline(source_path, language)
            st.session_state.result = result
            st.session_state.chat_history = []  # reset chat for new video
            status.update(label="✅ Pipeline complete", state="complete", expanded=False)
        except Exception as e:
            status.update(label="❌ Pipeline failed", state="error", expanded=True)
            st.error(f"Error: {e}")
            st.session_state.processing = False
    st.session_state.processing = False


# ---------------------------- Results ----------------------------
result = st.session_state.result

if result:
    st.markdown('<div class="section-label">02 // ANALYSIS OUTPUT</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <h3>📌 Title</h3>
        <p style="font-size:1.1rem; font-weight:600; color:#e6f1ff;">{result['title']}</p>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("Action Items", len(result["action_items"]) if hasattr(result["action_items"], "__len__") else "—")
    m2.metric("Key Decisions", len(result["key_decisions"]) if hasattr(result["key_decisions"], "__len__") else "—")
    m3.metric("Open Questions", len(result["open_questions"]) if hasattr(result["open_questions"], "__len__") else "—")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        <div class="card">
            <h3>📋 Summary</h3>
            <p>{result['summary']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <h3>✅ Action Items</h3>
            <p>{result['action_items']}</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
            <h3>🔑 Key Decisions</h3>
            <p>{result['key_decisions']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <h3>❓ Open Questions</h3>
            <p>{result['open_questions']}</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("📝 View Full Transcript"):
        st.markdown(f"<div class='card'><p>{result['transcript']}</p></div>", unsafe_allow_html=True)

    # ---------------------------- Chat with meeting (RAG) ----------------------------
    st.markdown('<div class="section-label">03 // CHAT WITH YOUR MEETING</div>', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_question = st.chat_input("Ask something about this video...")
    if user_question:
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.markdown(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_question(result["rag_chain"], user_question)
                st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

else:
    st.info("Provide a source above and hit **RUN PIPELINE** to get started.")