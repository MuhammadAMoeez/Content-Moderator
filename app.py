import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import requests

# 1. Page Configuration
st.set_page_config(page_title="🛡️ AI Moderator Console", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ AI Content Moderator Dashboard")

# --- 2. LIVE CONNECTION ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1n0L-3LG6bQHJw8E8iqMqpUtqzNgfvK4kBHtNGErO3lU/edit?usp=sharing"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=SHEET_URL, ttl=0)
    
    # Data Cleaning
    df.columns = df.columns.str.strip()
    col_map = {c.lower(): c for c in df.columns}
    
    score_col = col_map.get('toxicity score')
    cat_col = col_map.get('category')
    status_col = col_map.get('status') or col_map.get('action')

    # --- 3. TOP LEVEL METRICS ---
    total = len(df)
    flagged = len(df[df[status_col].astype(str).str.contains('Reject', case=False, na=False)]) if status_col else 0
    safety_score = ((total - flagged) / total * 100) if total > 0 else 0

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Scanned", total)
    m2.metric("Flagged Items", flagged, delta_color="inverse")
    m3.metric("Safety Score", f"{safety_score:.1f}%")

    st.divider()

    # --- 4. TABS INTERFACE ---
    tab1, tab2 = st.tabs(["📊 Analytics Overview", "📝 Detailed Logs"])

    with tab1:
        st.subheader("Moderation Insights")
        c1, c2 = st.columns(2)
        
        with c1:
            st.write("### Violation Breakdown")
            if cat_col:
                # Bar Chart for Categorical Data
                cat_counts = df[cat_col].value_counts()
                st.bar_chart(cat_counts, color="#ff4b4b")
        
        with c2:
            st.write("### Toxicity Trend (Last 20)")
            if score_col:
                # Line Chart for Numerical Trends
                # We ensure the score is numeric to avoid errors
                trend_data = pd.to_numeric(df[score_col], errors='coerce').tail(20)
                st.line_chart(trend_data, color="#29b5e8")

    with tab2:
        st.subheader("Real-time Activity Log")
        
        def highlight_risk(val):
            return 'background-color: #441111; color: white' if isinstance(val, (int, float)) and val > 0.7 else ''

        if score_col:
            styled_df = df.style.map(highlight_risk, subset=[score_col])
            st.dataframe(styled_df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

    # --- 5. SIDEBAR TESTER ---
    with st.sidebar:
        st.header("🧪 Test AI System")
        test_text = st.text_area("Paste content to moderate:")
        if st.button("Analyze Now"):
            WEBHOOK_URL = "https://n8n.triakislabs.com/webhook/moderate-content"
            requests.post(WEBHOOK_URL, json={"text": test_text})
            st.success("Sent! Refreshing data...")
            st.rerun()

except Exception as e:
    st.error(f"⚠️ Connection Error: {e}")