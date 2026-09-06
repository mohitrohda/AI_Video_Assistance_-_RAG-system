import streamlit as st
import time
from dotenv import load_dotenv

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.RAG_engine import build_rag_chain, ask_question

load_dotenv()

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------------
# Custom CSS — refined typography, animation, layout
# ------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 20% 0%, #101820 0%, #0a0d12 45%, #08090c 100%);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}

    /* ---------- Animations ---------- */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes shimmer {
        0%   { background-position: -400px 0; }
        100% { background-position: 400px 0; }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 0 rgba(88,166,255,0.0); }
        50%      { box-shadow: 0 0 24px rgba(88,166,255,0.25); }
    }
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes fadeIn {
        from { opacity: 0; } to { opacity: 1; }
    }

    .fade-in { animation: fadeInUp 0.55s ease both; }
    .fade-in-1 { animation: fadeInUp 0.55s ease 0.05s both; }
    .fade-in-2 { animation: fadeInUp 0.55s ease 0.15s both; }
    .fade-in-3 { animation: fadeInUp 0.55s ease 0.25s both; }
    .fade-in-4 { animation: fadeInUp 0.55s ease 0.35s both; }

    /* ---------- Header ---------- */
    .av-header {
        position: relative;
        padding: 2rem 2.2rem;
        border-radius: 18px;
        background: linear-gradient(120deg, #0f1720, #16202c, #101a24, #0f1720);
        background-size: 300% 300%;
        animation: gradientShift 12s ease infinite, fadeInUp 0.6s ease both;
        border: 1px solid #212d3b;
        margin-bottom: 1.6rem;
        overflow: hidden;
    }
    .av-header::after {
        content: "";
        position: absolute;
        top: -60%; right: -10%;
        width: 320px; height: 320px;
        background: radial-gradient(circle, rgba(88,166,255,0.15), transparent 70%);
        pointer-events: none;
    }
    .av-header h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -0.02em;
        color: #f0f4f8;
        margin-bottom: 0.35rem;
    }
    .av-header p {
        color: #8996a5;
        font-size: 1rem;
        font-weight: 400;
        margin: 0;
    }
    .av-badge {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 0.04em;
        color: #3fb950;
        background: rgba(63,185,80,0.1);
        border: 1px solid rgba(63,185,80,0.35);
        padding: 3px 10px;
        border-radius: 20px;
        margin-left: 10px;
        vertical-align: middle;
        animation: pulseGlow 3s ease-in-out infinite;
    }

    /* ---------- Input panel ---------- */
    .av-input-panel {
        background: linear-gradient(180deg, #121a23, #0f151d);
        border: 1px solid #1f2a37;
        border-radius: 16px;
        padding: 1.5rem 1.7rem;
        margin-bottom: 1.4rem;
        transition: border-color 0.3s ease;
    }
    .av-input-panel:hover {
        border-color: #2b3949;
    }
    .av-section-label {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 1.05rem;
        color: #e6edf3;
        margin-bottom: 0.9rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* ---------- Cards ---------- */
    .av-card {
        background: linear-gradient(180deg, #121a23, #0f151d);
        border: 1px solid #1f2a37;
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 1.1rem;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }
    .av-card:hover {
        transform: translateY(-3px);
        border-color: #375070;
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
    }
    .av-card h3 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 1.05rem;
        color: #6cb6ff;
        margin-bottom: 0.7rem;
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: -0.01em;
    }
    .av-card-body {
        color: #c3ccd6;
        font-size: 0.94rem;
        line-height: 1.6;
    }

    /* ---------- Pills ---------- */
    .av-pill {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #d7f5df;
        background: rgba(63,185,80,0.08);
        border: 1px solid rgba(63,185,80,0.3);
        padding: 4px 11px;
        border-radius: 999px;
        margin-right: 6px;
        margin-bottom: 4px;
        animation: fadeInUp 0.4s ease both;
    }

    /* ---------- Title reveal ---------- */
    .av-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.9rem;
        color: #f0f4f8;
        letter-spacing: -0.02em;
        margin: 1.6rem 0 1rem 0;
        animation: fadeInUp 0.5s ease both;
    }

    /* ---------- Chat ---------- */
    .chat-user {
        background: linear-gradient(135deg, #1c2530, #202b38);
        border-radius: 14px 14px 2px 14px;
        padding: 11px 16px;
        margin: 8px 0;
        color: #e6edf3;
        max-width: 78%;
        margin-left: auto;
        font-size: 0.93rem;
        line-height: 1.5;
        animation: fadeInUp 0.35s ease both;
    }
    .chat-bot {
        background: linear-gradient(135deg, #0f2a1f, #12331f);
        border: 1px solid #1f3a2c;
        border-radius: 14px 14px 14px 2px;
        padding: 11px 16px;
        margin: 8px 0;
        color: #e6edf3;
        max-width: 78%;
        font-size: 0.93rem;
        line-height: 1.5;
        animation: fadeInUp 0.35s ease both;
    }

    /* ---------- Buttons ---------- */
    .stButton>button {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        border-radius: 10px;
        border: 1px solid #2d3947;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(88,166,255,0.18);
    }
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #1f6feb, #388bfd);
        border: none;
    }

    /* ---------- Progress ---------- */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #1f6feb, #58a6ff, #1f6feb);
        background-size: 200% 100%;
        animation: shimmer 2s linear infinite;
    }
    .step-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #8996a5;
        animation: fadeIn 0.3s ease both;
    }

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 1px solid #1f2a37;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 500;
        font-size: 0.95rem;
        color: #8996a5;
        padding: 10px 6px;
    }
    .stTabs [aria-selected="true"] {
        color: #6cb6ff !important;
    }

    /* ---------- Text input / select ---------- */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        font-family: 'JetBrains Mono', monospace;
        border-radius: 10px !important;
    }

    /* ---------- Caption ---------- */
    .av-caption {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: #5b6570;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Session state
# ------------------------------------------------------------------
defaults = {
    "pipeline_result": None,
    "chat_history": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ------------------------------------------------------------------
# Pipeline runner with progress updates (same calls/order as run_pipeline)
# ------------------------------------------------------------------
def run_pipeline_with_progress(source: str, language: str, progress_bar, status_text) -> dict:
    status_text.markdown('<span class="step-label">[1/6] loading & chunking source...</span>', unsafe_allow_html=True)
    chunks = process_input(source)
    progress_bar.progress(15)

    status_text.markdown('<span class="step-label">[2/6] transcribing audio...</span>', unsafe_allow_html=True)
    transcript = transcribe_all(chunks, language)
    progress_bar.progress(40)

    status_text.markdown('<span class="step-label">[3/6] generating title...</span>', unsafe_allow_html=True)
    title = generate_title(transcript)
    progress_bar.progress(50)

    status_text.markdown('<span class="step-label">[4/6] summarizing transcript...</span>', unsafe_allow_html=True)
    summary = summarize(transcript)
    progress_bar.progress(65)

    status_text.markdown('<span class="step-label">[5/6] extracting action items, decisions & questions...</span>', unsafe_allow_html=True)
    action_item = extract_action_items(transcript)
    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)
    progress_bar.progress(85)

    status_text.markdown('<span class="step-label">[6/6] building RAG index...</span>', unsafe_allow_html=True)
    rag_chain = build_rag_chain(transcript)
    progress_bar.progress(100)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_item,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.markdown("""
<div class="av-header">
    <h1>🎙️ AI Video Assistant <span class="av-badge">RAG-POWERED</span></h1>
    <p>Transcribe → Summarize → Extract → Chat with any video or meeting</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Input panel (on home page)
# ------------------------------------------------------------------
st.markdown('<div class="av-input-panel fade-in-1">', unsafe_allow_html=True)
st.markdown('<div class="av-section-label">⚙️ Input Source</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    source = st.text_input("YouTube URL or local file path", placeholder="https://youtube.com/watch?v=...", label_visibility="collapsed")
with col2:
    language = st.selectbox("Language", ["english", "hinglish"], index=0, label_visibility="collapsed")
with col3:
    run_btn = st.button("🚀 Run Pipeline", use_container_width=True, type="primary")

if st.session_state.pipeline_result:
    st.markdown(
        '<span class="av-pill">✅ chunks processed</span>'
        '<span class="av-pill">✅ transcript ready</span>'
        '<span class="av-pill">✅ RAG index built</span>',
        unsafe_allow_html=True,
    )
    if st.button("🗑️ Reset session"):
        st.session_state.pipeline_result = None
        st.session_state.chat_history = []
        st.rerun()
else:
    st.markdown('<span class="av-caption">Awaiting input — paste a source above and run the pipeline.</span>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------
# Run pipeline
# ------------------------------------------------------------------
if run_btn:
    if not source.strip():
        st.error("Please provide a YouTube URL or local file path.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        with st.spinner("Processing..."):
            try:
                result = run_pipeline_with_progress(source.strip(), language, progress_bar, status_text)
                st.session_state.pipeline_result = result
                st.session_state.chat_history = []
                status_text.markdown('<span class="step-label">✅ done</span>', unsafe_allow_html=True)
                time.sleep(0.4)
                st.rerun()
            except Exception as e:
                st.error(f"Pipeline failed: {e}")

# ------------------------------------------------------------------
# Results
# ------------------------------------------------------------------
result = st.session_state.pipeline_result

if result:
    st.markdown(f'<div class="av-title fade-in">📌 {result["title"]}</div>', unsafe_allow_html=True)

    tab_summary, tab_transcript, tab_chat = st.tabs(
        ["📋  Summary & Insights", "📝  Full Transcript", "💬  Chat with Video"]
    )

    # ---- Summary tab ----
    with tab_summary:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f'''
                <div class="av-card fade-in-1">
                    <h3>📋 Summary</h3>
                    <div class="av-card-body">{result["summary"]}</div>
                </div>
            ''', unsafe_allow_html=True)

            st.markdown(f'''
                <div class="av-card fade-in-3">
                    <h3>✅ Action Items</h3>
                    <div class="av-card-body">{result["action_items"]}</div>
                </div>
            ''', unsafe_allow_html=True)

        with col2:
            st.markdown(f'''
                <div class="av-card fade-in-2">
                    <h3>🔑 Key Decisions</h3>
                    <div class="av-card-body">{result["key_decisions"]}</div>
                </div>
            ''', unsafe_allow_html=True)

            st.markdown(f'''
                <div class="av-card fade-in-4">
                    <h3>❓ Open Questions</h3>
                    <div class="av-card-body">{result["open_questions"]}</div>
                </div>
            ''', unsafe_allow_html=True)

    # ---- Transcript tab ----
    with tab_transcript:
        st.markdown('<div class="av-card fade-in"><h3>📝 Full Transcript</h3></div>', unsafe_allow_html=True)
        st.text_area("Transcript", result["transcript"], height=480, label_visibility="collapsed")
        st.download_button(
            "⬇️ Download transcript (.txt)",
            data=result["transcript"],
            file_name="transcript.txt",
            mime="text/plain",
        )

    # ---- Chat tab ----
    with tab_chat:
        st.markdown('<div class="av-card fade-in"><h3>💬 Chat with your video</h3></div>', unsafe_allow_html=True)

        for role, msg in st.session_state.chat_history:
            css_class = "chat-user" if role == "user" else "chat-bot"
            label = "You" if role == "user" else "🤖 Assistant"
            st.markdown(f'<div class="{css_class}"><b>{label}:</b> {msg}</div>', unsafe_allow_html=True)

        question = st.chat_input("Ask something about the video...")
        if question:
            st.session_state.chat_history.append(("user", question))
            with st.spinner("Thinking..."):
                answer = ask_question(result["rag_chain"], question)
            st.session_state.chat_history.append(("bot", answer))
            st.rerun()

else:
    st.markdown("""
    <div class="av-card fade-in-2">
        <h3>👋 Get started</h3>
        <div class="av-card-body">
        Paste a YouTube URL or local file path above and hit
        <b>Run Pipeline</b> to transcribe, summarize, and unlock chat with your video.
        </div>
    </div>
    """, unsafe_allow_html=True)