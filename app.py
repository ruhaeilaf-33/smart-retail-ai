import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# ================= CONFIG =================
st.set_page_config(
    page_title="Retail Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CSS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

/* ── BASE ── */
html, body, [class*="css"], .stApp {
    background-color: #f1f5f9 !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #1e293b !important;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] small {
    color: #334155 !important;
}
section[data-testid="stSidebar"] .stFileUploader label p,
section[data-testid="stSidebar"] .stSelectbox label p {
    font-family: 'Syne', sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #3b82f6 !important;
}

/* ── FILE UPLOADER — FORCE LIGHT ── */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background-color: #eff6ff !important;
    border: 2px dashed #93c5fd !important;
    border-radius: 12px !important;
}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] * {
    color: #1e40af !important;
    background-color: transparent !important;
}
/* The actual inner drop zone */
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    background-color: #eff6ff !important;
    border: none !important;
}
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] * {
    color: #3b82f6 !important;
}
/* Browse button inside uploader */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] button,
section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
    background-color: #3b82f6 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
/* File name chip after upload */
section[data-testid="stSidebar"] [data-testid="stFileUploaderFile"] {
    background-color: #dbeafe !important;
    border: 1px solid #93c5fd !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] [data-testid="stFileUploaderFile"] * {
    color: #1e40af !important;
}

/* ── SELECTBOX ── */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    color: #1e293b !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #1e293b !important;
}
[data-baseweb="popover"] li {
    background: #ffffff !important;
    color: #1e293b !important;
}
[data-baseweb="popover"] li:hover {
    background: #eff6ff !important;
    color: #1d4ed8 !important;
}

/* ── MAIN AREA ── */
.main .block-container {
    background-color: #f1f5f9 !important;
    padding-top: 1rem !important;
    max-width: 1400px !important;
}

/* ── HEADER ── */
.dash-header {
    padding: 32px 0 24px;
    text-align: center;
}
.dash-badge {
    display: inline-block;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    color: #2563eb;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 100px;
    margin-bottom: 12px;
}
.dash-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(24px, 3.5vw, 44px);
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 50%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 8px;
    line-height: 1.15;
}
.dash-sub {
    font-size: 14px;
    color: #64748b;
    letter-spacing: 0.02em;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff !important;
    border-radius: 14px !important;
    padding: 5px !important;
    gap: 4px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}
.stTabs [role="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #64748b !important;
    background: transparent !important;
    border-radius: 10px !important;
    padding: 9px 20px !important;
    border: none !important;
    transition: all 0.2s ease !important;
}
.stTabs [role="tab"]:hover {
    color: #3b82f6 !important;
    background: #f0f9ff !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #1d4ed8, #6d28d9) !important;
    color: #ffffff !important;
}

/* ── KPI CARDS ── */
.kpi-wrap {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px 20px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    height: 100%;
}
.kpi-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #7c3aed);
    border-radius: 16px 16px 0 0;
}
.kpi-wrap:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(59,130,246,0.12);
}
.kpi-icon { font-size: 22px; margin-bottom: 8px; display: block; }
.kpi-label {
    font-size: 11px; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: #94a3b8; margin-bottom: 6px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 28px; font-weight: 700;
    color: #0f172a; line-height: 1;
}
.kpi-delta { font-size: 12px; color: #22c55e; margin-top: 6px; font-weight: 500; }

/* ── SECTION CARDS ── */
.section-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px;
    margin-top: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 15px; font-weight: 700;
    color: #0f172a; letter-spacing: -0.01em;
    margin-bottom: 16px;
    padding-left: 12px;
    border-left: 3px solid #3b82f6;
}

