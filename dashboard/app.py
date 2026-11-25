import os                                         # to find the database
import sqlite3                                    # to open it
import pandas as pd                               # to hold query rows
import plotly.express as px                       # to draw the charts
import streamlit as st                            # to build the page

st.set_page_config(page_title="AIRTEL TELECOM ANALYSIS", layout="wide")

HERE = os.path.dirname(os.path.abspath(__file__)) # the dashboard folder
DB = os.path.join(HERE, "..", "data", "raw", "airtel.db")

T7_P_VALUE = "p < 0.0001"


@st.cache_data
def q(sql: str, params: tuple = ()) -> pd.DataFrame:
    """Helper function to query SQLite database and cache results."""
    with sqlite3.connect(DB) as conn:
        return pd.read_sql_query(sql, conn, params=params)


# ==============================================================================
# CINEMATIC PEACH & OLIVE THEME CONSTANTS
# ==============================================================================
BG_MAIN = "#070A09"         # Deep Cinema Obsidian
BG_SIDEBAR = "#0C1210"      # Theater Side Panel
BG_CARD = "#141E1B"         # Translucent Smoked Card
BORDER_CARD = "#2B3E38"     # Subtle Rim Border
PEACH_ACCENT = "#F48C72"    # Warm Cinema Peach
PEACH_SOFT = "#F7B29E"      # Soft Peach Highlight
OLIVE_POSITIVE = "#93BD6B"  # Luminous Olive Sage
ACCENT_GOLD = "#FBBF24"     # Reference Marker Gold
MUTED_SLATE = "#64748B"     # Neutral Baseline
TEXT_WHITE = "#F8FAFC"
TEXT_MUTED = "#A7B8B2"

# ==============================================================================
# CSS STYLING
# ==============================================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, .stApp {{
        background:
            radial-gradient(circle at 18% 12%, rgba(244, 140, 114, 0.11) 0%, transparent 38%),
            radial-gradient(circle at 85% 22%, rgba(147, 189, 107, 0.09) 0%, transparent 42%),
            radial-gradient(circle at 50% 95%, rgba(244, 140, 114, 0.06) 0%, transparent 50%),
            {BG_MAIN};
        color: {TEXT_WHITE};
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* Subtle Analog Film Grain Overlay */
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 999;
        opacity: 0.032;
        background-image: radial-gradient(rgba(255, 255, 255, 0.65) 0.6px, transparent 0.6px);
        background-size: 3px 3px;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(16, 24, 21, 0.96) 0%, rgba(7, 10, 9, 0.98) 100%);
        backdrop-filter: blur(14px);
        border-right: 1px solid {BORDER_CARD};
        min-width: 268px !important;
        box-shadow: 8px 0 28px rgba(0, 0, 0, 0.55);
    }}

    [data-testid="stMainBlockContainer"] {{
        padding-top: 1.05rem !important;
        padding-bottom: 1.15rem !important;
        padding-left: 1.85rem !important;
        padding-right: 1.85rem !important;
        max-width: 100% !important;
    }}

    [data-testid="stHeader"] {{
        background-color: transparent;
        height: 0rem;
    }}

    /* Cinematic Main Title */
    h1 {{
        font-size: 2.35rem !important;
        font-weight: 900 !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
        background: linear-gradient(90deg, {TEXT_WHITE} 0%, {PEACH_SOFT} 65%, {OLIVE_POSITIVE} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 3px 16px rgba(244, 140, 114, 0.25));
        position: relative !important;
        z-index: 5 !important;
        transform: translateY(10px) !important;
        line-height: 1.2 !important;
        margin-bottom: 0.55rem !important;
    }}
    h1 a {{
        display: none !important;
    }}

    .sidebar-section-title {{
        font-size: 0.72rem;
        font-weight: 700;
        color: {TEXT_MUTED};
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin: 1.05rem 0 0.45rem 0;
    }}

    .sidebar-info-box {{
        background: linear-gradient(150deg, rgba(28, 41, 37, 0.78) 0%, rgba(14, 20, 18, 0.92) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid {BORDER_CARD};
        border-left: 4px solid {PEACH_ACCENT};
        border-radius: 13px;
        padding: 0.92rem;
        margin-top: 1.1rem;
        width: 100%;
        box-sizing: border-box;
        font-size: 0.8rem;
        color: {TEXT_MUTED};
        line-height: 1.5;
        box-shadow: 0 12px 26px rgba(0, 0, 0, 0.45);
    }}

    /* Glassmorphic Pill Tabs */
    div[data-testid="stSidebar"] div[role="radiogroup"] {{
        display: flex;
        flex-direction: column;
        gap: 7px;
    }}
    div[data-testid="stSidebar"] div[role="radiogroup"] > label {{
        background: rgba(255, 255, 255, 0.025);
        backdrop-filter: blur(10px);
        border: 1px solid {BORDER_CARD};
        padding: 10px 14px;
        border-radius: 11px;
        margin-bottom: 0;
        font-size: 0.92rem !important;
        font-weight: 600;
        color: {TEXT_WHITE} !important;
        cursor: pointer;
        transition: all 0.22s ease;
    }}
    div[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{
        background: rgba(244, 140, 114, 0.11);
        border-color: rgba(244, 140, 114, 0.52);
        transform: translateX(3px);
    }}
    div[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {{
        background: linear-gradient(135deg, {PEACH_ACCENT} 0%, {PEACH_SOFT} 100%) !important;
        border-color: {PEACH_SOFT} !important;
        font-weight: 800;
        color: {BG_MAIN} !important;
        box-shadow: 0 8px 24px rgba(244, 140, 114, 0.34);
    }}

    /* Multi-Select Dropdown & Tags */
    div[data-testid="stSidebar"] div[data-testid="stMultiSelect"] label {{
        color: #E2E8F0 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }}
    div[data-testid="stSidebar"] div[data-testid="stMultiSelect"] > div > div {{
        background-color: rgba(20, 30, 27, 0.85) !important;
        border: 1px solid {BORDER_CARD} !important;
        border-radius: 10px !important;
        color: {TEXT_WHITE} !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }}
    div[data-testid="stSidebar"] div[data-testid="stMultiSelect"] > div > div:hover {{
        border-color: {PEACH_ACCENT} !important;
        box-shadow: 0 0 0 1px rgba(244, 140, 114, 0.25);
    }}
    div[data-testid="stSidebar"] span[data-baseweb="tag"] {{
        background: linear-gradient(135deg, rgba(244, 140, 114, 0.32) 0%, rgba(147, 189, 107, 0.22) 100%) !important;
        border: 1px solid rgba(244, 140, 114, 0.65) !important;
        color: {TEXT_WHITE} !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
    }}

    .sub-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0 0.78rem 0;
        border-bottom: 1.5px solid rgba(244, 140, 114, 0.75);
        box-shadow: 0 6px 16px -10px rgba(244, 140, 114, 0.45);
        margin-bottom: 1.1rem;
        gap: 16px;
        line-height: 1.4;
    }}

    /* Cinematic Glass KPI Cards */
    .kpi-card {{
        background: linear-gradient(150deg, rgba(27, 40, 36, 0.82) 0%, rgba(14, 21, 19, 0.92) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid {BORDER_CARD};
        border-radius: 15px;
        padding: 1.05rem 1.25rem;
        min-height: 106px;
        display: flex;
        align-items: center;
        gap: 16px;
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.48), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
    }}
    .kpi-card:hover {{
        transform: translateY(-3px);
        border-color: {PEACH_ACCENT};
        box-shadow: 0 18px 36px rgba(0, 0, 0, 0.6), 0 0 22px rgba(244, 140, 114, 0.16);
    }}
    .kpi-icon {{
        font-size: 1.85rem;
        width: 56px;
        height: 56px;
        border-radius: 13px;
        background: linear-gradient(135deg, rgba(244, 140, 114, 0.24) 0%, rgba(147, 189, 107, 0.12) 100%);
        border: 1px solid rgba(244, 140, 114, 0.42);
        color: {PEACH_SOFT};
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: inset 0 0 12px rgba(244, 140, 114, 0.14);
    }}
    .kpi-value {{
        font-size: 1.65rem;
        font-weight: 800;
        color: {TEXT_WHITE};
        line-height: 1.15;
        letter-spacing: -0.4px;
    }}
    .kpi-label {{
        font-size: 0.85rem;
        color: {TEXT_MUTED};
        margin-top: 3px;
        font-weight: 600;
    }}
    .fixed-pill {{
        background: linear-gradient(90deg, {OLIVE_POSITIVE} 0%, #769E52 100%);
        color: {BG_MAIN};
        font-size: 0.63rem;
        font-weight: 800;
        letter-spacing: 0.7px;
        padding: 2px 8px;
        border-radius: 999px;
        margin-left: 8px;
        vertical-align: middle;
    }}

    /* Cinematic Chart Containers */
    div[data-testid="stPlotlyChart"] {{
        background: linear-gradient(155deg, rgba(24, 36, 32, 0.8) 0%, rgba(13, 19, 17, 0.92) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid {BORDER_CARD};
        border-radius: 15px;
        padding: 10px 12px 6px 12px;
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.48), inset 0 1px 0 rgba(255, 255, 255, 0.04);
        transition: border-color 0.22s ease, box-shadow 0.22s ease;
    }}
    div[data-testid="stPlotlyChart"]:hover {{
        border-color: rgba(244, 140, 114, 0.52);
        box-shadow: 0 18px 36px rgba(0, 0, 0, 0.58), 0 0 24px rgba(147, 189, 107, 0.08);
    }}

    .provenance-line {{
        font-size: 0.78rem;
        color: {TEXT_MUTED};
        text-align: right;
        margin-top: 0.65rem;
        font-weight: 500;
        letter-spacing: 0.2px;
    }}
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def render_card(icon, value, label="", sub="", fixed=False):
    badge = '<span class="fixed-pill">FIXED</span>' if fixed else ""
    label_html = f'<div class="kpi-label">{label}</div>' if label else ""
    sub_html = f'<div style="font-size:0.76rem;color:#E2E8F0;margin-top:3px;font-weight:500;">{sub}</div>' if sub else ""
    html = (
        f'<div class="kpi-card">'
        f'<div class="kpi-icon">{icon}</div>'
        f'<div>'
        f'<div class="kpi-value">{value}{badge}</div>'
        f'{label_html}'
        f'{sub_html}'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def apply_dark_chart(fig, title, height=345):
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, weight=700, color=TEXT_WHITE)),
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(7, 10, 9, 0.35)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color=TEXT_MUTED, size=12),
        margin=dict(l=20, r=24, t=48, b=42),
        xaxis=dict(showgrid=False, zeroline=False, color=TEXT_MUTED),
        yaxis=dict(showgrid=True, gridcolor="rgba(147, 189, 107, 0.14)", zeroline=False, color=TEXT_MUTED),
    )
    return fig


