import os
import textwrap
from typing import Any

import streamlit as st
from dotenv import load_dotenv

from langchain.agents import create_agent as langchain_create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from tools.hospitals_tool import get_hospitals_tool
from tools.institutions_tool import get_institutions_tool
from tools.restaurants_tool import get_restaurants_tool
from tools.web_search_tool import get_web_search_tool


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


st.set_page_config(
    page_title="Bangladesh AI",
    page_icon="🇧🇩",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None


# ============================================================
# HTML HELPER
# ============================================================

def render_html(html: str):
    st.markdown(
        textwrap.dedent(html),
        unsafe_allow_html=True,
    )


# ============================================================
# DESIGN SYSTEM (BANGLADESH FLAG THEME + HIGH CONTRAST)
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   GOOGLE FONT IMPORT
   ============================================================ */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ============================================================
   BANGLADESH FLAG PALETTE & ADAPTIVE STYLING
   ============================================================ */
:root {
    --bd-green: #006a4e;
    --bd-green-dark: #004d38;
    --bd-green-deep: #002e22;
    --bd-green-light: rgba(0, 106, 78, 0.08);
    --bd-green-border: rgba(0, 106, 78, 0.2);
    
    --bd-red: #f42a41;
    --bd-red-dark: #d01d32;
    --bd-red-light: rgba(244, 42, 65, 0.08);
    --bd-red-border: rgba(244, 42, 65, 0.25);
}

/* Base Body & Reset */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

code, pre, .stCode {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Hide Streamlit Header/Footer Clutter while preserving layout */
#MainMenu, footer, header {
    visibility: hidden;
}

/* Container Adjustments */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 6rem;
}

/* Smooth Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: var(--bd-green-border);
    border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--bd-green);
}

/* ============================================================
   SIDEBAR & TOGGLE FIXES
   ============================================================ */
/* Ensure native Streamlit toggle stays visible & accessible */
[data-testid="stSidebarCollapseButton"], 
[data-testid="stSidebarExpandButton"] {
    z-index: 999999 !important;
    visibility: visible !important;
}

section[data-testid="stSidebar"] {
    border-right: 1px solid var(--bd-green-border);
}

section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem;
}

/* Brand Display */
.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: var(--bd-green-light);
    border: 1px solid var(--bd-green-border);
    border-radius: 14px;
    margin-bottom: 16px;
}

.brand-logo {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: radial-gradient(circle, var(--bd-red) 0%, var(--bd-red) 36%, var(--bd-green) 37%, var(--bd-green) 100%);
    font-size: 22px;
    box-shadow: 0 4px 14px rgba(0, 106, 78, 0.25);
    flex-shrink: 0;
}

.brand-name {
    font-size: 17px;
    font-weight: 800;
    line-height: 1.2;
    letter-spacing: -0.3px;
    color: var(--bd-green-dark);
}

.brand-subtitle {
    font-size: 11px;
    font-weight: 600;
    opacity: 0.75;
    margin-top: 2px;
}

/* Online Status */
.online-status {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 50px;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #059669;
    font-size: 11px;
    font-weight: 800;
    margin-bottom: 20px;
}

.online-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}

/* Sidebar Section Headers */
.sidebar-title {
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.9px;
    opacity: 0.7;
    margin: 20px 4px 10px;
}

/* Sidebar Tool Item */
.sidebar-tool {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    margin-bottom: 8px;
    border: 1px solid var(--bd-green-border);
    border-radius: 12px;
    background: var(--bd-green-light);
    transition: all 0.2s ease;
}

.sidebar-tool:hover {
    border-color: var(--bd-green);
    transform: translateX(3px);
}

.sidebar-tool-icon {
    width: 34px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: var(--bd-green);
    color: #ffffff;
    font-size: 16px;
    flex-shrink: 0;
}

.sidebar-tool-name {
    font-size: 12px;
    font-weight: 700;
}

.sidebar-tool-description {
    font-size: 10px;
    opacity: 0.75;
    line-height: 1.3;
    margin-top: 1px;
}

/* Info Box */
.sidebar-info {
    padding: 12px;
    border: 1px solid var(--bd-green-border);
    border-radius: 12px;
    background: var(--bd-green-light);
}

.sidebar-info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 0;
}

.sidebar-info-label {
    font-size: 11px;
    opacity: 0.75;
}

.sidebar-info-value {
    color: var(--bd-green);
    font-size: 11px;
    font-weight: 800;
}

/* Sidebar Button Styling */
section[data-testid="stSidebar"] div.stButton > button {
    min-height: 40px;
    border-radius: 10px;
    border: 1px solid var(--bd-red-border);
    background: var(--bd-red-light);
    color: var(--bd-red);
    font-size: 12px;
    font-weight: 700;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] div.stButton > button:hover {
    border-color: var(--bd-red);
    background: var(--bd-red);
    color: #ffffff;
}