/* ── INSIGHT PILLS ── */
.insight-pill {
    display: inline-flex; align-items: center;
    gap: 6px; padding: 6px 14px;
    border-radius: 100px; font-size: 13px;
    font-weight: 500; margin: 4px;
}
.pill-green { background:#f0fdf4; border:1px solid #bbf7d0; color:#15803d; }
.pill-yellow { background:#fefce8; border:1px solid #fef08a; color:#a16207; }
.pill-blue { background:#eff6ff; border:1px solid #bfdbfe; color:#1d4ed8; }

/* ══════════════════════════════════════
   CHAT — FULL LIGHT FIX
══════════════════════════════════════ */

/* Outer chat wrapper */
.stChatFloatingInputContainer,
[data-testid="stChatInputContainer"],
div[class*="stChatInputContainer"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
}

/* The textarea itself */
[data-testid="stChatInput"],
[data-testid="stChatInput"] textarea,
textarea[data-testid="stChatInput"],
.stChatInputContainer textarea,
div[class*="stChatInput"] textarea {
    background-color: #ffffff !important;
    color: #1e293b !important;
    caret-color: #3b82f6 !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}

/* Placeholder text */
[data-testid="stChatInput"] textarea::placeholder,
.stChatInputContainer textarea::placeholder {
    color: #94a3b8 !important;
}

/* Send button */
[data-testid="stChatInputSubmitButton"] button,
button[kind="primaryFormSubmit"] {
    background-color: #3b82f6 !important;
    border-radius: 8px !important;
    border: none !important;
}
[data-testid="stChatInputSubmitButton"] button svg {
    fill: #ffffff !important;
}

/* Chat message bubbles */
[data-testid="stChatMessage"] {
    background-color: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div {
    color: #1e293b !important;
}
/* User bubble slightly different */
[data-testid="stChatMessage"][data-testid*="user"] {
    background-color: #eff6ff !important;
    border-color: #bfdbfe !important;
}

/* ── ALERTS ── */
.stSuccess > div, .stInfo > div, .stWarning > div {
    border-radius: 12px !important;
    font-size: 14px !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* ── DIVIDER ── */
hr { border-color: #e2e8f0 !important; margin: 12px 0 !important; }

</style>
""", unsafe_allow_html=True)

# ================= PLOTLY LIGHT THEME =================
CHART_COLORWAY = ["#3b82f6", "#7c3aed", "#22c55e", "#f59e0b", "#ef4444", "#06b6d4"]

CHART_THEME = dict(
    template="plotly_white",
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font=dict(family="DM Sans", color="#475569", size=12),
    margin=dict(l=16, r=16, t=36, b=16),
    colorway=CHART_COLORWAY,
    legend=dict(
        bgcolor="#ffffff",
        bordercolor="#e2e8f0",
        borderwidth=1,
        font=dict(color="#334155")
    )
)

def style_chart(fig):
    fig.update_layout(**CHART_THEME)
    fig.update_xaxes(
        gridcolor="#f1f5f9", zeroline=False, linecolor="#e2e8f0",
        tickfont=dict(color="#64748b"), title_font=dict(color="#475569")
    )
    fig.update_yaxes(
        gridcolor="#f1f5f9", zeroline=False, linecolor="#e2e8f0",
        tickfont=dict(color="#64748b"), title_font=dict(color="#475569")
    )
    return fig

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("""
    <div style="padding:24px 0 8px; text-align:center;">
        <div style="font-family:'Syne',sans-serif; font-size:20px; font-weight:800;
                    background:linear-gradient(135deg,#1d4ed8,#7c3aed);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text; margin-bottom:2px;">
            RI System
        </div>
        <div style="font-size:10px; color:#94a3b8; letter-spacing:0.12em; font-weight:600;">
            RETAIL INTELLIGENCE
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    file = st.file_uploader("Upload CSV Dataset", type=["csv"])
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    chart_type = st.selectbox("Visualization Style",
                              ["Bar Chart", "Pie Chart", "Line Chart", "Area Chart"])

    if file:
        st.markdown("""
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px;
                    padding:10px 14px; margin-top:14px; font-size:13px;
                    color:#15803d; font-weight:600;">
            ✓ Dataset loaded successfully
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:32px; text-align:center; font-size:11px; color:#cbd5e1;">
    Built for scale
    </div>
    """, unsafe_allow_html=True)

# ================= LOAD DATA =================
df = None
if file:
    df = pd.read_csv(file)
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# ================= HEADER =================
st.markdown("""
<div class="dash-header">
    <div class="dash-badge">🛒 Retail Intelligence Platform</div>
    <h1 class="dash-title">Retail Intelligence System</h1>
    <p class="dash-sub">Real-time analytics · AI-powered insights · Business clarity</p>
</div>
""", unsafe_allow_html=True)

# ================= TABS =================
tab1, tab2, tab3, tab4 = st.tabs([
    "  📊  Dashboard  ",
    "  📈  Analytics  ",
    "  🧠  ML Insights  ",
    "  🤖  AI Assistant  "
])

# ══════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════
with tab1:
    if df is not None:
        revenue   = (df["Quantity"] * df["Price"]).sum()
        orders    = len(df)
        avg_qty   = df["Quantity"].mean()
        avg_price = df["Price"].mean() if "Price" in df.columns else 0

        c1, c2, c3, c4 = st.columns(4, gap="medium")
        with c1:
            st.markdown(f"""<div class="kpi-wrap">
                <span class="kpi-icon">💰</span>
                <div class="kpi-label">Total Revenue</div>
                <div class="kpi-value">₹{revenue:,.0f}</div>
                <div class="kpi-delta">↑ All time</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="kpi-wrap">
                <span class="kpi-icon">📦</span>
                <div class="kpi-label">Total Orders</div>
                <div class="kpi-value">{orders:,}</div>
                <div class="kpi-delta">↑ Total records</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="kpi-wrap">
                <span class="kpi-icon">📊</span>
                <div class="kpi-label">Avg Quantity</div>
                <div class="kpi-value">{avg_qty:.1f}</div>
                <div class="kpi-delta">Per order</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="kpi-wrap">
                <span class="kpi-icon">🏷️</span>
                <div class="kpi-label">Avg Price</div>
                <div class="kpi-value">₹{avg_price:.0f}</div>
                <div class="kpi-delta">Per unit</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Product Performance</div>', unsafe_allow_html=True)

        sales = df.groupby("Product")["Quantity"].sum().reset_index()

        if chart_type == "Bar Chart":
            fig = px.bar(sales, x="Product", y="Quantity",
                         color="Product", color_discrete_sequence=CHART_COLORWAY)
            fig.update_traces(marker_line_width=0, opacity=0.88)
        elif chart_type == "Pie Chart":
            fig = px.pie(sales, names="Product", values="Quantity",
                         color_discrete_sequence=CHART_COLORWAY)
            fig.update_traces(textfont_size=12, hole=0.38)
        elif chart_type == "Area Chart":
            fig = px.area(sales, x="Product", y="Quantity",
                          color_discrete_sequence=CHART_COLORWAY)
        else:
            fig = px.line(sales, x="Product", y="Quantity", markers=True,
                          color_discrete_sequence=CHART_COLORWAY)

        fig = style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if "Price" in df.columns:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Revenue by Product</div>', unsafe_allow_html=True)
            rev_df = df.copy()
            rev_df["Revenue"] = rev_df["Quantity"] * rev_df["Price"]
            rev_grouped = rev_df.groupby("Product")["Revenue"].sum().reset_index()
            fig2 = px.bar(rev_grouped, x="Revenue", y="Product", orientation="h",
                          color="Revenue",
                          color_continuous_scale=["#bfdbfe", "#3b82f6", "#1d4ed8"])
            fig2 = style_chart(fig2)
            fig2.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align:center; padding:80px 20px; background:#ffffff;
                    border-radius:16px; border:1px solid #e2e8f0; margin-top:20px;">
            <div style="font-size:52px; margin-bottom:16px;">📂</div>
            <div style="font-family:'Syne',sans-serif; font-size:20px; font-weight:700;
                        color:#0f172a; margin-bottom:8px;">Upload your dataset to get started</div>
            <div style="color:#94a3b8; font-size:14px;">
                Use the sidebar to upload a CSV with columns:
                <strong style="color:#3b82f6;">Product, Quantity, Price, Date</strong>
            </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 2 — ANALYTICS
# ══════════════════════════════════════════════
with tab2:
    if df is not None:
        if "Date" in df.columns:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Sales Trend Over Time</div>', unsafe_allow_html=True)
            trend = df.groupby("Date")["Quantity"].sum().reset_index()
            fig = px.area(trend, x="Date", y="Quantity", color_discrete_sequence=["#3b82f6"])
            fig.update_traces(fill="tozeroy", fillcolor="rgba(59,130,246,0.07)", line_width=2.5)
            fig = style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if "Price" in df.columns and "Date" in df.columns:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Revenue Trend Over Time</div>', unsafe_allow_html=True)
            df_copy = df.copy()
            df_copy["Revenue"] = df_copy["Quantity"] * df_copy["Price"]
            rev_trend = df_copy.groupby("Date")["Revenue"].sum().reset_index()
            fig = px.line(rev_trend, x="Date", y="Revenue", color_discrete_sequence=["#7c3aed"])
            fig.update_traces(line_width=2.5)
            fig = style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Quantity Distribution</div>', unsafe_allow_html=True)
            fig = px.histogram(df, x="Quantity", nbins=20, color_discrete_sequence=["#3b82f6"])
            fig = style_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            if "Price" in df.columns:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Price Distribution</div>', unsafe_allow_html=True)
                fig = px.histogram(df, x="Price", nbins=20, color_discrete_sequence=["#7c3aed"])
                fig = style_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("⬅️ Upload a dataset from the sidebar to view analytics.")

# ══════════════════════════════════════════════
# TAB 3 — ML INSIGHTS
# ══════════════════════════════════════════════
with tab3:
    if df is not None:
        product_sales = df.groupby("Product")["Quantity"].sum()
        top     = product_sales.idxmax()
        low     = product_sales.idxmin()
        top_val = product_sales.max()
        low_val = product_sales.min()

        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.markdown(f"""<div class="kpi-wrap">
                <span class="kpi-icon">🏆</span>
                <div class="kpi-label">Top Performer</div>
                <div class="kpi-value" style="font-size:22px;">{top}</div>
                <div class="kpi-delta">↑ {top_val:,} units sold</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""<div class="kpi-wrap" style="border-top:3px solid #ef4444;">
                <span class="kpi-icon">⚠️</span>
                <div class="kpi-label">Needs Attention</div>
                <div class="kpi-value" style="font-size:22px;">{low}</div>
                <div class="kpi-delta" style="color:#ef4444;">↓ {low_val:,} units sold</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">AI-Generated Insights</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px;">
            <span class="insight-pill pill-green">✓ Promote {top}</span>
            <span class="insight-pill pill-yellow">⚠ Review {low} strategy</span>
            <span class="insight-pill pill-blue">📦 {len(product_sales)} products tracked</span>
        </div>""", unsafe_allow_html=True)

        sorted_sales = product_sales.sort_values(ascending=True).reset_index()
        sorted_sales.columns = ["Product", "Quantity"]
        fig = px.bar(sorted_sales, x="Quantity", y="Product", orientation="h",
                     color="Quantity",
                     color_continuous_scale=["#fca5a5", "#fbbf24", "#4ade80"],
                     title="Product Ranking by Sales Volume")
        fig = style_chart(fig)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("⬅️ Upload a dataset from the sidebar to generate insights.")

# ══════════════════════════════════════════════
# TAB 4 — AI ASSISTANT
# ══════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div style="text-align:center; padding:24px 0 16px;">
        <div style="font-family:'Syne',sans-serif; font-size:22px; font-weight:700; color:#0f172a;">
            AI Business Assistant
        </div>
        <div style="color:#94a3b8; font-size:13px; margin-top:4px;">
            Ask anything about your retail data
        </div>
    </div>""", unsafe_allow_html=True)

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user = st.chat_input("Ask about products, revenue, trends...")

    if user:
        st.session_state.chat.append({"role": "user", "content": user})

        with st.chat_message("assistant"):
            try:
                client = OpenAI(
                    api_key=os.getenv("GROQ_API_KEY"),
                    base_url="https://api.groq.com/openai/v1"
                )

                if df is not None:
                    revenue       = (df["Quantity"] * df["Price"]).sum()
                    product_sales = df.groupby("Product")["Quantity"].sum()
                    top           = product_sales.idxmax()
                    low           = product_sales.idxmin()
                    n_products    = len(product_sales)

                    summary = f"""You are a retail business intelligence assistant.
Current dataset summary:
- Total Revenue: ₹{revenue:,.0f}
- Total Orders: {len(df)}
- Number of Products: {n_products}
- Top Product: {top} ({product_sales.max():,} units)
- Weakest Product: {low} ({product_sales.min():,} units)
- Average Order Quantity: {df['Quantity'].mean():.2f}
Provide concise, actionable insights. Be direct and data-driven."""
                else:
                    summary = "You are a retail business assistant. No data has been uploaded yet. Ask the user to upload a CSV file."

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": summary},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.chat[:-1]],
                        {"role": "user", "content": user}
                    ]
                )
                reply = response.choices[0].message.content

            except Exception as e:
                reply = f"⚠️ Could not connect to AI service. Please check your GROQ_API_KEY.\n\nError: {str(e)}"

            st.markdown(reply)

        st.session_state.chat.append({"role": "assistant", "content": reply})