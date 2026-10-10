import streamlit as st
import pandas as pd
import plotly.express as px

from detector import analyze_message
from database import init_db, save_incident, get_incidents
from ai_analyzer import get_ai_analysis
from voice import generate_tamil_warning
# Initialize database
init_db()

# Page configuration
st.set_page_config(
    page_title="Gram-Shield",
    page_icon="🛡️",
    layout="wide"
)
st.markdown(
    """
    <style>

    /* =========================
       ANIMATED BACKGROUND
       ========================= */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 20%,
                rgba(0, 255, 200, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(120, 80, 255, 0.20),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(0, 140, 255, 0.15),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #07111f,
                #0b1628,
                #10152e
            );

        background-size: 200% 200%;
        animation: backgroundMove 12s ease infinite;
    }

    @keyframes backgroundMove {
        0% {
            background-position: 0% 50%;
        }

        50% {
            background-position: 100% 50%;
        }

        100% {
            background-position: 0% 50%;
        }
    }


    /* =========================
       SIDEBAR
       ========================= */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #081526,
                #11152f
            );

        border-right: 1px solid rgba(0, 255, 200, 0.15);
    }


    /* =========================
       HEADER
       ========================= */

    [data-testid="stHeader"] {
        background: transparent;
    }


    /* =========================
       TITLE GLOW
       ========================= */

    h1 {
        animation: titleGlow 3s ease-in-out infinite alternate;
    }

    @keyframes titleGlow {

        from {
            text-shadow:
                0 0 5px rgba(0, 255, 200, 0.3);
        }

        to {
            text-shadow:
                0 0 10px rgba(0, 255, 200, 0.8),
                0 0 25px rgba(80, 100, 255, 0.5);
        }
    }


    /* =========================
       GLASS CARDS
       ========================= */

    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.05);

        border: 1px solid rgba(255,255,255,0.10);

        border-radius: 18px;

        padding: 18px;

        backdrop-filter: blur(12px);

        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease,
            border-color 0.3s ease;
    }


    [data-testid="stMetric"]:hover {

        transform: translateY(-5px);

        border-color:
            rgba(0,255,200,0.5);

        box-shadow:
            0 0 20px rgba(0,255,200,0.15);
    }


    /* =========================
       BUTTON GLOW
       ========================= */

    .stButton > button {

        border-radius: 12px;

        border: 1px solid
            rgba(0,255,200,0.4);

        background:
            linear-gradient(
                135deg,
                rgba(0,255,200,0.15),
                rgba(100,80,255,0.18)
            );

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease;
    }


    .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 0 18px
            rgba(0,255,200,0.35);
    }


    /* =========================
       PULSING STATUS
       ========================= */

    .status-dot {

        display: inline-block;

        width: 10px;
        height: 10px;

        background: #00ffb3;

        border-radius: 50%;

        margin-right: 8px;

        box-shadow:
            0 0 5px #00ffb3,
            0 0 15px #00ffb3;

        animation:
            pulse 1.5s infinite;
    }


    @keyframes pulse {

        0% {
            transform: scale(1);
            opacity: 1;
        }

        50% {
            transform: scale(1.5);
            opacity: 0.5;
        }

        100% {
            transform: scale(1);
            opacity: 1;
        }
    }


    /* =========================
       GLASS CONTAINERS
       ========================= */

    .glass-card {

        background:
            rgba(255,255,255,0.04);

        border:
            1px solid rgba(255,255,255,0.08);

        border-radius: 18px;

        padding: 20px;

        backdrop-filter: blur(12px);

        box-shadow:
            0 8px 30px
            rgba(0,0,0,0.25);

        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease;
    }


    .glass-card:hover {

        transform:
            translateY(-4px);

        box-shadow:
            0 0 25px
            rgba(80,120,255,0.18);
    }


    /* =========================
       EMERGENCY PULSE
       ========================= */

    .emergency {

        animation:
            emergencyPulse 2s infinite;

        border-radius: 14px;
    }


    @keyframes emergencyPulse {

        0% {
            box-shadow:
                0 0 0
                rgba(255,50,50,0);
        }

        50% {
            box-shadow:
                0 0 20px
                rgba(255,50,50,0.35);
        }

        100% {
            box-shadow:
                0 0 0
                rgba(255,50,50,0);
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)
# Title
st.markdown(
    """
    <div style="
        padding: 20px;
        border-radius: 15px;
        background: linear-gradient(135deg, #0f172a, #1e3a5f);
        margin-bottom: 25px;
    ">
        <h1 style="color: white; margin-bottom: 5px;">
            🛡️ Gram-Shield
        </h1>
        <p style="color: #cbd5e1; font-size: 18px; margin: 0;">
            Vernacular Scam Alert & Panchayat Threat Intelligence
        </p>
        <p style="color: #94a3b8; margin-top: 10px;">
            Protecting rural communities from digital fraud and social engineering.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style="
        margin-bottom:20px;
        font-size:14px;
        color:#00ffb3;
        font-weight:600;
    ">
        <span class="status-dot"></span>
        SYSTEM ACTIVE • REAL-TIME THREAT MONITORING
    </div>
    """,
    unsafe_allow_html=True
)
# Sidebar
st.sidebar.markdown(
    """
    <h2 style="text-align:center;">
        🏛️ Gram-Shield
    </h2>
    <p style="text-align:center;">
        Panchayat Cyber Safety
    </p>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Select Module",
    [
        "🚨 Scam Detector",
        "📊 Threat Dashboard"
    ]
)

# =========================================================
# SCAM DETECTOR
# =========================================================

if page == "🚨 Scam Detector":
    message = st.text_area(
        "📩 Message to analyze",
        height=180,
        placeholder="Paste a suspicious SMS, WhatsApp message or link here..."
    )
    
    village = st.selectbox(
    "📍 Select Panchayat / Village",
    [
        "Manivakkam",
        "Nandambakkam",
        "Maraimalai Nagar",
        "Other"
    ]
)

    if st.button("🔍 Analyze Message", use_container_width=True):

        if not message.strip():

            st.warning("Please enter a message first.")

        else:

            result = analyze_message(message)

            # Save incident
            save_incident(
            village,
            message,
            result["scam_type"],
            result["risk"],
            result["score"]
            )

            st.subheader("Analysis Result")

            # Risk display
            if result["risk"] == "HIGH":
                st.error(f"🔴 HIGH RISK — Score: {result['score']}")

            elif result["risk"] == "MEDIUM":
                st.warning(f"🟠 MEDIUM RISK — Score: {result['score']}")

            else:
                st.success(f"🟢 LOW RISK — Score: {result['score']}")

            st.write("**Scam Type:**", result["scam_type"])

            st.write("### ⚠️ Why was this flagged?")

            if result["reasons"]:

                for reason in result["reasons"]:
                    st.write("•", reason)

            else:

                st.write("No major suspicious indicators detected.")

            st.divider()

            st.subheader("🤖 AI Analysis")

            with st.spinner("AI is analyzing the message..."):
             ai_result = get_ai_analysis(message)

            st.write(ai_result) 
            st.divider()

st.subheader("🔊 Tamil Safety Warning")

if st.button("🔊 Play Tamil Warning"):

    audio_file = generate_tamil_warning()

    with open(audio_file, "rb") as f:
        audio_bytes = f.read()

    st.audio(audio_bytes, format="audio/mp3") 


# =========================================================
# PANCHAYAT DASHBOARD
# =========================================================

else:

    st.header("🏛️ Panchayat Cyber Threat Dashboard")
    st.caption("Real-time overview of reported cyber threats")

    incidents = get_incidents()

    if not incidents:

        st.info("No scam incidents recorded yet.")

    else:

        df = pd.DataFrame(
            incidents,
            columns=[
    "ID",
    "Timestamp",
    "Village",
    "Message",
    "Scam Type",
    "Risk",
    "Score"
]
        )

        # =========================
        # METRICS
        # =========================

        total = len(df)
        high = len(df[df["Risk"] == "HIGH"])
        medium = len(df[df["Risk"] == "MEDIUM"])
        low = len(df[df["Risk"] == "LOW"])

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("📋 Total Reports", total)
        col2.metric("🔴 High Risk", high)
        col3.metric("🟠 Medium Risk", medium)
        col4.metric("🟢 Low Risk", low)

        if high > 0:
            st.error(
             f"🚨 EMERGENCY ALERT: {high} high-risk scam incident(s) detected!"
            )
        else:
            st.success("🟢 No high-risk incidents currently detected.")

        st.divider() 

        #===============
        #Village Threat Summary
        #===============

        st.subheader("📍 Village-wise Threat Summary")

        village_counts=(
            df["Village"]
            .value_counts()
            .reset_index()
        )

        village_counts.columns=["Village","Reports"]

        st.dataframe(
            village_counts,
            use_container_width=True,
            hide_index=True
        )

        st.divider()


        # =========================
        # CHART
        # =========================

        st.subheader("📊 Scam Distribution")

        scam_counts = (
            df["Scam Type"]
            .value_counts()
            .reset_index()
        )

        scam_counts.columns = ["Scam Type", "Count"]

        fig = px.bar(
            scam_counts,
            x="Scam Type",
            y="Count",
            title="Reported Scam Categories"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        # =========================
        # FILTER
        # =========================

        st.subheader("🔎 Filter Incidents")

        risk_filter = st.selectbox(
            "Select Risk Level",
            ["ALL", "HIGH", "MEDIUM", "LOW"]
        )

        if risk_filter != "ALL":
            filtered_df = df[df["Risk"] == risk_filter]
        else:
            filtered_df = df

        # =========================
        # INCIDENT TABLE
        # =========================

        st.subheader("🚨 Recent Incidents")

        display_df = filtered_df[
            [
                "Timestamp",
                "Village",
                "Scam Type",
                "Risk",
                "Score",
                "Message"
            ]
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )