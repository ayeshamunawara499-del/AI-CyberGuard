import streamlit as st
import re
import os
from dotenv import load_dotenv
from google import genai


# =========================================================
# GEMINI AI SETUP
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None


def get_ai_analysis(content, content_type, risk_score, indicators):
    """
    Send the detected content and cybersecurity indicators
    to Gemini AI for additional security analysis.
    """

    if client is None:
        return "⚠️ Gemini API key not found. Please check your .env file."

    indicator_text = ", ".join(indicators) if indicators else "No suspicious indicators detected"

    prompt = f"""
You are an AI cybersecurity assistant called AI CyberGuard.

Your job is to analyze a {content_type} for possible phishing,
scam, social engineering, or other cybersecurity risks.

Do NOT claim that something is 100% safe or 100% malicious.
Give a careful assessment based on the available indicators.

Content:
{content}

Rule-based Risk Score:
{risk_score}/100

Detected Security Indicators:
{indicator_text}

Provide your response in this format:

Security Assessment:
- Give a simple assessment such as Likely Safe, Suspicious, or High Risk.

Why:
- Explain the important security indicators in simple language.

What You Should Do:
- Give practical safety advice.
- Tell the user whether they should click, reply, or share sensitive information.

Important:
- Never ask the user to click the link.
- Never request passwords, OTPs, PINs, CVV, or other sensitive information.
- Keep the explanation clear and beginner-friendly.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"⚠️ Gemini AI could not analyze this input.\n\nError: {str(e)}"


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI CyberGuard",
    page_icon="🔐",
    layout="centered"
)
# =========================================================
# COLORFUL CYBERSECURITY UI
# =========================================================

st.markdown("""
<style>

    /* Main Background */
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(79, 70, 229, 0.18), transparent 30%),
            radial-gradient(circle at 90% 20%, rgba(6, 182, 212, 0.15), transparent 30%),
            radial-gradient(circle at 50% 90%, rgba(168, 85, 247, 0.15), transparent 35%),
            linear-gradient(135deg, #050816 0%, #0b1026 45%, #111936 100%);
        color: white;
    }

    /* Main Content */
    .main .block-container {
        max-width: 950px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Headings */
    h1 {
        color: #ffffff !important;
        text-align: center;
        font-size: 3.2rem !important;
        font-weight: 800 !important;
        text-shadow:
            0 0 10px rgba(99, 102, 241, 0.8),
            0 0 25px rgba(6, 182, 212, 0.5);
        animation: titleGlow 3s ease-in-out infinite alternate;
    }

    h2, h3 {
        color: #e0e7ff !important;
    }

    /* Subtitle */
    .stApp h2 {
        text-align: center;
    }

    /* Normal Text */
    p, label, .stMarkdown {
        color: #dbeafe !important;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            #6366f1,
            #06b6d4,
            #a855f7,
            transparent
        );
        margin: 25px 0;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border: 1px solid rgba(129, 140, 248, 0.6);
        border-radius: 14px;
        padding: 0.8rem 1rem;
        background: linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed,
            #0891b2
        );
        color: white !important;
        font-size: 1rem;
        font-weight: 700;
        box-shadow:
            0 8px 25px rgba(79, 70, 229, 0.35),
            inset 0 0 15px rgba(255, 255, 255, 0.08);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow:
            0 12px 35px rgba(6, 182, 212, 0.45),
            0 0 20px rgba(124, 58, 237, 0.45);
        border-color: #67e8f9;
    }

    /* Text Input */
    .stTextInput input,
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.85) !important;
        color: white !important;
        border: 1px solid rgba(99, 102, 241, 0.55) !important;
        border-radius: 12px !important;
        padding: 12px !important;
        transition: all 0.3s ease;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #22d3ee !important;
        box-shadow:
            0 0 0 2px rgba(34, 211, 238, 0.15),
            0 0 20px rgba(34, 211, 238, 0.25) !important;
    }

    /* Risk Score Card */
    [data-testid="stMetric"] {
        background: linear-gradient(
            135deg,
            rgba(30, 41, 59, 0.95),
            rgba(49, 46, 129, 0.65)
        );
        border: 1px solid rgba(129, 140, 248, 0.45);
        border-radius: 18px;
        padding: 20px;
        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.35),
            0 0 20px rgba(99, 102, 241, 0.15);
        animation: cardFloat 4s ease-in-out infinite;
    }

    [data-testid="stMetricLabel"] {
        color: #c7d2fe !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    /* Success / Warning / Error Cards */
    [data-testid="stAlert"] {
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.20);
        animation: alertSlide 0.5s ease-out;
    }

    /* Code / URL Box */
    code {
        color: #67e8f9 !important;
    }

    [data-testid="stCodeBlock"] {
        border: 1px solid rgba(34, 211, 238, 0.3);
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(34, 211, 238, 0.08);
    }

    /* AI Analysis Area */
    [data-testid="stMarkdownContainer"] {
        line-height: 1.65;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #22d3ee !important;
    }

    /* Animations */

    @keyframes titleGlow {
        from {
            text-shadow:
                0 0 8px rgba(99, 102, 241, 0.6),
                0 0 18px rgba(6, 182, 212, 0.3);
        }

        to {
            text-shadow:
                0 0 15px rgba(99, 102, 241, 0.9),
                0 0 35px rgba(6, 182, 212, 0.7),
                0 0 50px rgba(168, 85, 247, 0.4);
        }
    }

    @keyframes cardFloat {
        0%, 100% {
            transform: translateY(0px);
        }

        50% {
            transform: translateY(-3px);
        }
    }

    @keyframes alertSlide {
        from {
            opacity: 0;
            transform: translateY(8px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    /* Feature Cards */

.feature-card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 18px;
    padding: 22px 16px;
    text-align: center;
    min-height: 190px;
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    transition: all 0.35s ease;
}

.feature-card:hover {
    transform: translateY(-8px);
    border-color: #22d3ee;
    box-shadow:
        0 15px 35px rgba(6, 182, 212, 0.25),
        0 0 25px rgba(99, 102, 241, 0.2);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 8px;
    animation: iconFloat 3s ease-in-out infinite;
}

.feature-card h4 {
    color: #ffffff !important;
    font-size: 1.15rem;
    margin-bottom: 8px;
}

.feature-card p {
    color: #cbd5e1 !important;
    font-size: 0.9rem;
    line-height: 1.5;
}

@keyframes iconFloat {
    0%, 100% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-5px);
    }
}
/* Premium Action Buttons */

