import streamlit as st
import os
import tempfile

from dotenv import load_dotenv

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions
)
from core.RAG_engine import build_rag_chain, ask_question


load_dotenv()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,0.15), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(168,85,247,0.12), transparent 25%),
        radial-gradient(circle at 50% 100%, rgba(6,182,212,0.08), transparent 30%),
        #050816;
    color: #f8fafc;
}


/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* Main container */

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* Header */

.hero {
    text-align: center;
    padding: 45px 20px 35px 20px;
}

.hero-badge {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 30px;

    background: rgba(99, 102, 241, 0.10);
    border: 1px solid rgba(129, 140, 248, 0.35);

    color: #a5b4fc;

    font-size: 13px;
    font-weight: 600;

    margin-bottom: 18px;

    box-shadow: 0 0 25px rgba(99, 102, 241, 0.08);
}

.hero-title {
    margin: 0;

    font-size: 58px;
    line-height: 1.1;

    font-weight: 800;
    letter-spacing: -2px;

    background: linear-gradient(
        90deg,
        #ffffff,
        #a5b4fc,
        #c084fc
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    margin-top: 18px;

    color: #94a3b8;

    font-size: 17px;
    line-height: 1.6;
}

.hero h1 {
    font-size: 55px;
    font-weight: 800;
    margin: 0;
    letter-spacing: -2px;
    background: linear-gradient(
        90deg,
        #ffffff,
        #a5b4fc,
        #c084fc
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #94a3b8;
    font-size: 17px;
    margin-top: 15px;
}


/* Glass cards */

.glass {
    background: rgba(15,23,42,0.68);
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 20px;
    padding: 25px;
    backdrop-filter: blur(20px);
    box-shadow:
        0 20px 60px rgba(0,0,0,0.25),
        inset 0 1px 0 rgba(255,255,255,0.03);
}


/* Input cards */

.input-card {
    background: linear-gradient(
        145deg,
        rgba(30,41,59,0.7),
        rgba(15,23,42,0.8)
    );
    border: 1px solid rgba(129,140,248,0.16);
    border-radius: 22px;
    padding: 30px;
    margin-top: 10px;
}


/* Section titles */

.section-title {
    font-size: 24px;
    font-weight: 700;
    margin: 25px 0 15px 0;
}

.section-subtitle {
    color: #94a3b8;
    font-size: 14px;
}


/* Metric cards */

.metric-card {
    background: rgba(15,23,42,0.75);
    border: 1px solid rgba(148,163,184,0.1);
    border-radius: 18px;
    padding: 20px;
    min-height: 110px;
}

.metric-icon {
    font-size: 25px;
}

.metric-title {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 8px;
}

.metric-value {
    font-size: 24px;
    font-weight: 700;
    color: white;
}


/* Result cards */

.result-card {
    background: rgba(15,23,42,0.65);
    border: 1px solid rgba(148,163,184,0.1);
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 18px;
}

.result-card h3 {
    margin-top: 0;
    color: #e2e8f0;
}

.result-content {
    color: #cbd5e1;
    line-height: 1.75;
}


/* Chat */

.chat-user {
    background: linear-gradient(
        135deg,
        rgba(79,70,229,0.25),
        rgba(99,102,241,0.12)
    );
    border: 1px solid rgba(129,140,248,0.2);
    border-radius: 18px;
    padding: 15px 20px;
    margin: 12px 0;
}

.chat-ai {
    background: rgba(15,23,42,0.8);
    border: 1px solid rgba(148,163,184,0.1);
    border-radius: 18px;
    padding: 15px 20px;
    margin: 12px 0;
}


/* Buttons */

.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid rgba(129,140,248,0.3);
    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    );
    color: white;
    font-weight: 700;
    padding: 12px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #a5b4fc;
    transform: translateY(-1px);
    box-shadow: 0 8px 30px rgba(99,102,241,0.25);
}


/* File uploader */

[data-testid="stFileUploader"] {
    background: rgba(15,23,42,0.5);
    border-radius: 15px;
}


/* Text inputs */

.stTextInput input {
    background: rgba(15,23,42,0.8) !important;
    color: white !important;
    border: 1px solid rgba(148,163,184,0.15) !important;
    border-radius: 12px !important;
}


/* Select box */

.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(15,23,42,0.8);
    border-radius: 12px;
}


/* Divider */

hr {
    border-color: rgba(148,163,184,0.1);
}


/* Footer */