/* ============================================================
   HERO BANNER (BANGLADESH GREEN & RED ACCENT)
   ============================================================ */
.hero {
    position: relative;
    overflow: hidden;
    padding: 36px;
    border-radius: 20px;
    background: linear-gradient(135deg, var(--bd-green-deep) 0%, var(--bd-green) 65%, #008a66 100%);
    color: #ffffff !important;
    margin-bottom: 24px;
    box-shadow: 0 16px 36px -10px rgba(0, 106, 78, 0.3);
}

.hero::before {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    right: -40px;
    top: -80px;
    border-radius: 50%;
    background: radial-gradient(circle, var(--bd-red) 0%, transparent 70%);
    opacity: 0.85;
    pointer-events: none;
}

.hero::after {
    content: "🇧🇩";
    position: absolute;
    right: 24px;
    bottom: 10px;
    font-size: 76px;
    opacity: 0.15;
    pointer-events: none;
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-small {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #a7f3d0;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.hero-title {
    font-size: 32px;
    line-height: 1.2;
    font-weight: 800;
    letter-spacing: -0.8px;
    color: #ffffff !important;
    margin: 0;
}

.hero-description {
    max-width: 620px;
    font-size: 14px;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.9) !important;
    margin-top: 10px;
}

/* ============================================================
   STATISTICS GRID
   ============================================================ */
.stat-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 28px;
}

.stat-card {
    padding: 16px;
    border: 1px solid var(--bd-green-border);
    border-radius: 16px;
    background: var(--bd-green-light);
    transition: all 0.25s ease;
}

.stat-card:hover {
    transform: translateY(-3px);
    border-color: var(--bd-green);
    box-shadow: 0 10px 25px -5px rgba(0, 106, 78, 0.15);
}

.stat-icon {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    background: var(--bd-green);
    color: #ffffff;
    font-size: 16px;
    margin-bottom: 10px;
}

.stat-value {
    color: var(--bd-green);
    font-size: 22px;
    font-weight: 800;
    line-height: 1;
}

.stat-label {
    font-size: 11px;
    font-weight: 600;
    opacity: 0.75;
    margin-top: 4px;
}

/* ============================================================
   EMPTY STATE & PROMPTS
   ============================================================ */
.empty-state {
    text-align: center;
    padding: 20px 0 24px;
}

.empty-icon {
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 12px;
    border-radius: 18px;
    background: var(--bd-green-light);
    border: 1px solid var(--bd-green-border);
    font-size: 30px;
}

.empty-title {
    font-size: 18px;
    font-weight: 800;
}

.empty-description {
    font-size: 12px;
    opacity: 0.75;
    max-width: 420px;
    line-height: 1.5;
    margin: 6px auto 0;
}

/* Main Area Action Buttons */
div.stButton > button {
    min-height: 48px;
    border: 1px solid var(--bd-green-border);
    border-radius: 12px;
    background: var(--bd-green-light);
    font-size: 12px;
    font-weight: 700;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    border-color: var(--bd-green);
    background: var(--bd-green);
    color: #ffffff !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 106, 78, 0.2);
}

/* ============================================================
   CHAT LOG & INTERFACE
   ============================================================ */
[data-testid="stChatMessage"] {
    padding: 8px 0;
    background: transparent;
}

[data-testid="stChatMessageContent"] {
    font-size: 14px;
    line-height: 1.65;
}

/* User Bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
    background: var(--bd-green-light);
    border: 1px solid var(--bd-green-border);
    border-radius: 16px 16px 4px 16px;
    padding: 12px 16px;
}

/* Assistant Bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"] {
    background: rgba(0, 106, 78, 0.03);
    border: 1px solid var(--bd-green-border);
    border-left: 4px solid var(--bd-green);
    border-radius: 4px 16px 16px 16px;
    padding: 12px 16px;
}

/* Chat Input Styling */
[data-testid="stChatInput"] {
    border-radius: 14px !important;
    border: 1px solid var(--bd-green-border) !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: var(--bd-green) !important;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 11px;
    font-weight: 600;
    opacity: 0.6;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid var(--bd-green-border);
}