.stButton > button {
    position: relative;
    overflow: hidden;
    min-height: 58px;
    border-radius: 16px !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.3px;
    transition: all 0.3s ease !important;
}

.stButton > button::before {
    content: "";
    position: absolute;
    top: 0;
    left: -120%;
    width: 70%;
    height: 100%;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255, 255, 255, 0.25),
        transparent
    );
    transform: skewX(-20deg);
    transition: left 0.6s ease;
}

.stButton > button:hover::before {
    left: 150%;
}

.stButton > button:hover {
    transform: translateY(-4px) !important;
    box-shadow:
        0 12px 35px rgba(34, 211, 238, 0.35),
        0 0 25px rgba(99, 102, 241, 0.25) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}
/* =========================================================
   RISK SCORE PREMIUM EFFECT
   ========================================================= */

[data-testid="stMetric"] {
    position: relative;
    overflow: hidden;
    text-align: center;
    min-height: 150px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border-radius: 22px !important;
    background:
        linear-gradient(
            135deg,
            rgba(30, 41, 59, 0.95),
            rgba(49, 46, 129, 0.75)
        ) !important;
    border: 1px solid rgba(103, 232, 249, 0.45) !important;
    box-shadow:
        0 10px 35px rgba(0, 0, 0, 0.35),
        0 0 30px rgba(99, 102, 241, 0.20) !important;
    animation: riskCardPulse 3s ease-in-out infinite;
}

[data-testid="stMetric"]::before {
    content: "";
    position: absolute;
    top: -80px;
    left: -80px;
    width: 160px;
    height: 160px;
    background: rgba(34, 211, 238, 0.12);
    border-radius: 50%;
    filter: blur(20px);
    animation: riskGlow 4s ease-in-out infinite;
}

[data-testid="stMetricLabel"] {
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #a5b4fc !important;
}

[data-testid="stMetricValue"] {
    font-size: 3rem !important;
    font-weight: 900 !important;
    color: #ffffff !important;
    text-shadow:
        0 0 10px rgba(34, 211, 238, 0.7),
        0 0 25px rgba(99, 102, 241, 0.5);
    animation: scoreGlow 2.5s ease-in-out infinite alternate;
}

/* Risk Card Animation */