.footer {
    text-align: center;
    color: #64748b;
    margin-top: 60px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []



# ============================================================
# HERO
# ============================================================

st.markdown(
"""
<style>
.hero {
    text-align: center;
    padding: 45px 20px 35px 20px;
}

.hero-badge {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 30px;
    background: rgba(99, 102, 241, 0.10);
    border: 1px solid rgba(129, 140, 248, 0.35);
    color: #a5b4fc;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 18px;
    box-shadow: 0 0 25px rgba(99, 102, 241, 0.08);
}

.hero-title {
    margin: 0;
    font-size: 58px;
    line-height: 1.1;
    font-weight: 800;
    letter-spacing: -2px;

    background: linear-gradient(
        90deg,
        #ffffff,
        #a5b4fc,
        #c084fc
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    margin-top: 18px;
    color: #94a3b8;
    font-size: 17px;
    line-height: 1.6;
}
</style>

<div class="hero">

<div class="hero-badge">
⚡ AI-POWERED VIDEO & MEETING INTELLIGENCE
</div>

<h1 class="hero-title">
AI Video Assistant
</h1>

<p class="hero-subtitle">
Turn long videos and meetings into searchable,
actionable intelligence.
</p>

</div>
""",
unsafe_allow_html=True
)

# ============================================================
# INPUT SECTION
# ============================================================

st.markdown("""
<div class="input-card">

<h2 style="margin-top:0;">
🎬 Analyze Your Video
</h2>

<p style="color:#94a3b8;">
Upload a video/audio file or paste a YouTube URL.
The AI will transcribe, summarize and extract insights.
</p>

</div>
""", unsafe_allow_html=True)


tab1, tab2 = st.tabs([
    "📁 Upload Video / Audio",
    "🔗 YouTube URL"
])


source = None


# ============================================================
# FILE UPLOAD
# ============================================================

with tab1:

    uploaded_file = st.file_uploader(
        "Upload your video or audio",
        type=[
            "mp4",
            "mp3",
            "wav",
            "m4a",
            "mov",
            "avi",
            "mkv"
        ],
        help="Supported formats: MP4, MP3, WAV, M4A, MOV, AVI, MKV"
    )

    if uploaded_file:

        st.success(
            f"✓ {uploaded_file.name} ready for processing"
        )

        # Save uploaded file temporarily
        temp_dir = tempfile.gettempdir()

        file_path = os.path.join(
            temp_dir,
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        source = file_path


# ============================================================
# YOUTUBE INPUT
# ============================================================

with tab2:

    youtube_url = st.text_input(
        "Paste YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed"
    )

    if youtube_url:

        source = youtube_url

        st.info(
            "🔗 YouTube video detected. Audio will be processed automatically."
        )


# ============================================================
# SETTINGS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:

    language = st.selectbox(
        "🌐 Language",
        [
            "english",
            "hinglish"
        ]
    )


with col2:

    st.markdown(
        """
        <div style="
            padding-top:32px;
            color:#64748b;
            font-size:13px;
        ">
        💡 Choose <b>Hinglish</b> for Hindi-English mixed conversations.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

analyze = st.button(
    "🚀 Analyze Video",
    use_container_width=True
)


# ============================================================
# PIPELINE
# ============================================================

if analyze:

    if not source:

        st.warning(
            "⚠️ Please upload a video/audio file or enter a YouTube URL."
        )

    else:

        st.session_state.chat_history = []

        progress = st.progress(0)

        status = st.empty()

        try:

            # ----------------------------------------
            # Step 1
            # ----------------------------------------

            status.info("🎧 Processing video/audio...")

            chunks = process_input(source)

            progress.progress(20)


            # ----------------------------------------
            # Step 2
            # ----------------------------------------

            status.info("🎙️ Transcribing with AI...")

            transcript = transcribe_all(
                chunks,
                language
            )

            progress.progress(40)


            # ----------------------------------------
            # Step 3
            # ----------------------------------------

            status.info("🧠 Generating title and summary...")

            title = generate_title(transcript)

            summary = summarize(transcript)

            progress.progress(60)


            # ----------------------------------------
            # Step 4
            # ----------------------------------------

            status.info("🔍 Extracting meeting intelligence...")

            action_items = extract_action_items(
                transcript
            )

            decisions = extract_key_decisions(
                transcript
            )

            questions = extract_questions(
                transcript
            )

            progress.progress(80)


            # ----------------------------------------
            # Step 5
            # ----------------------------------------

            status.info("🔗 Building RAG knowledge base...")

            rag_chain = build_rag_chain(
                transcript
            )

            progress.progress(100)

            status.success(
                "✅ Analysis completed successfully!"
            )


            # ----------------------------------------
            # Store result
            # ----------------------------------------

            st.session_state.result = {
                "title": title,
                "transcript": transcript,
                "summary": summary,
                "action_items": action_items,
                "key_decisions": decisions,
                "open_questions": questions,
                "rag_chain": rag_chain
            }

            st.rerun()

        except Exception as e:

            st.error(
                f"❌ Something went wrong:\n\n{str(e)}"
            )


# ============================================================
# RESULTS
# ============================================================

result = st.session_state.result


if result:

    st.markdown("---")

    # ========================================================
    # TITLE
    # ========================================================

    st.markdown(
        f"""
        <div class="glass">

        <div style="
            color:#818cf8;
            font-size:13px;
            font-weight:600;
            margin-bottom:8px;
        ">
        AI GENERATED TITLE
        </div>

        <h1 style="
            margin:0;
            font-size:32px;
        ">
        {result["title"]}
        </h1>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # METRICS
    # ========================================================

    transcript_length = len(
        result["transcript"]
    )

    word_count = len(
        result["transcript"].split()
    )

    c1, c2, c3, c4 = st.columns(4)


    with c1:
        st.markdown(
            f"""
            <div class="metric-card">

            <div class="metric-icon">📝</div>

            <div class="metric-title">
            Transcript
            </div>

            <div class="metric-value">
            {transcript_length:,}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:
        st.markdown(
            f"""
            <div class="metric-card">

            <div class="metric-icon">🔤</div>

            <div class="metric-title">
            Words
            </div>

            <div class="metric-value">
            {word_count:,}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c3:
        st.markdown(
            """
            <div class="metric-card">

            <div class="metric-icon">⚡</div>

            <div class="metric-title">
            AI Analysis
            </div>

            <div class="metric-value">
            Complete
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c4:
        st.markdown(
            """
            <div class="metric-card">

            <div class="metric-icon">🧠</div>

            <div class="metric-title">
            RAG Chat
            </div>

            <div class="metric-value">
            Ready
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # SUMMARY
    # ========================================================

    st.markdown(
        '<div class="section-title">📋 AI Summary</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="result-card">

        <div class="result-content">

        {result["summary"]}

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # INSIGHTS
    # ========================================================

    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            '<div class="section-title">✅ Action Items</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="result-card">

            <div class="result-content">

            {result["action_items"]}

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            '<div class="section-title">🔑 Key Decisions</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="result-card">

            <div class="result-content">

            {result["key_decisions"]}

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # OPEN QUESTIONS
    # ========================================================

    st.markdown(
        '<div class="section-title">❓ Open Questions</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="result-card">

        <div class="result-content">

        {result["open_questions"]}

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # TRANSCRIPT
    # ========================================================

    st.markdown(
        '<div class="section-title">📝 Full Transcript</div>',
        unsafe_allow_html=True
    )

    with st.expander(
        "Open full transcript"
    ):

        st.text_area(
            "Transcript",
            result["transcript"],
            height=500,
            label_visibility="collapsed"
        )


    # ========================================================
    # RAG CHAT
    # ========================================================

    st.markdown("---")

    st.markdown(
        """
        <div class="hero" style="padding:25px 0;">

        <div class="hero-badge">
        🧠 RETRIEVAL AUGMENTED GENERATION
        </div>

        <h1 style="font-size:38px;">
        Chat With Your Video
        </h1>

        <p>
        Ask anything about the uploaded meeting or video.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # Existing chat history

    for role, message in st.session_state.chat_history:

        if role == "user":

            st.markdown(
                f"""
                <div class="chat-user">

                <b>👤 You</b>

                <br><br>

                {message}

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="chat-ai">

                <b>🤖 AI Assistant</b>

                <br><br>

                {message}

                </div>
                """,
                unsafe_allow_html=True
            )


    # Chat input

    question = st.chat_input(
        "Ask something about your video..."
    )


    if question:

        st.session_state.chat_history.append(
            ("user", question)
        )

        with st.spinner(
            "🧠 Searching your video..."
        ):

            try:

                answer = ask_question(
                    result["rag_chain"],
                    question
                )

            except Exception as e:

                answer = f"Error: {str(e)}"


        st.session_state.chat_history.append(
            ("assistant", answer)
        )

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    Built with Python • Streamlit • Whisper • RAG • AI

    </div>
    """,
    unsafe_allow_html=True
)