# ==============================================================================
# MAIN TITLE
# ==============================================================================
st.title("AIRTEL TELECOM ANALYSIS")

# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    st.markdown(
        f'<div style="display:flex; align-items:center; gap:12px; margin-bottom:0.85rem; padding-top:0.25rem;">'
        f'<svg width="38" height="38" viewBox="0 0 100 100" fill="none">'
        f'<path d="M68 18C48 16 24 32 18 50C14 62 24 68 35 61C48 53 60 40 71 42C80 44 79 58 67 70C57 80 43 85 38 81C34 78 39 70 46 65C51 61 48 54 41 57C31 62 24 75 30 85C37 96 60 90 76 74C92 58 94 21 68 18Z" fill="{PEACH_ACCENT}"/>'
        f'</svg>'
        f'<div><div style="font-size:1.95rem; font-weight:800; color:{PEACH_ACCENT}; letter-spacing:-0.7px; line-height:1;">airtel</div></div>'
        f'</div>'
        f'<div style="height:1px; background:linear-gradient(90deg, {PEACH_ACCENT} 0%, {OLIVE_POSITIVE} 55%, rgba(244,140,114,0.05) 100%); margin-bottom:0.9rem;"></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-section-title">Tabs (Domain D)</div>', unsafe_allow_html=True)
    active_tab = st.radio("Navigation", ["Overview", "Category Detail"], label_visibility="collapsed")

    st.markdown('<div class="sidebar-section-title">Filters (Multi-Select)</div>', unsafe_allow_html=True)
    conn_options = q("SELECT DISTINCT connection_type FROM customer_features ORDER BY connection_type")["connection_type"].tolist()
    region_options = q("SELECT DISTINCT region FROM customer_features ORDER BY region")["region"].tolist()

    selected_conn = st.multiselect("Connection Type", conn_options, placeholder="All Connection Types")
    selected_region = st.multiselect("Region", region_options, placeholder="All Regions")

    conn_summary = ", ".join(selected_conn) if selected_conn else "All Types"
    region_summary = ", ".join(selected_region) if selected_region else "All Regions"

    st.markdown(
        f'<div class="sidebar-info-box">'
        f'<strong style="color:{TEXT_WHITE}; font-size:0.85rem;">Airtel Telecom Analytics</strong><br>'
        f'Customer Service Dashboard (Jan–Jun 2025).<br>'
        f'<div style="margin-top:0.55rem; padding-top:0.5rem; border-top:1px solid rgba(147,189,107,0.22); font-size:0.74rem; color:#E2E8F0;">'
        f'<div><span style="color:{PEACH_SOFT}; font-weight:600;">Conn:</span> {conn_summary}</div>'
        f'<div style="margin-top:2px;"><span style="color:{OLIVE_POSITIVE}; font-weight:600;">Region:</span> {region_summary}</div>'
        f'</div>'
        f'<div style="margin-top:0.5rem; font-size:0.72rem; color:{TEXT_MUTED};">Note: T7 shows an association (a link only), not causation.</div>'
        f'</div>'
        f'<div style="margin-top:0.85rem; text-align:center; font-size:0.68rem; font-weight:700; letter-spacing:1.2px; color:#64748B;">DOMAIN D · CUSTOMER SERVICE</div>',
        unsafe_allow_html=True,
    )