@keyframes riskCardPulse {
    0%, 100% {
        transform: translateY(0px);
        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.35),
            0 0 25px rgba(99, 102, 241, 0.15);
    }

    50% {
        transform: translateY(-4px);
        box-shadow:
            0 15px 40px rgba(0, 0, 0, 0.40),
            0 0 35px rgba(34, 211, 238, 0.25);
    }
}

@keyframes riskGlow {
    0%, 100% {
        transform: scale(1);
        opacity: 0.6;
    }

    50% {
        transform: scale(1.35);
        opacity: 1;
    }
}

@keyframes scoreGlow {
    from {
        text-shadow:
            0 0 8px rgba(34, 211, 238, 0.5);
    }

    to {
        text-shadow:
            0 0 15px rgba(34, 211, 238, 0.9),
            0 0 30px rgba(99, 102, 241, 0.7);
    }
}
/* =========================================================
   RISK LEVEL NEON CARDS
   ========================================================= */

.risk-card {
    padding: 22px;
    margin: 15px 0;
    border-radius: 20px;
    text-align: center;
    backdrop-filter: blur(12px);
    animation: riskAppear 0.6s ease-out;
}

.risk-card h2 {
    margin: 0;
    font-size: 1.8rem;
    font-weight: 800;
}

.risk-card p {
    margin: 8px 0 0;
    font-size: 1rem;
}

/* LOW RISK */

.low-risk {
    background: linear-gradient(
        135deg,
        rgba(16, 185, 129, 0.18),
        rgba(6, 78, 59, 0.45)
    );
    border: 1px solid rgba(52, 211, 153, 0.7);
    box-shadow:
        0 0 20px rgba(16, 185, 129, 0.25),
        inset 0 0 25px rgba(16, 185, 129, 0.08);
}

.low-risk h2 {
    color: #34d399 !important;
    text-shadow: 0 0 15px rgba(52, 211, 153, 0.7);
}

/* MEDIUM RISK */

.medium-risk {
    background: linear-gradient(
        135deg,
        rgba(245, 158, 11, 0.18),
        rgba(120, 53, 15, 0.45)
    );
    border: 1px solid rgba(251, 191, 36, 0.7);
    box-shadow:
        0 0 20px rgba(245, 158, 11, 0.25),
        inset 0 0 25px rgba(245, 158, 11, 0.08);
}

.medium-risk h2 {
    color: #fbbf24 !important;
    text-shadow: 0 0 15px rgba(251, 191, 36, 0.7);
}

/* HIGH RISK */

.high-risk {
    background: linear-gradient(
        135deg,
        rgba(239, 68, 68, 0.20),
        rgba(127, 29, 29, 0.50)
    );
    border: 1px solid rgba(248, 113, 113, 0.8);
    box-shadow:
        0 0 25px rgba(239, 68, 68, 0.35),
        inset 0 0 30px rgba(239, 68, 68, 0.10);
    animation: highRiskPulse 2s ease-in-out infinite;
}

.high-risk h2 {
    color: #f87171 !important;
    text-shadow:
        0 0 12px rgba(248, 113, 113, 0.8),
        0 0 25px rgba(239, 68, 68, 0.5);
}

/* Animations */

