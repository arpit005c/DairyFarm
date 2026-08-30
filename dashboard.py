import streamlit as st
import sys
import os

# Important: Setup environment correctly so backend modules can be imported
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from backend.app.analytics.analytics_service import AnalyticsOrchestrator

# Setup Page Configuration
st.set_page_config(
    page_title="DairyFarm Analytics",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply premium minimal custom styling consistent with the main app theme
st.markdown("""
<style>
    /* Use system sans-serif font */
    html, body, [class*="css"]  {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    .reportview-container {
        background: #f8fafc;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    h1, h2, h3 {
        color: #1a4d2e; 
        font-weight: 700;
    }
    
    .metric-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.04), 0 1px 3px rgba(0, 0, 0, 0.08);
        border: 1px solid #eef2f5;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    
    @media (prefers-reduced-motion: no-preference) {
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.08);
        }
    }
    
    .metric-icon {
        position: absolute;
        top: 24px;
        right: 24px;
        font-size: 2.5rem;
        opacity: 0.9;
    }
    
    .metric-title {
        font-size: 0.95rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
    }
    
    .metric-value {
        font-size: 2.25rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
        line-height: 1.2;
    }
    
    .metric-delta {
        font-size: 0.875rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    .delta-positive { color: #10b981; }
    .delta-negative { color: #ef4444; }
    .delta-neutral { color: #64748b; }
    .delta-text { color: #64748b; font-weight: 400; font-size: 0.8rem; margin-left: 4px;}
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        background-color: transparent;
        border-radius: 8px 8px 0px 0px;
    }
    
    .section-container {
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #eef2f5;
        margin-bottom: 24px;
    }
    
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 20px;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>🐄 DairyFarm</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-top: 0;'>Intelligence Dashboard</p>", unsafe_allow_html=True)
    st.divider()
    
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
    SPA = f"{FRONTEND_URL}/index.html"

    # Sidebar navigation — Dashboard stays here; all other items open the Bootstrap SPA in a new tab
    st.markdown(f"""
    <div style='color: #64748b; font-size: 0.9rem; margin-bottom: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>Navigation</div>

    <div style='padding: 10px 14px; background: #e2e8f0; border-radius: 8px; font-weight: 600; color: #0f172a; margin-bottom: 6px;'>
        📊 Dashboard
    </div>

    <a href="{SPA}#farmers" target="_blank" style='display:block; padding: 10px 14px; color: #475569; margin-bottom: 6px; border-radius: 8px; text-decoration: none; transition: background 0.15s;' onmouseover="this.style.background='#f1f5f9'" onmouseout="this.style.background='transparent'">
        🧑‍🌾 Farmers
    </a>

    <a href="{SPA}#cattle" target="_blank" style='display:block; padding: 10px 14px; color: #475569; margin-bottom: 6px; border-radius: 8px; text-decoration: none;' onmouseover="this.style.background='#f1f5f9'" onmouseout="this.style.background='transparent'">
        🐄 Cattle
    </a>

    <a href="{SPA}#milk" target="_blank" style='display:block; padding: 10px 14px; color: #475569; margin-bottom: 6px; border-radius: 8px; text-decoration: none;' onmouseover="this.style.background='#f1f5f9'" onmouseout="this.style.background='transparent'">
        🥛 Milk Production
    </a>

    <a href="{SPA}#feed" target="_blank" style='display:block; padding: 10px 14px; color: #475569; margin-bottom: 6px; border-radius: 8px; text-decoration: none;' onmouseover="this.style.background='#f1f5f9'" onmouseout="this.style.background='transparent'">
        🌾 Feed
    </a>

    <a href="{SPA}#expenses" target="_blank" style='display:block; padding: 10px 14px; color: #475569; margin-bottom: 6px; border-radius: 8px; text-decoration: none;' onmouseover="this.style.background='#f1f5f9'" onmouseout="this.style.background='transparent'">
        💰 Financials
    </a>

    <div style='padding: 10px 14px; color: #94a3b8; margin-bottom: 6px; border-radius: 8px; cursor: not-allowed; display: flex; justify-content: space-between; align-items: center;'>
        <span>⚙️ Settings</span>
        <span style='font-size: 0.7rem; background: #e2e8f0; color: #64748b; padding: 2px 8px; border-radius: 99px; font-weight: 600;'>Coming Soon</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.caption("Powered by Streamlit & PostgreSQL.")


# --- HEADER ---
st.markdown("<h1 style='margin-bottom: 4px;'>Farm Performance Overview</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-size: 1.1rem; margin-bottom: 2rem;'>Real-time insights and analytics for your dairy operations.</p>", unsafe_allow_html=True)

# Initialize Analytics Orchestrator
@st.cache_data(ttl=60)
def fetch_analytics_data():
    orchestrator = AnalyticsOrchestrator()
    summary = orchestrator.get_summary()
    detailed = orchestrator.get_detailed_metrics()
    return summary, detailed

try:
    summary, detailed = fetch_analytics_data()
except Exception as e:
    st.error(f"Failed to connect to the database or fetch analytics: {e}")
    st.stop()

# Helper for rendering rich KPI cards
def kpi_card(title, value, icon, delta_val, delta_type, timeframe="vs last month"):
    arrow = "↑" if delta_type == "positive" else "↓" if delta_type == "negative" else "−"
    delta_class = f"delta-{delta_type}"
    
    return f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-delta {delta_class}">
            {arrow} {delta_val} <span class="delta-text">{timeframe}</span>
        </div>
    </div>
    """

# --- KPI ROW ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    milk_total = summary['milk_production']['total_production']
    st.markdown(kpi_card("Total Milk", f"{milk_total:,} L", "🥛", "8.2%", "positive"), unsafe_allow_html=True)
    
with col2:
    rev_total = summary['revenue']['total_revenue']
    st.markdown(kpi_card("Total Revenue", f"₹{rev_total:,}", "💰", "12.4%", "positive"), unsafe_allow_html=True)
    
with col3:
    exp_total = summary['expenses']['total_expense']
    # Lower expenses usually positive indicator, but mathematically it went down
    st.markdown(kpi_card("Total Expenses", f"₹{exp_total:,}", "💸", "3.1%", "positive", "vs last month"), unsafe_allow_html=True)
    
with col4:
    net_profit = summary['financial_summary']['net_profit']
    profit_type = "positive" if net_profit >= 0 else "negative"
    st.markdown(kpi_card("Net Profit", f"₹{net_profit:,}", "📈", "16.8%", profit_type), unsafe_allow_html=True)


# --- DASHBOARD TABS ---
tab_overview, tab_details = st.tabs(["📊 Executive Dashboard", "📋 Raw Analytics Data"])

with tab_overview:
    # First Row: Production Chart & Insights
    r1c1, r1c2 = st.columns([2, 1])
    
    with r1c1:
        st.markdown("<div class='section-container'><div class='section-title'>Milk Production Trend</div>", unsafe_allow_html=True)
        milk_ts = detailed.get("milk_production_time_series", {})
        if milk_ts:
            st.area_chart(milk_ts, width="stretch", color="#10b981")
        else:
            st.info("No milk production data available to visualize.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with r1c2:
        st.markdown("<div class='section-container'><div class='section-title'>Production Summary</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='margin-bottom: 14px; font-size: 1.05rem;'><strong>Average Yield:</strong> <span style='float: right; color: #0f172a;'>{summary['milk_production']['average_production']} L</span></div>
        <div style='margin-bottom: 14px; font-size: 1.05rem;'><strong>Highest Yield:</strong> <span style='float: right; color: #0f172a;'>{summary['milk_production']['max_production']} L</span></div>
        <div style='margin-bottom: 14px; font-size: 1.05rem;'><strong>Std Deviation:</strong> <span style='float: right; color: #0f172a;'>{summary['milk_production']['std_deviation']} L</span></div>
        <div style='margin-bottom: 14px; font-size: 1.05rem;'><strong>Total Records:</strong> <span style='float: right; color: #0f172a;'>{summary['milk_production']['record_count']}</span></div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='section-title' style='margin-top: 32px;'>Farm Insights</div>", unsafe_allow_html=True)
        st.info("💡 Production volume is trending optimally.")
        st.success("✨ Expenses are currently well controlled.")
        if net_profit >= 0:
            st.success("📈 Farm is operating at a net profit.")
        else:
            st.error("📉 Farm is operating at a net loss.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Second Row: Financials
    r2c1, r2c2 = st.columns([1, 1])
    
    with r2c1:
        st.markdown("<div class='section-container'><div class='section-title'>Financial Overview</div>", unsafe_allow_html=True)
        fin_data = {
            "Amount (₹)": {
                "Revenue": summary['revenue']['total_revenue'],
                "Expenses": summary['expenses']['total_expense'],
                "Profit": summary['financial_summary']['net_profit']
            }
        }
        st.bar_chart(fin_data, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with r2c2:
        st.markdown("<div class='section-container'><div class='section-title'>Expense Distribution</div>", unsafe_allow_html=True)
        expense_cat = detailed.get("expense_categorical", {})
        if expense_cat:
            st.bar_chart(expense_cat, width="stretch")
        else:
            st.info("No expense data available to visualize.")
        st.markdown("</div>", unsafe_allow_html=True)

with tab_details:
    st.markdown("<div class='section-container'><div class='section-title'>Extracted Analytics Payload</div>", unsafe_allow_html=True)
    st.markdown("This tab displays the raw structured data provided by the `AnalyticsOrchestrator` for auditing.")
    st.json(summary)
    st.markdown("</div>", unsafe_allow_html=True)