# ==============================================================================
# DYNAMIC FILTERS & SUB-HEADER
# ==============================================================================
where = "WHERE 1=1"
params = []
if selected_conn:
    placeholders = ", ".join(["?"] * len(selected_conn))
    where += f" AND c.connection_type IN ({placeholders})"
    params.extend(selected_conn)
if selected_region:
    placeholders = ", ".join(["?"] * len(selected_region))
    where += f" AND c.region IN ({placeholders})"
    params.extend(selected_region)
params = tuple(params)

st.markdown(
    f'<div class="sub-header">'
    f'<div style="font-size:1.05rem; color:{TEXT_MUTED}; font-weight:600;">Customer Service Dashboard – <span style="color:{PEACH_ACCENT}; font-weight:800;">{active_tab}</span></div>'
    f'<div style="font-size:0.86rem; font-style:italic; color:#CBD5E1; text-align:right;">For the Head of Customer Service: decide where support-team effort should be focused first.</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# ==============================================================================
# TAB 1: OVERVIEW
# ==============================================================================
if active_tab == "Overview":
    ov_card1 = q("""
        SELECT COUNT(*) AS total_tickets
        FROM complaints
        WHERE complaint_date BETWEEN '2025-01-01' AND '2025-06-30'
    """).iloc[0]

    ov_card3 = q(f"""
        SELECT
            SUM(CASE WHEN t.is_resolved = 0 THEN 1 ELSE 0 END) AS open_tickets,
            ROUND(100.0 * SUM(CASE WHEN t.is_resolved = 0 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 1) AS open_pct,
            COUNT(*) AS filtered_total
        FROM complaints t
        JOIN customer_features c ON t.customer_id = c.customer_id
        {where}
          AND t.complaint_date BETWEEN '2025-01-01' AND '2025-06-30'
    """, params).iloc[0]

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        render_card("🎫", f"{int(ov_card1['total_tickets']):,}", "Total Tickets (Jan–Jun 2025)", "Before filters", fixed=True)
    with c2:
        render_card(icon="📈", value="Higher Churn", sub=f"Two-tailed {T7_P_VALUE} · a link only", fixed=True)
    with c3:
        render_card("⏳", f"{int(ov_card3['open_tickets'] or 0):,} ({ov_card3['open_pct'] or 0.0}%)", "Tickets Still Open", f"Of {int(ov_card3['filtered_total'] or 0):,} filtered tickets")

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    hero_ov_df = q(f"""
        WITH ref_line AS (
            SELECT ROUND(100.0 * AVG(c.is_churned), 1) AS filter_churn_rate
            FROM customer_features c
            {where}
        )
        SELECT
            CASE
                WHEN c.complaint_count = 0 THEN 'Never complained'
                WHEN c.unresolved_count = 0 THEN 'All tickets closed'
                ELSE 'One ticket still open'
            END AS history_group,
            CASE WHEN c.complaint_count = 0 THEN 1 WHEN c.unresolved_count = 0 THEN 2 ELSE 3 END AS sort_order,
            COUNT(*) AS sub_count,
            ROUND(100.0 * AVG(c.is_churned), 1) AS churn_rate,
            r.filter_churn_rate
        FROM customer_features c
        CROSS JOIN ref_line r
        {where}
        GROUP BY history_group, sort_order, r.filter_churn_rate
        ORDER BY sort_order
    """, params + params)

    sup1_ov_df = q(f"""
        SELECT
            t.category,
            CASE WHEN t.is_resolved = 1 THEN 'Closed' ELSE 'Open' END AS status,
            COUNT(*) AS ticket_count
        FROM complaints t
        JOIN customer_features c ON t.customer_id = c.customer_id
        {where}
          AND t.complaint_date BETWEEN '2025-01-01' AND '2025-06-30'
        GROUP BY t.category, status
        ORDER BY t.category, status
    """, params)

    col_hero, col_right = st.columns([1.05, 1.15], gap="medium")
    with col_hero:
        if not hero_ov_df.empty:
            ref_val = hero_ov_df["filter_churn_rate"].iloc[0]
            open_row = hero_ov_df[hero_ov_df["history_group"] == "One ticket still open"]
            top_rate = open_row["churn_rate"].iloc[0] if not open_row.empty else ref_val
            fig_hero = px.bar(
                hero_ov_df, x="history_group", y="churn_rate",
                text=hero_ov_df.apply(lambda r: f"{r['churn_rate']}%<br>(n={int(r['sub_count']):,})", axis=1),
                color="history_group",
                color_discrete_map={"Never complained": MUTED_SLATE, "All tickets closed": OLIVE_POSITIVE, "One ticket still open": PEACH_ACCENT},
            )
            fig_hero.add_hline(
                y=ref_val,
                line_dash="dash",
                line_width=2,
                line_color=ACCENT_GOLD,
                annotation_text=f"Filtered churn: {ref_val}%",
                annotation_position="top left",
                annotation_font=dict(size=11, color=ACCENT_GOLD),
            )
            fig_hero.update_traces(textposition="outside", textfont=dict(size=11, color=TEXT_WHITE), marker_line_width=0, cliponaxis=False)
            apply_dark_chart(fig_hero, f"Open-ticket subscribers show {top_rate}% churn (a link only)", height=350)
            fig_hero.update_layout(
                showlegend=False,
                xaxis_title="Complaint History",
                yaxis_title="Churn Rate (%)",
                xaxis_title_font=dict(size=12, color=TEXT_WHITE),
                yaxis_title_font=dict(size=12, color=TEXT_WHITE),
                margin=dict(l=62, r=24, t=54, b=52),
            )
            st.plotly_chart(fig_hero, width="stretch")

    with col_right:
        if not sup1_ov_df.empty:
            cat_order = (
                sup1_ov_df.groupby("category")["ticket_count"]
                .sum()
                .sort_values(ascending=False)
                .index.tolist()
            )
            fig_hist = px.histogram(
                sup1_ov_df,
                x="category",
                y="ticket_count",
                color="status",
                histfunc="sum",
                category_orders={"category": cat_order, "status": ["Closed", "Open"]},
                color_discrete_map={"Closed": OLIVE_POSITIVE, "Open": PEACH_ACCENT},
            )
            fig_hist.update_traces(
                marker_line_color=BG_MAIN,
                marker_line_width=1.2,
                opacity=0.92,
                cliponaxis=False,
            )
            apply_dark_chart(fig_hist, "Tickets by Category · Closed vs Open", height=350)
            fig_hist.update_layout(
                barmode="group",
                bargap=0.22,
                bargroupgap=0.08,
                xaxis_title="Category",
                yaxis_title="Ticket Volume",
                xaxis_title_font=dict(size=12, color=TEXT_WHITE),
                yaxis_title_font=dict(size=12, color=TEXT_WHITE),
                legend=dict(
                    title=dict(text="Status", font=dict(size=11, color=TEXT_WHITE)),
                    font=dict(size=10, color=TEXT_WHITE),
                    bgcolor="rgba(14, 21, 19, 0.75)",
                    bordercolor=BORDER_CARD,
                    borderwidth=1,
                ),
                margin=dict(l=62, r=24, t=54, b=62),
            )
            st.plotly_chart(fig_hist, width="stretch")

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    bottom_ov_df = q(f"""
        WITH circle_subs AS (
            SELECT c.circle_name, COUNT(*) AS sub_count
            FROM customer_features c
            {where}
            GROUP BY c.circle_name
        ),
        circle_tkts AS (
            SELECT c.circle_name, COUNT(t.complaint_id) AS ticket_count
            FROM complaints t
            JOIN customer_features c ON t.customer_id = c.customer_id
            {where}
              AND t.complaint_date BETWEEN '2025-01-01' AND '2025-06-30'
            GROUP BY c.circle_name
        )
        SELECT
            cs.circle_name,
            cs.sub_count,
            COALESCE(ct.ticket_count, 0) AS ticket_count,
            ROUND(100.0 * COALESCE(ct.ticket_count, 0) / NULLIF(cs.sub_count, 0), 1) AS tickets_per_100
        FROM circle_subs cs
        LEFT JOIN circle_tkts ct ON cs.circle_name = ct.circle_name
        ORDER BY tickets_per_100 DESC
    """, params + params)

    if not bottom_ov_df.empty:
        top_circle, top_100 = bottom_ov_df.iloc[0]["circle_name"], bottom_ov_df.iloc[0]["tickets_per_100"]
        bar_colors = [PEACH_ACCENT if i == 0 else OLIVE_POSITIVE for i in range(len(bottom_ov_df))]
        fig_bot = px.bar(
            bottom_ov_df, x="circle_name", y="tickets_per_100",
            text=bottom_ov_df.apply(lambda r: f"{r['tickets_per_100']}<br>(n={int(r['sub_count']):,})", axis=1),
        )
        fig_bot.update_traces(marker_color=bar_colors, textposition="outside", textfont=dict(size=10, color=TEXT_WHITE), cliponaxis=False)
        apply_dark_chart(fig_bot, f"{top_circle} leads complaint intensity at {top_100} tickets per 100 subscribers (all circles shown)", height=285)
        fig_bot.update_layout(
            xaxis_title="Telecom Circles",
            yaxis_title="Tickets per 100 Subs",
            xaxis_title_font=dict(size=12, color=TEXT_WHITE),
            yaxis_title_font=dict(size=12, color=TEXT_WHITE),
            margin=dict(l=65, r=24, t=52, b=72),
        )
        st.plotly_chart(fig_bot, width="stretch")

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.dataframe(
            bottom_ov_df.head(5).rename(columns={
                "circle_name": "Telecom Circle",
                "sub_count": "Subscribers",
                "ticket_count": "Tickets",
                "tickets_per_100": "Tickets per 100 Subs",
            }),
            use_container_width=True,
            hide_index=True,
        )

# ==============================================================================
# TAB 2: CATEGORY DETAIL
# ==============================================================================
else:
    cat_list_df = q(f"""
        SELECT t.category, COUNT(*) AS cnt
        FROM complaints t
        JOIN customer_features c ON t.customer_id = c.customer_id
        {where}
          AND t.complaint_date BETWEEN '2025-01-01' AND '2025-06-30'
        GROUP BY t.category
        ORDER BY cnt DESC
        LIMIT 6
    """, params)
    categories = cat_list_df["category"].tolist() if not cat_list_df.empty else ["No Data"]

    d_c1, d_c2, d_c3, d_sel = st.columns([1.1, 1.1, 1.1, 0.9], gap="medium")
    with d_sel:
        selected_cat = st.selectbox("Category (most tickets first)", categories)

    cat_params = params + (selected_cat,)

    det_cards = q(f"""
        WITH all_filtered AS (
            SELECT COUNT(*) AS total_all
            FROM complaints t JOIN customer_features c ON t.customer_id = c.customer_id
            {where} AND t.complaint_date BETWEEN '2025-01-01' AND '2025-06-30'
        ),
        cat_tkts AS (
            SELECT
                COUNT(*) AS cat_total,
                ROUND(100.0 * AVG(t.is_resolved), 1) AS closed_pct,
                ROUND(AVG(CASE WHEN t.is_resolved = 1 THEN t.resolution_days END), 1) AS avg_days_closed
            FROM complaints t JOIN customer_features c ON t.customer_id = c.customer_id
            {where} AND t.complaint_date BETWEEN '2025-01-01' AND '2025-06-30'
              AND t.category = ?
        ),
        open_subs AS (
            SELECT
                COUNT(DISTINCT c.customer_id) AS subs_with_open,
                COUNT(DISTINCT CASE WHEN c.is_churned = 1 THEN c.customer_id END) AS open_subs_left
            FROM complaints t JOIN customer_features c ON t.customer_id = c.customer_id
            {where} AND t.complaint_date BETWEEN '2025-01-01' AND '2025-06-30'
              AND t.category = ? AND t.is_resolved = 0
        )
        SELECT
            ct.cat_total,
            ROUND(100.0 * ct.cat_total / NULLIF(a.total_all, 0), 1) AS cat_share_pct,
            ct.closed_pct, ct.avg_days_closed, o.subs_with_open, o.open_subs_left
        FROM cat_tkts ct CROSS JOIN all_filtered a CROSS JOIN open_subs o
    """, params + cat_params + cat_params).iloc[0]

    with d_c1:
        render_card("📂", f"{int(det_cards['cat_total'] or 0):,}", f"{selected_cat} Tickets", f"{det_cards['cat_share_pct'] or 0.0}% share of all tickets")
    with d_c2:
        render_card("✅", f"{det_cards['closed_pct'] or 0.0}%", "Tickets Closed", f"Avg {det_cards['avg_days_closed'] or 0.0} days to close")
    with d_c3:
        render_card("🚪", f"{int(det_cards['subs_with_open'] or 0):,}", "Subs with Open Ticket", f"{int(det_cards['open_subs_left'] or 0):,} of them left")

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    det_hero_df = q(f"""
        SELECT strftime('%Y-%m', t.complaint_date) AS month_ym, COUNT(*) AS ticket_count
        FROM complaints t JOIN customer_features c ON t.customer_id = c.customer_id
        {where} AND t.complaint_date BETWEEN '2025-01-01' AND '2025-06-30' AND t.category = ?
        GROUP BY month_ym ORDER BY month_ym
    """, cat_params)

    det_sup1_df = q(f"""
        SELECT
            t.channel,
            CASE WHEN t.is_resolved = 1 THEN 'Closed' ELSE 'Open' END AS status,
            COUNT(*) AS ticket_count
        FROM complaints t JOIN customer_features c ON t.customer_id = c.customer_id
        {where} AND t.complaint_date BETWEEN '2025-01-01' AND '2025-06-30' AND t.category = ?
        GROUP BY t.channel, status
        ORDER BY t.channel, status
    """, cat_params)

    det_bot_df = q(f"""
        WITH cat_subs AS (
            SELECT c.customer_id, c.is_churned, SUM(CASE WHEN t.is_resolved = 0 THEN 1 ELSE 0 END) AS open_cnt
            FROM complaints t JOIN customer_features c ON t.customer_id = c.customer_id
            {where} AND t.complaint_date BETWEEN '2025-01-01' AND '2025-06-30' AND t.category = ?
            GROUP BY c.customer_id, c.is_churned
        ),
        national_ref AS (
            SELECT ROUND(100.0 * AVG(is_churned), 1) AS national_churn_rate FROM customer_features
        )
        SELECT
            CASE WHEN open_cnt = 0 THEN 'All tickets closed' ELSE 'One ticket still open' END AS status_group,
            COUNT(*) AS sub_count, ROUND(100.0 * AVG(is_churned), 1) AS churn_rate, nr.national_churn_rate
        FROM cat_subs CROSS JOIN national_ref nr
        GROUP BY status_group, nr.national_churn_rate ORDER BY status_group
    """, cat_params)

    d_hero, d_right = st.columns([1.05, 1.15], gap="medium")
    with d_hero:
        if not det_hero_df.empty:
            pk = det_hero_df.loc[det_hero_df["ticket_count"].idxmax()]
            fig_dh = px.line(det_hero_df, x="month_ym", y="ticket_count", markers=True, text="ticket_count")
            fig_dh.update_traces(line_color=PEACH_ACCENT, line_width=3.5, marker=dict(size=9, color=TEXT_WHITE, line=dict(width=2, color=PEACH_ACCENT)), textposition="top center", textfont=dict(size=11, color=TEXT_WHITE), cliponaxis=False)
            apply_dark_chart(fig_dh, f"{selected_cat} tickets peaked in {pk['month_ym']} ({int(pk['ticket_count']):,} tickets)", height=350)
            fig_dh.update_layout(
                xaxis_title="Month",
                yaxis_title="Number of Tickets",
                xaxis_title_font=dict(size=12, color=TEXT_WHITE),
                yaxis_title_font=dict(size=12, color=TEXT_WHITE),
                margin=dict(l=62, r=24, t=56, b=52),
            )
            st.plotly_chart(fig_dh, width="stretch")

    with d_right:
        if not det_sup1_df.empty:
            ch_order = (
                det_sup1_df.groupby("channel")["ticket_count"]
                .sum()
                .sort_values(ascending=False)
                .index.tolist()
            )
            fig_d_hist = px.histogram(
                det_sup1_df,
                x="channel",
                y="ticket_count",
                color="status",
                histfunc="sum",
                category_orders={"channel": ch_order, "status": ["Closed", "Open"]},
                color_discrete_map={"Closed": OLIVE_POSITIVE, "Open": PEACH_ACCENT},
            )
            fig_d_hist.update_traces(
                marker_line_color=BG_MAIN,
                marker_line_width=1.2,
                opacity=0.92,
                cliponaxis=False,
            )
            apply_dark_chart(fig_d_hist, f"{selected_cat} by Channel · Closed vs Open", height=350)
            fig_d_hist.update_layout(
                barmode="group",
                bargap=0.22,
                bargroupgap=0.08,
                xaxis_title="Channel",
                yaxis_title="Ticket Volume",
                xaxis_title_font=dict(size=12, color=TEXT_WHITE),
                yaxis_title_font=dict(size=12, color=TEXT_WHITE),
                legend=dict(
                    title=dict(text="Status", font=dict(size=11, color=TEXT_WHITE)),
                    font=dict(size=10, color=TEXT_WHITE),
                    bgcolor="rgba(14, 21, 19, 0.75)",
                    bordercolor=BORDER_CARD,
                    borderwidth=1,
                ),
                margin=dict(l=62, r=24, t=54, b=62),
            )
            st.plotly_chart(fig_d_hist, width="stretch")

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    if not det_bot_df.empty:
        nat_ref = det_bot_df["national_churn_rate"].iloc[0]
        fig_db = px.bar(
            det_bot_df, x="churn_rate", y="status_group", orientation="h",
            text=det_bot_df.apply(lambda r: f"{r['churn_rate']}% (n={int(r['sub_count']):,})", axis=1),
            color="status_group",
            color_discrete_map={"All tickets closed": OLIVE_POSITIVE, "One ticket still open": PEACH_ACCENT},
        )
        fig_db.add_vline(
            x=nat_ref,
            line_dash="dash",
            line_width=2,
            line_color=ACCENT_GOLD,
            annotation_text=f"National churn: {nat_ref}%",
            annotation_position="top right",
            annotation=dict(yshift=14, font=dict(size=11, color=ACCENT_GOLD)),
        )
        fig_db.update_traces(textposition="outside", textfont=dict(size=11, color=TEXT_WHITE), cliponaxis=False)
        apply_dark_chart(fig_db, f"In {selected_cat}, open tickets are linked to higher churn (a link only)", height=275)
        fig_db.update_layout(
            showlegend=False,
            xaxis_title="Churn Rate (%)",
            yaxis_title="",
            xaxis_title_font=dict(size=12, color=TEXT_WHITE),
            yaxis_title_font=dict(size=12, color=TEXT_WHITE),
            margin=dict(l=24, r=55, t=60, b=48),
        )
        st.plotly_chart(fig_db, width="stretch")

    if not det_sup1_df.empty:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        ch_table_df = (
            det_sup1_df.pivot_table(
                index="channel",
                columns="status",
                values="ticket_count",
                aggfunc="sum",
                fill_value=0,
            )
            .reset_index()
        )
        for col in ["Closed", "Open"]:
            if col not in ch_table_df.columns:
                ch_table_df[col] = 0
        ch_table_df["Total Tickets"] = ch_table_df["Closed"] + ch_table_df["Open"]
        ch_table_df = ch_table_df.sort_values("Total Tickets", ascending=False)
        st.dataframe(
            ch_table_df.rename(columns={"channel": "Channel"}),
            use_container_width=True,
            hide_index=True,
        )

st.markdown(
    '<div class="provenance-line">Data provenance: Circle and plan structures are real; subscriber-level records are synthetic.</div>',
    unsafe_allow_html=True,
)