@keyframes riskAppear {
    from {
        opacity: 0;
        transform: translateY(12px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes highRiskPulse {
    0%, 100% {
        box-shadow:
            0 0 20px rgba(239, 68, 68, 0.25),
            inset 0 0 25px rgba(239, 68, 68, 0.08);
    }

    50% {
        box-shadow:
            0 0 40px rgba(239, 68, 68, 0.50),
            inset 0 0 35px rgba(239, 68, 68, 0.15);
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HOME PAGE
# =========================================================

st.title("🔐 AI CyberGuard")
st.subheader("Before You Click")

st.write(
    "Check suspicious links and messages before you click."
)

st.divider()

st.header("What do you want to check?")
# =========================================================
# FEATURE CARDS
# =========================================================

feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🛡️</div>
        <h4>Smart Detection</h4>
        <p>Detect suspicious security indicators in links and messages.</p>
    </div>
    """, unsafe_allow_html=True)

with feature_col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <h4>AI Analysis</h4>
        <p>Get intelligent security explanations powered by Gemini AI.</p>
    </div>
    """, unsafe_allow_html=True)

with feature_col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h4>Risk Scoring</h4>
        <p>Understand security risk with Low, Medium and High levels.</p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# MAIN OPTIONS
# =========================================================

col1, col2 = st.columns(2)

with col1:
    if st.button("🔗 Check Link", use_container_width=True):
        st.session_state["check_link"] = True
        st.session_state["check_message"] = False

with col2:
    if st.button("📩 Check Message", use_container_width=True):
        st.session_state["check_message"] = True
        st.session_state["check_link"] = False


# =========================================================
# DEFAULT STATE
# =========================================================

if "check_link" not in st.session_state:
    st.session_state["check_link"] = False

if "check_message" not in st.session_state:
    st.session_state["check_message"] = False


# =========================================================
# URL CHECKER
# =========================================================

if st.session_state["check_link"]:

    st.divider()

    st.subheader("🔗 URL Checker")

    url = st.text_input(
        "Paste the URL here",
        placeholder="https://example.com"
    )

    if st.button("🔍 Analyze Link", use_container_width=True):

        if url.strip():

            risk_score = 0
            indicators = []

            st.success("✅ URL received successfully.")

            st.write("**URL:**")
            st.code(url)

            # -------------------------------------------------
            # HTTPS CHECK
            # -------------------------------------------------

            if url.lower().startswith("https://"):

                st.success(
                    "🔒 HTTPS: Secure connection detected."
                )

            else:

                st.warning(
                    "⚠️ HTTPS: This URL is not using HTTPS."
                )

                risk_score += 20
                indicators.append("URL is not using HTTPS")


            # -------------------------------------------------
            # IP ADDRESS CHECK
            # -------------------------------------------------

            ip_pattern = r"https?://(?:\d{1,3}\.){3}\d{1,3}"

            if re.search(ip_pattern, url):

                st.warning(
                    "⚠️ IP Address: URL uses an IP address."
                )

                risk_score += 20
                indicators.append("URL uses an IP address")

            else:

                st.success(
                    "✅ IP Address: No IP address detected."
                )


            # -------------------------------------------------
            # URL LENGTH CHECK
            # -------------------------------------------------

            if len(url) > 100:

                st.warning(
                    "⚠️ URL Length: This URL is unusually long."
                )

                risk_score += 10
                indicators.append("URL is unusually long")

            else:

                st.success(
                    "✅ URL Length: URL length looks normal."
                )


            # -------------------------------------------------
            # SUSPICIOUS CHARACTER CHECK
            # -------------------------------------------------

            suspicious_chars = ["@", "%"]

            found_chars = [
                char for char in suspicious_chars
                if char in url
            ]

            if found_chars:

                st.warning(
                    f"⚠️ Suspicious Characters: Found "
                    f"{', '.join(found_chars)} in the URL."
                )

                risk_score += 10

                indicators.append(
                    "Suspicious characters: "
                    + ", ".join(found_chars)
                )

            else:

                st.success(
                    "✅ Suspicious Characters: "
                    "No suspicious characters detected."
                )


            # -------------------------------------------------
            # SUSPICIOUS KEYWORD CHECK
            # -------------------------------------------------

            suspicious_keywords = [
                "login",
                "verify",
                "account",
                "update",
                "secure",
                "bank",
                "password",
                "confirm"
            ]

            found_keywords = [
                word
                for word in suspicious_keywords
                if word in url.lower()
            ]

            if found_keywords:

                st.warning(
                    f"⚠️ Suspicious Keywords: "
                    f"Found {', '.join(found_keywords)}."
                )

                risk_score += 10

                indicators.append(
                    "Suspicious keywords: "
                    + ", ".join(found_keywords)
                )

            else:

                st.success(
                    "✅ Suspicious Keywords: "
                    "No suspicious keywords detected."
                )


            # -------------------------------------------------
            # SUSPICIOUS DOMAIN PATTERN CHECK
            # -------------------------------------------------

            if "://" in url:

                domain_part = (
                    url.split("://", 1)[1]
                    .split("/", 1)[0]
                )

            else:

                domain_part = url.split("/", 1)[0]

            hyphen_count = domain_part.count("-")

            if hyphen_count >= 2:

                st.warning(
                    "⚠️ Domain Pattern: "
                    "This domain contains multiple hyphens."
                )

                risk_score += 10

                indicators.append(
                    "Domain contains multiple hyphens"
                )

            else:

                st.success(
                    "✅ Domain Pattern: "
                    "No suspicious domain pattern detected."
                )


            # -------------------------------------------------
            # UNUSUAL URL STRUCTURE CHECK
            # -------------------------------------------------

            if "://" not in url:

                st.warning(
                    "⚠️ URL Structure: URL is missing a "
                    "protocol such as http:// or https://."
                )

                risk_score += 10

                indicators.append(
                    "URL is missing HTTP/HTTPS protocol"
                )

            else:

                parts = url.split("://", 1)

                if len(parts) == 2 and parts[1].strip():

                    domain_part = (
                        parts[1]
                        .split("/", 1)[0]
                    )

                    if "." in domain_part:

                        st.success(
                            "✅ URL Structure: "
                            "URL structure looks normal."
                        )

                    else:

                        st.warning(
                            "⚠️ URL Structure: "
                            "Domain structure looks unusual."
                        )

                        risk_score += 10

                        indicators.append(
                            "Unusual domain structure"
                        )

                else:

                    st.warning(
                        "⚠️ URL Structure: "
                        "URL structure is invalid."
                    )

                    risk_score += 10

                    indicators.append(
                        "Invalid URL structure"
                    )


            # -------------------------------------------------
            # FINAL URL RISK RESULT
            # -------------------------------------------------

            st.divider()

            st.subheader("📊 Security Risk Result")

            st.metric(
                "Risk Score",
                f"{risk_score}/100"
            )


            if risk_score <= 20:

                st.markdown("""
                <div class="risk-card low-risk">
                    <h2>🟢 LOW RISK</h2>
                    <p>This URL shows only a few or no suspicious indicators.</p>
                </div>
                """, unsafe_allow_html=True)

            elif risk_score <= 50:

                st.markdown("""
                <div class="risk-card medium-risk">
                    <h2>🟡 MEDIUM RISK</h2>
                    <p>This URL contains some suspicious indicators. Be careful before opening it.</p>
                </div>
                """, unsafe_allow_html=True)

            else:

                st.markdown("""
                <div class="risk-card high-risk">
                    <h2>🔴 HIGH RISK</h2>
                    <p>This URL contains multiple suspicious indicators. Do not click unless you can verify it is safe.</p>
                </div>
                """, unsafe_allow_html=True)


            # =================================================
            # GEMINI AI ANALYSIS
            # =================================================

            st.divider()

            st.subheader("🤖 AI Security Analysis")

            with st.spinner(
                "🤖 Gemini AI is analyzing the URL..."
            ):

                ai_result = get_ai_analysis(
                    content=url,
                    content_type="URL",
                    risk_score=risk_score,
                    indicators=indicators
                )

            st.write(ai_result)


        else:

            st.warning(
                "⚠️ Please enter a URL."
            )


# =========================================================
# MESSAGE CHECKER
# =========================================================

if st.session_state["check_message"]:

    st.divider()

    st.subheader("📩 Message Checker")

    message = st.text_area(
        "Paste or type your message here",
        placeholder="Paste the suspicious message here...",
        height=150
    )

    if st.button(
        "🔍 Analyze Message",
        use_container_width=True
    ):

        if message.strip():

            risk_score = 0
            indicators = []

            st.success(
                "✅ Message received successfully."
            )

            st.write("**Message:**")

            st.write(message)


            # -------------------------------------------------
            # URGENT LANGUAGE
            # -------------------------------------------------

            urgent_words = [
                "urgent",
                "immediately",
                "now",
                "today",
                "hurry",
                "act fast"
            ]

            found_urgent = [
                word
                for word in urgent_words
                if word in message.lower()
            ]

            if found_urgent:

                st.warning(
                    f"⚠️ Urgent Language: "
                    f"Found {', '.join(found_urgent)}."
                )

                risk_score += 10

                indicators.append(
                    "Urgent language: "
                    + ", ".join(found_urgent)
                )

            else:

                st.success(
                    "✅ Urgent Language: "
                    "No urgent language detected."
                )


            # -------------------------------------------------
            # THREATENING LANGUAGE
            # -------------------------------------------------

            threatening_words = [
                "blocked",
                "suspended",
                "legal action",
                "police",
                "arrest",
                "penalty",
                "terminate"
            ]

            found_threats = [
                word
                for word in threatening_words
                if word in message.lower()
            ]

            if found_threats:

                st.warning(
                    f"⚠️ Threatening Language: "
                    f"Found {', '.join(found_threats)}."
                )

                risk_score += 15

                indicators.append(
                    "Threatening language: "
                    + ", ".join(found_threats)
                )

            else:

                st.success(
                    "✅ Threatening Language: "
                    "No threatening language detected."
                )


            # -------------------------------------------------
            # PRIZE / OFFER CLAIMS
            # -------------------------------------------------

            prize_words = [
                "prize",
                "winner",
                "won",
                "reward",
                "offer",
                "free",
                "cashback",
                "lottery",
                "gift"
            ]

            found_prizes = [
                word
                for word in prize_words
                if word in message.lower()
            ]

            if found_prizes:

                st.warning(
                    f"⚠️ Prize/Offer Claim: "
                    f"Found {', '.join(found_prizes)}."
                )

                risk_score += 10

                indicators.append(
                    "Prize/offer claim: "
                    + ", ".join(found_prizes)
                )

            else:

                st.success(
                    "✅ Prize/Offer Claim: "
                    "No prize or offer claim detected."
                )


            # -------------------------------------------------
            # BANK / PAYMENT REQUEST
            # -------------------------------------------------

            payment_words = [
                "bank",
                "payment",
                "pay",
                "upi",
                "credit card",
                "debit card",
                "account number",
                "transaction"
            ]

            found_payment = [
                word
                for word in payment_words
                if word in message.lower()
            ]

            if found_payment:

                st.warning(
                    f"⚠️ Bank/Payment Request: "
                    f"Found {', '.join(found_payment)}."
                )

                risk_score += 15

                indicators.append(
                    "Bank/payment request: "
                    + ", ".join(found_payment)
                )

            else:

                st.success(
                    "✅ Bank/Payment Request: "
                    "No bank or payment request detected."
                )


            # -------------------------------------------------
            # PASSWORD / OTP REQUEST
            # -------------------------------------------------

            credential_words = [
                "password",
                "otp",
                "one time password",
                "pin",
                "cvv",
                "verification code",
                "login details",
                "passcode"
            ]

            found_credentials = [
                word
                for word in credential_words
                if word in message.lower()
            ]

            if found_credentials:

                st.warning(
                    f"⚠️ Password/OTP Request: "
                    f"Found {', '.join(found_credentials)}."
                )

                risk_score += 20

                indicators.append(
                    "Password/OTP request: "
                    + ", ".join(found_credentials)
                )

            else:

                st.success(
                    "✅ Password/OTP Request: "
                    "No password or OTP request detected."
                )


            # -------------------------------------------------
            # SUSPICIOUS LINK
            # -------------------------------------------------

            url_pattern = r"https?://\S+|www\.\S+"

            found_links = re.findall(
                url_pattern,
                message.lower()
            )

            if found_links:

                st.warning(
                    f"⚠️ Suspicious Link: "
                    f"Found {len(found_links)} link(s) "
                    f"in the message."
                )

                st.write("🔗 Link(s) detected:")

                for link in found_links:

                    st.code(link)

                risk_score += 20

                indicators.append(
                    f"Message contains {len(found_links)} link(s)"
                )

            else:

                st.success(
                    "✅ Suspicious Link: "
                    "No links detected in the message."
                )


            # -------------------------------------------------
            # FINAL MESSAGE RISK RESULT
            # -------------------------------------------------

            st.divider()

            st.subheader(
                "📊 Security Risk Result"
            )

            st.metric(
                "Risk Score",
                f"{risk_score}/100"
            )


            if risk_score <= 20:

                st.markdown("""
                <div class="risk-card low-risk">
                    <h2>🟢 LOW RISK</h2>
                    <p>This message shows only a few or no suspicious indicators.</p>
                </div>
                """, unsafe_allow_html=True)

            elif risk_score <= 50:

                st.markdown("""
                <div class="risk-card medium-risk">
                    <h2>🟡 MEDIUM RISK</h2>
                    <p>This message contains some suspicious indicators. Be careful before responding or clicking any link.</p>
                </div>
                """, unsafe_allow_html=True)

            else:

                st.markdown("""
                <div class="risk-card high-risk">
                    <h2>🔴 HIGH RISK</h2>
                    <p>This message contains multiple suspicious indicators. Do not click links or share sensitive information.</p>
                </div>
                """, unsafe_allow_html=True)


            # =================================================
            # GEMINI AI ANALYSIS
            # =================================================

            st.divider()

            st.subheader(
                "🤖 AI Security Analysis"
            )

            with st.spinner(
                "🤖 Gemini AI is analyzing the message..."
            ):

                ai_result = get_ai_analysis(
                    content=message,
                    content_type="message",
                    risk_score=risk_score,
                    indicators=indicators
                )

            st.write(ai_result)


        else:

            st.warning(
                "⚠️ Please enter a message."
            )


# =========================================================
# SAFETY REMINDER
# =========================================================

st.divider()

st.info(
    "🛡️ Stay safe. Think before you click."
)