/* Responsive Grid Rules */
@media (max-width: 768px) {
    .stat-row {
        grid-template-columns: repeat(2, 1fr);
    }
    .hero {
        padding: 24px;
    }
    .hero-title {
        font-size: 24px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# MODEL
# ============================================================

def create_model():

    if not GOOGLE_API_KEY:

        raise RuntimeError(
            "GOOGLE_API_KEY is missing. "
            "Please add it to your .env file."
        )

    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=GOOGLE_API_KEY,
    )


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are Bangladesh AI, a helpful AI assistant focused on
Bangladesh-related information.

You have access to four tools:

1. InstitutionsDBTool
2. HospitalsDBTool
3. RestaurantsDBTool
4. WebSearchTool


============================================================
INSTITUTIONS
============================================================

Use InstitutionsDBTool for Bangladesh institution data,
including:

- schools
- colleges
- universities
- EIIN
- institution types
- divisions
- districts
- upazilas
- unions
- management types


============================================================
HOSPITALS
============================================================

Use HospitalsDBTool for Bangladesh hospital records,
including:

- hospital name
- location
- type
- division
- district
- city corporation
- upazila
- public/private status

IMPORTANT:

Never claim that the hospital database contains:

- number of beds
- doctors
- phone numbers
- departments

unless that information is actually returned by the tool.


============================================================
RESTAURANTS
============================================================

Use RestaurantsDBTool for:

- restaurant searches
- restaurant counts
- locations
- cuisine
- ratings


============================================================
WEB SEARCH
============================================================

Use WebSearchTool for:

- current events
- latest information
- general knowledge
- government policies
- definitions
- information missing from the database


============================================================
TOOL SELECTION
============================================================

Use the database tools when the user asks about
specific Bangladesh database records.

Use WebSearchTool when:

- information is current
- the user asks for latest news
- the information is not available in the database
- the question requires general web knowledge


============================================================
RESPONSE STYLE
============================================================

Be concise, friendly, accurate, and natural.

Use:

- tables for multi-row data
- bullet points for lists
- clear counts
- short explanations

Never invent database information.

If the database does not contain requested information,
clearly explain that limitation.

For current information, prefer WebSearchTool.
"""


# ============================================================
# BUILD AGENT
# ============================================================

def build_agent():

    llm = create_model()

    tools = [
        get_institutions_tool(llm),
        get_hospitals_tool(llm),
        get_restaurants_tool(llm),
    ]

    if TAVILY_API_KEY:

        tools.append(
            get_web_search_tool()
        )

    return langchain_create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )


# ============================================================
# GET AGENT
# ============================================================

def get_agent():

    if st.session_state.agent is None:

        st.session_state.agent = build_agent()

    return st.session_state.agent


# ============================================================
# NORMALIZE CONTENT
# ============================================================

def normalize_content(
    content: Any,
) -> str:

    if content is None:
        return ""

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):

        parts = []

        for item in content:

            if isinstance(item, str):

                parts.append(item)

            elif isinstance(item, dict):

                if "text" in item:

                    parts.append(
                        str(item["text"])
                    )

                elif "content" in item:

                    parts.append(
                        str(item["content"])
                    )

            else:

                parts.append(
                    str(item)
                )

        return "\n".join(parts).strip()

    return str(content).strip()


# ============================================================
# RUN AGENT
# ============================================================

def run_agent() -> str:

    agent = get_agent()

    history = []

    for message in st.session_state.messages:

        role = message.get("role")

        content = message.get(
            "content",
            "",
        )

        if role in (
            "user",
            "assistant",
        ):

            history.append(
                {
                    "role": role,
                    "content": content,
                }
            )

    result = agent.invoke(
        {
            "messages": history
        }
    )

    result_messages = result.get(
        "messages",
        [],
    )

    if not result_messages:

        raise RuntimeError(
            "The agent returned no messages."
        )

    answer = ""

    for message in reversed(
        result_messages
    ):

        message_type = getattr(
            message,
            "type",
            "",
        )

        if message_type == "ai":

            answer = normalize_content(
                getattr(
                    message,
                    "content",
                    "",
                )
            )

            if answer:
                break

    if not answer:

        answer = normalize_content(
            getattr(
                result_messages[-1],
                "content",
                "",
            )
        )

    return (
        answer
        or
        "Sorry, I couldn't generate a response."
    )


# ============================================================
# HANDLE USER QUERY
# ============================================================

def handle_user_query(
    query_text: str,
):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query_text,
        }
    )

    try:

        with st.spinner(
            "Bangladesh AI is thinking..."
        ):

            answer = run_agent()

    except Exception as error:

        answer = (
            "### ❌ Something went wrong\n\n"
            "```text\n"
            f"{str(error)}"
            "\n```"
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # Brand Title
    render_html(
        """
        <div class="brand">
            <div class="brand-logo">🇧🇩</div>
            <div>
                <div class="brand-name">Bangladesh AI</div>
                <div class="brand-subtitle">Your local AI assistant</div>
            </div>
        </div>
        """
    )

    # Online Status
    if GOOGLE_API_KEY:
        render_html(
            """
            <div class="online-status">
                <span class="online-dot"></span>
                AI SYSTEM ONLINE
            </div>
            """
        )
    else:
        st.error("Google API key is missing.")

    # Data Tools Title
    render_html(
        """
        <div class="sidebar-title">Data Tools</div>
        """
    )

    # Data Tools List
    render_html(
        """
        <div class="sidebar-tool">
            <div class="sidebar-tool-icon">🏛️</div>
            <div>
                <div class="sidebar-tool-name">Institutions</div>
                <div class="sidebar-tool-description">Schools, colleges & universities</div>
            </div>
        </div>

        <div class="sidebar-tool">
            <div class="sidebar-tool-icon">🏥</div>
            <div>
                <div class="sidebar-tool-name">Hospitals</div>
                <div class="sidebar-tool-description">Locations & hospital types</div>
            </div>
        </div>

        <div class="sidebar-tool">
            <div class="sidebar-tool-icon">🍽️</div>
            <div>
                <div class="sidebar-tool-name">Restaurants</div>
                <div class="sidebar-tool-description">Restaurants, cuisines & ratings</div>
            </div>
        </div>

        <div class="sidebar-tool">
            <div class="sidebar-tool-icon">🌐</div>
            <div>
                <div class="sidebar-tool-name">Web Search</div>
                <div class="sidebar-tool-description">Current information & news</div>
            </div>
        </div>
        """
    )

    # System Section
    render_html(
        """
        <div class="sidebar-title">System</div>
        """
    )

    render_html(
        f"""
        <div class="sidebar-info">
            <div class="sidebar-info-row">
                <span class="sidebar-info-label">AI Model</span>
                <span class="sidebar-info-value">Gemini 3.5 Flash</span>
            </div>
            <div class="sidebar-info-row">
                <span class="sidebar-info-label">Agent</span>
                <span class="sidebar-info-value">LangChain</span>
            </div>
            <div class="sidebar-info-row">
                <span class="sidebar-info-label">Web Search</span>
                <span class="sidebar-info-value">{"Enabled" if TAVILY_API_KEY else "Disabled"}</span>
            </div>
            <div class="sidebar-info-row">
                <span class="sidebar-info-label">Messages</span>
                <span class="sidebar-info-value">{len(st.session_state.messages)}</span>
            </div>
        </div>
        """
    )

    # Conversation Clear Title & Action
    render_html(
        """
        <div class="sidebar-title">Conversation</div>
        """
    )

    if st.button("🗑️  Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.agent = None
        st.rerun()


# ============================================================
# MAIN HERO BANNER
# ============================================================

render_html(
    """
    <div class="hero">
        <div class="hero-content">
            <div class="hero-small">🇧🇩 BANGLADESH AI ASSISTANT</div>
            <div class="hero-title">How can I help you today?</div>
            <div class="hero-description">
                Search Bangladesh institutions, hospitals, restaurants, government 
                information and current events using one intelligent assistant.
            </div>
        </div>
    </div>
    """
)


# ============================================================
# STATISTICS CARDS
# ============================================================

render_html(
    """
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-icon">🔗</div>
            <div class="stat-value">4</div>
            <div class="stat-label">Connected sources</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">📍</div>
            <div class="stat-value">64</div>
            <div class="stat-label">Districts</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🗺️</div>
            <div class="stat-value">8</div>
            <div class="stat-label">Divisions</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">⚡</div>
            <div class="stat-value">Live</div>
            <div class="stat-label">Web grounding</div>
        </div>
    </div>
    """
)


# ============================================================
# EMPTY STATE & SUGGESTIONS
# ============================================================

selected_prompt = None

if not st.session_state.messages:

    render_html(
        """
        <div class="empty-state">
            <div class="empty-icon">🤖</div>
            <div class="empty-title">Start a conversation</div>
            <div class="empty-description">
                Ask anything about Bangladesh or choose one of the examples below.
            </div>
        </div>
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🏥  Hospitals in Dhaka", use_container_width=True):
            selected_prompt = "How many hospitals are in Dhaka?"

    with col2:
        if st.button("🏛️  Universities in Dhaka", use_container_width=True):
            selected_prompt = "Find universities in Dhaka."

    with col3:
        if st.button("🌐  Role of DGHS", use_container_width=True):
            selected_prompt = "What is the role of DGHS?"


# ============================================================
# QUICK PROMPT HANDLER
# ============================================================

if selected_prompt:
    handle_user_query(selected_prompt)
    st.rerun()


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:
    role = message["role"]
    avatar = "🇧🇩" if role == "assistant" else "👤"

    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input("Ask Bangladesh AI anything...")

if user_input:
    handle_user_query(user_input)
    st.rerun()


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">
        🇧🇩 Bangladesh AI &nbsp;·&nbsp; Gemini 3.5 Flash &nbsp;·&nbsp; LangChain
    </div>
    """
)