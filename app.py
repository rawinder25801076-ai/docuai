
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime

from services.document_reader import extract_text
from services.ai_engine import (
    ask_ai,
    summarize_document,
    answer_document,
    generate_study_notes
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "document_text": "",
    "document_name": "",
    "document_summary": "",
    "study_notes": "",
    "chat_history": [],
    "selected_page": "Dashboard"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# PREMIUM DASHBOARD UI
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
      radial-gradient(ellipse at 10% 5%, #252052 0%, transparent 40%),
      radial-gradient(ellipse at 90% 90%, #152a49 0%, transparent 40%),
      #080b16;
    color: #f5f5ff;
}

[data-testid="stSidebar"] {
    background: rgba(13, 16, 33, 0.98);
    border-right: 1px solid #292b4d;
}

h1, h2, h3 {
    color: #ffffff !important;
}

p, label, span {
    color: #c7c9dd;
}

/* HERO */

.hero {
    padding: 35px;
    border: 1px solid #49417e;
    border-radius: 24px;
    background: linear-gradient(
        120deg,
        #211b4b,
        #171c3a,
        #102d43
    );
    box-shadow: 0 10px 45px #0005;
    animation: appear 0.7s ease;
}

.hero h1 {
    font-size: clamp(30px, 5vw, 48px);
    font-weight: 800;
    background: linear-gradient(
        90deg,
        #ffffff,
        #b7a5ff,
        #65d9ff
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    font-size: 15px;
}

/* CARDS */

.card {
    padding: 23px;
    border-radius: 18px;
    background: linear-gradient(
        145deg,
        #171b32,
        #101426
    );
    border: 1px solid #303657;
    transition: all .3s ease;
    min-height: 145px;
}

.card:hover {
    transform: translateY(-5px);
    border-color: #987aff;
    box-shadow: 0 10px 30px #7857ff25;
}

.card h3 {
    font-size: 18px;
}

.card .number {
    font-size: 28px;
    font-weight: 800;
    color: #b7a0ff;
}

/* BUTTONS */

.stButton > button {
    border: 1px solid #8063ff;
    border-radius: 12px;
    background: linear-gradient(
        100deg,
        #6548e8,
        #318acb
    );
    color: white;
    font-weight: 700;
    min-height: 44px;
    transition: .25s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px #7955ff55;
    border-color: #bbaaff;
}

/* DOWNLOAD BUTTON */

.stDownloadButton > button {
    width: 100%;
    background: linear-gradient(
        100deg,
        #256b82,
        #3457a5
    );
    color: white;
    border: 1px solid #65b8e8;
    border-radius: 12px;
    font-weight: 700;
    min-height: 44px;
}

/* UPLOADER */

[data-testid="stFileUploader"] {
    border: 1px dashed #8a73ef;
    border-radius: 18px;
    padding: 15px;
    background: #171b32;
}

/* INPUTS */

.stTextArea textarea,
.stTextInput input {
    background: #151a2d !important;
    color: white !important;
    border: 1px solid #41466b !important;
    border-radius: 12px !important;
}

hr {
    border-color: #30334f;
}

[data-testid="stMetric"] {
    background: #151a2d;
    border: 1px solid #303657;
    padding: 15px;
    border-radius: 14px;
}

/* ANIMATION */

@keyframes appear {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* MOBILE */

@media (max-width: 768px) {

    .hero {
        padding: 22px;
    }

    .hero h1 {
        font-size: 30px;
    }

    .card {
        padding: 15px;
        min-height: 120px;
    }

    [data-testid="stMainBlockContainer"] {
        padding: 1rem;
    }
}

#MainMenu,
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# DOCUMENT LOADING HELPER
# ==========================================

def load_document(uploaded_file):

    try:

        text = extract_text(uploaded_file)

        if not text or not text.strip():

            st.error(
                "No readable text was found. "
                "This may be a scanned PDF or empty document."
            )

            return False

        st.session_state.document_text = text

        st.session_state.document_name = uploaded_file.name

        st.session_state.document_summary = ""

        st.session_state.study_notes = ""

        return True

    except Exception as error:

        st.error(f"Document reading error: {error}")

        return False


# ==========================================
# CHAT DOWNLOAD HELPER
# ==========================================

def create_chat_download():

    chat_text = "DOCUMIND AI - CHAT HISTORY\n"

    chat_text += "=" * 45 + "\n"

    chat_text += (
        f"Export date: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n\n"
    )

    for role, message in st.session_state.chat_history:

        if role == "user":
            chat_text += "YOU:\n"
        else:
            chat_text += "DOCUMIND AI:\n"

        chat_text += message + "\n\n"

        chat_text += "-" * 45 + "\n\n"

    return chat_text


# ==========================================
# SIDEBAR / TASKBAR
# ==========================================

menu_options = [
    "Dashboard",
    "My Documents",
    "Document Analysis",
    "Study Notes",
    "AI Chat",
    "Settings"
]

menu_icons = [
    "grid",
    "folder2-open",
    "file-earmark-text",
    "journal-bookmark",
    "chat-dots",
    "gear"
]

with st.sidebar:

    st.markdown("## 🧠 DocuMind AI")

    st.caption("Read Less. Understand More.")

    st.divider()

    st.markdown("### YOUR WORKSPACE")

    if st.session_state.selected_page not in menu_options:
        st.session_state.selected_page = "Dashboard"

    page = option_menu(
        menu_title=None,
        options=menu_options,
        icons=menu_icons,
        default_index=menu_options.index(
            st.session_state.selected_page
        ),
        styles={
            "container": {
                "background-color": "transparent"
            },
            "icon": {
                "color": "#a991ff"
            },
            "nav-link": {
                "color": "#d4d5e8",
                "border-radius": "10px",
                "margin": "5px"
            },
            "nav-link-selected": {
                "background-color": "#5541a5",
                "color": "white"
            }
        }
    )

    st.session_state.selected_page = page

    st.divider()

    st.caption("AI ENGINE")

    st.success("Groq AI Connected")

    st.caption("Powered by LangChain")

    st.divider()

    st.caption("DOCUMIND AI")

    st.caption("Version 1.2")


# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    st.markdown("""
    <div class="hero">

        <h1>Welcome to DocuMind AI ✨</h1>

        <p>
        Your personal intelligent document analysis
        and AI learning workspace.
        </p>

        <p>
        Read documents, understand complex topics
        and learn smarter with AI.
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # DASHBOARD STATISTICS

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Document Loaded",
            "Yes" if st.session_state.document_text else "No"
        )

    with c2:

        st.metric(
            "Chat Messages",
            len(st.session_state.chat_history)
        )

    with c3:

        st.metric(
            "AI Provider",
            "Groq AI"
        )

    st.write("")

    st.subheader("🚀 Quick Actions")

    a, b, c = st.columns(3)

    with a:

        st.markdown("""
        <div class="card">
            <h3>📄 Document Analysis</h3>
            <div class="number">Analyse</div>
            <p>Understand your PDF, DOCX and TXT files.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Open Document Analysis",
            key="dashboard_analysis",
            use_container_width=True
        ):

            st.session_state.selected_page = "Document Analysis"

            st.rerun()

    with b:

        st.markdown("""
        <div class="card">
            <h3>📖 Study Notes</h3>
            <div class="number">Learn</div>
            <p>Create structured and exam-friendly notes.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Open Study Notes",
            key="dashboard_notes",
            use_container_width=True
        ):

            st.session_state.selected_page = "Study Notes"

            st.rerun()

    with c:

        st.markdown("""
        <div class="card">
            <h3>💬 AI Assistant</h3>
            <div class="number">Chat</div>
            <p>Ask questions and learn with DocuMind AI.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Open AI Chat",
            key="dashboard_chat",
            use_container_width=True
        ):

            st.session_state.selected_page = "AI Chat"

            st.rerun()

    st.divider()

    st.subheader("📂 Current Document")

    if st.session_state.document_name:

        st.success(
            f"Currently loaded: {st.session_state.document_name}"
        )

        st.caption(
            f"{len(st.session_state.document_text):,} characters extracted"
        )

    else:

        st.info(
            "No document loaded yet. "
            "Upload a document in Document Analysis."
        )

    st.divider()

    st.caption(
        "DocuMind AI | Your intelligent document companion."
    )


# ==========================================
# DOCUMENT ANALYSIS
# ==========================================

elif page == "Document Analysis":

    st.title("📄 Document Analysis")

    st.caption(
        "Upload your document and let DocuMind AI understand it."
    )

    uploaded_file = st.file_uploader(
        "Choose a document",
        type=["pdf", "docx", "txt"],
        help="Supported formats: PDF, DOCX and TXT",
        key="analysis_upload"
    )

    if uploaded_file:

        if (
            st.session_state.document_name != uploaded_file.name
            or not st.session_state.document_text
        ):

            with st.spinner("Reading your document..."):

                load_document(uploaded_file)

    text = st.session_state.document_text

    if text:

        st.success(
            f"Document ready: {st.session_state.document_name}"
        )

        st.info(
            f"Extracted text: {len(text):,} characters"
        )

        with st.expander(
            "📖 View Extracted Document Content",
            expanded=True
        ):

            st.text_area(
                "Document text",
                text,
                height=300,
                disabled=True,
                key="analysis_document_preview"
            )

        st.divider()

        st.subheader("🧠 AI Document Analysis")

        if st.button(
            "✨ Generate Summary",
            use_container_width=True
        ):

            with st.spinner(
                "DocuMind AI is analysing your document..."
            ):

                summary = summarize_document(text)

                if summary and not summary.startswith("AI Error:"):

                    st.session_state.document_summary = summary

                else:

                    st.error(summary)

        if st.session_state.document_summary:

            st.subheader("📋 Document Summary")

            st.markdown(
                st.session_state.document_summary
            )

            st.download_button(
                "⬇️ Download Summary",
                data=st.session_state.document_summary,
                file_name="DocuMind_Summary.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.divider()

        st.subheader("💬 Ask Questions About Your Document")

        question = st.text_input(
            "Enter your question",
            placeholder="What are the main topics in this document?",
            key="document_question"
        )

        if st.button(
            "Ask DocuMind AI",
            use_container_width=True
        ):

            if question.strip():

                with st.spinner("Finding your answer..."):

                    answer = answer_document(text, question)

                if answer.startswith("AI Error:"):

                    st.error(answer)

                else:

                    st.markdown("### 🤖 AI Answer")

                    st.markdown(answer)

            else:

                st.warning("Please enter a question first.")

    else:

        st.info(
            "Upload a PDF, DOCX or TXT document to get started."
        )


# ==========================================
# STUDY NOTES
# ==========================================

elif page == "Study Notes":

    st.title("📖 AI Study Notes Generator")

    st.caption(
        "Turn lengthy documents into organized, easy-to-understand notes."
    )

    st.markdown("""
    <div class="hero">

        <h1>Study Smarter with AI ✨</h1>

        <p>
        Generate structured notes, important definitions,
        key points and revision questions from your documents.
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.session_state.document_text:

        st.success(
            f"Using uploaded document: {st.session_state.document_name}"
        )

        st.caption(
            f"{len(st.session_state.document_text):,} characters available"
        )

        if st.button(
            "🔄 Upload a Different Document",
            use_container_width=True
        ):

            st.session_state.document_text = ""

            st.session_state.document_name = ""

            st.session_state.document_summary = ""

            st.session_state.study_notes = ""

            st.rerun()

    else:

        st.info(
            "Upload a document here, or first upload one in Document Analysis."
        )

        uploaded_file = st.file_uploader(
            "Upload PDF, DOCX or TXT",
            type=["pdf", "docx", "txt"],
            key="study_notes_upload"
        )

        if uploaded_file:

            with st.spinner("Reading your document..."):

                load_document(uploaded_file)

            if st.session_state.document_text:

                st.rerun()

    if st.session_state.document_text:

        st.divider()

        st.subheader("🧠 Generate Your Study Notes")

        st.write(
            "DocuMind AI will organize your document into "
            "student-friendly notes."
        )

        if st.button(
            "✨ Generate Study Notes",
            use_container_width=True
        ):

            with st.spinner(
                "DocuMind AI is preparing your study notes..."
            ):

                notes = generate_study_notes(
                    st.session_state.document_text
                )

                if notes and not notes.startswith("AI Error:"):

                    st.session_state.study_notes = notes

                else:

                    st.error(notes)

        if st.session_state.study_notes:

            st.divider()

            st.subheader("📚 Your Study Notes")

            st.markdown(
                st.session_state.study_notes
            )

            st.divider()

            st.download_button(
                label="⬇️ Download Study Notes",
                data=st.session_state.study_notes,
                file_name="DocuMind_Study_Notes.txt",
                mime="text/plain",
                use_container_width=True
            )

            st.success("Your study notes are ready!")


# ==========================================
# MY DOCUMENTS
# ==========================================

elif page == "My Documents":

    st.title("📁 My Documents")

    st.caption(
        "Manage your currently loaded document."
    )

    if st.session_state.document_name:

        st.success("Current uploaded document")

        st.markdown(
            f"### 📄 {st.session_state.document_name}"
        )

        st.caption(
            f"{len(st.session_state.document_text):,} characters extracted"
        )

        if st.session_state.document_summary:

            st.write("✅ Summary generated")

        if st.session_state.study_notes:

            st.write("✅ Study notes generated")

        with st.expander("View document content"):

            st.text_area(
                "Document preview",
                st.session_state.document_text,
                height=250,
                disabled=True,
                key="library_preview"
            )

        if st.button(
            "🗑️ Clear Current Document",
            use_container_width=True
        ):

            st.session_state.document_text = ""

            st.session_state.document_name = ""

            st.session_state.document_summary = ""

            st.session_state.study_notes = ""

            st.rerun()

    else:

        st.info(
            "Your current document area is empty. "
            "Upload a document in Document Analysis."
        )


# ==========================================
# AI CHAT
# ==========================================

elif page == "AI Chat":

    st.title("💬 DocuMind AI Chat")

    st.caption(
        "Your intelligent AI assistant. Ask, learn and explore."
    )

    # CHAT HEADER

    st.markdown("""
    <div class="hero">

        <h1>Talk with DocuMind AI 🤖</h1>

        <p>
        Ask questions about technology, education,
        writing and general knowledge.
        </p>

        <p>
        Powered by Groq AI and LangChain.
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # CHAT ACTIONS

    chat_col1, chat_col2 = st.columns(2)

    with chat_col1:

        if st.session_state.chat_history:

            chat_download = create_chat_download()

            st.download_button(
                label="⬇️ Download Chat History",
                data=chat_download,
                file_name="DocuMind_AI_Chat.txt",
                mime="text/plain",
                use_container_width=True
            )

        else:

            st.button(
                "⬇️ Download Chat History",
                disabled=True,
                use_container_width=True
            )

    with chat_col2:

        if st.button(
            "🗑️ Clear Chat History",
            use_container_width=True
        ):

            st.session_state.chat_history = []

            st.rerun()

    st.divider()

    # DISPLAY OLD MESSAGES

    for role, message in st.session_state.chat_history:

        with st.chat_message(role):

            st.markdown(message)

    # NEW MESSAGE

    prompt = st.chat_input(
        "Ask DocuMind AI anything..."
    )

    if prompt:

        st.session_state.chat_history.append(
            ("user", prompt)
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner(
                "DocuMind AI is thinking..."
            ):

                answer = ask_ai(prompt)

                st.markdown(answer)

        st.session_state.chat_history.append(
            ("assistant", answer)
        )

        st.rerun()

    st.divider()

    st.caption(
        "Your chat is currently stored in this Streamlit session. "
        "Download it before closing the session if you want to keep a copy."
    )


# ==========================================
# SETTINGS
# ==========================================

elif page == "Settings":

    st.title("⚙️ Settings")

    st.subheader("Application Information")

    st.write("**Application:** DocuMind AI")

    st.write("**Version:** 1.2")

    st.write("**Frontend:** Python + Streamlit")

    st.write("**AI Framework:** LangChain")

    st.write("**AI Provider:** Groq API")

    st.write("**Document Processing:** PyMuPDF + python-docx")

    st.divider()

    st.subheader("Available Features")

    st.write("✅ PDF, DOCX and TXT Upload")

    st.write("✅ AI Document Summary")

    st.write("✅ Document Question Answering")

    st.write("✅ AI General Chat")

    st.write("✅ AI Study Notes Generator")

    st.write("✅ Download Chat History")

    st.write("✅ Clear Chat History")

    st.divider()

    st.subheader("Workspace Information")

    st.write(
        "Document and chat data currently use Streamlit session state."
    )

    st.caption(
        "Persistent accounts and private cloud document storage "
        "will be integrated in the next development stage."
    )

    st.caption(
        "DocuMind AI — Read Less. Understand More. Learn Smarter."
    )
