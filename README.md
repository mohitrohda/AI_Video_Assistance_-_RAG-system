# 🤖 AI Video Assistant - Meeting Intelligence & RAG

An AI-powered meeting intelligence application that transforms meeting
videos into searchable, actionable knowledge.

The **AI Video Assistant** accepts a YouTube meeting URL or a local
video file, transcribes the audio, generates structured meeting
insights, and creates a RAG-powered chat interface so users can ask
questions about the meeting.

------------------------------------------------------------------------

## ✨ Features

### 🎙️ Multilingual Transcription

-   Process meeting videos from a **YouTube URL** or uploaded local
    video.
-   Transcribe meeting audio using **Whisper** and **Sarvam AI**.
-   Supports **English and Hindi** transcription.

### 📝 Meeting Intelligence

Automatically generate useful information from the meeting: - Meeting
title - Summary - Action items - Key decisions - Open questions

### 🔎 RAG-Powered Meeting Chat

The project implements a **Retrieval-Augmented Generation (RAG)**
pipeline that allows users to interact with their meeting content.

Users can ask questions such as:

-   What were the key decisions?
-   What action items were assigned?
-   What topics were discussed?
-   What questions remain unresolved?

The system retrieves relevant meeting information and uses the LLM to
generate an answer based on the retrieved context.

### 📄 Report Export

Meeting insights can be exported as: - PDF - Text

### 🌐 Interactive Interface

The application provides a **Streamlit** interface for: - Selecting a
video source - Selecting the language - Running the AI pipeline -
Viewing processing progress - Accessing generated meeting insights -
Interacting with the RAG system

------------------------------------------------------------------------

## 🧠 How It Works

``` text
                ┌─────────────────────┐
                │   Meeting Source    │
                │ YouTube url / Local     │
                │       Video         │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Media Processing   │
                │   & Chunking        │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Transcription    │
                │ Whisper / Sarvam AI │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Meeting Analysis    │
                │     Mistral AI      │
                │    + LangChain      │
                └──────────┬──────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
   ┌───────────────────┐       ┌───────────────────┐
   │ Structured        │       │ RAG Pipeline      │
   │ Meeting Insights  │       │ Embeddings        │
   │                   │       │ + ChromaDB        │
   │ • Summary         │       └─────────┬─────────┘
   │ • Action Items    │                 │
   │ • Decisions       │                 ▼
   │ • Questions       │       ┌───────────────────┐
   └─────────┬─────────┘       │ Meeting Q&A       │
             │                 │    with LLM       │
             │                 └───────────────────┘
             ▼
   ┌───────────────────┐
   │ PDF / Text Export │
   └───────────────────┘
```

------------------------------------------------------------------------

## 🛠️ Tech Stack

  -----------------------------------------------------------------------
  Category                            Technologies
  ----------------------------------- -----------------------------------
  Programming Language                Python

  LLM                                 Mistral AI

  Speech-to-Text                      Whisper, Sarvam AI

  GenAI Framework                     LangChain, LangChain Expression
                                      Language (LCEL)

  RAG                                 Retrieval-Augmented Generation

  Embeddings                          HuggingFace Embeddings

  Vector Database                     ChromaDB

  Frontend                            Streamlit

  AI Engineering                      Text Chunking, Embeddings, Semantic
                                      Search, Retrieval Pipelines

  Output                              PDF / Text Reports
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🔄 RAG Pipeline

The RAG component follows a retrieval-based workflow:

``` text
Meeting Transcript
       │
       ▼
Text Processing
       │
       ▼
Text Chunking
       │
       ▼
HuggingFace Embeddings
       │
       ▼
ChromaDB Vector Store
       │
       ▼
User Question
       │
       ▼
Semantic Retrieval
       │
       ▼
Relevant Meeting Context
       │
       ▼
Mistral AI
       │
       ▼
Grounded Answer
```

This makes the meeting content searchable instead of requiring users to
manually scan the complete transcript.

------------------------------------------------------------------------

## ⚙️ Installation

### 1. Clone the repository

``` bash
git clone <"https://github.com/mohitrohda/AI_Video_Assistance.git">
cd AI-Video-Assistant
```

### 2. Create a virtual environment

``` bash
python -m venv venv
```

Activate it:

**macOS / Linux**

``` bash
source venv/bin/activate
```

**Windows**

``` bash
venv\Scripts\activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file and add the API credentials required by your
implementation.

Example:

``` env
MISTRAL_API_KEY=your_mistral_api_key
SARVAM_API_KEY=your_sarvam_api_key
```

> Add or rename environment variables according to the configuration
> used in your code. Never commit API keys to GitHub.

### 5. Run the application

``` bash
streamlit run app.py
```

The application will open in your browser.

------------------------------------------------------------------------

## 💡 Example Use Case

Imagine a 60-minute project meeting.

Instead of manually watching the entire recording, the AI Video
Assistant can process the meeting and provide:

**Summary** \> A concise overview of the discussion.

**Action Items** \> Tasks that need to be completed after the meeting.

**Key Decisions** \> Important decisions made during the discussion.

**Open Questions** \> Topics that still require clarification.

You can then ask the RAG system questions about the meeting instead of
searching through the complete recording manually.

------------------------------------------------------------------------

## 🎯 Why I Built This

Meetings contain a large amount of valuable information, but that
information is often difficult to access after the meeting ends.

I built this project to explore how **Generative AI, speech-to-text,
LLMs, embeddings, vector databases, and RAG** can work together to turn
unstructured meeting recordings into an interactive knowledge system.

The project also gave me hands-on experience with an end-to-end GenAI
workflow:

``` text
Raw Video
   ↓
Speech-to-Text
   ↓
Transcript
   ↓
LLM Analysis
   ↓
Structured Insights
   ↓
Embeddings
   ↓
Vector Database
   ↓
RAG
   ↓
Interactive Meeting Assistant
```

------------------------------------------------------------------------

## 🚀 Future Improvements

Potential improvements include:

-   Advanced RAG evaluation
-   Hybrid search
-   Better retrieval strategies
-   Conversation memory
-   Speaker identification
-   Timestamp-based answers
-   Meeting comparison across multiple recordings
-   Authentication and user-specific meeting storage
-   Production deployment
-   Monitoring and observability
-   Improved multilingual support

------------------------------------------------------------------------

## 🔑 Key Concepts Demonstrated

This project demonstrates practical experience with:

-   Generative AI
-   Large Language Models (LLMs)
-   Retrieval-Augmented Generation (RAG)
-   Speech-to-Text
-   Prompt Engineering
-   LangChain
-   LCEL
-   Embeddings
-   Vector Search
-   ChromaDB
-   Semantic Search
-   Text Chunking
-   Document Processing
-   NLP
-   AI Application Development
-   Streamlit

------------------------------------------------------------------------

## 👨‍💻 Author

**Mohit Rohda**

AI/ML Engineer \| Generative AI \| RAG \| NLP \| Deep Learning

-   LinkedIn: \[https://www.linkedin.com/in/mohit-rohda/]
-   GitHub: \[https://github.com/mohitrohda]

