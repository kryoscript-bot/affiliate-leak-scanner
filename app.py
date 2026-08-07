import streamlit as st
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

st.set_page_config(
    page_title="Affiliate Leak Protocol Engine Pro v4.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .main { background-color: #0b0f19 !important; color: #cbd5e1 !important; font-family: 'Inter', sans-serif; }
    h1 { color: #00f2fe !important; font-weight: 800 !important; letter-spacing: -1.5px; text-shadow: 0 0 15px rgba(0,242,254,0.25); margin-bottom: 5px; }
    h3 { color: #ffffff !important; font-weight: 700 !important; }
    .metric-container-box {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        padding: 26px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.04);
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 15px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #0b0f19 !important;
        border-radius: 12px !important;
        padding: 16px 36px !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(0, 242, 254, 0.35);
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 30px rgba(0, 242, 254, 0.6);
    }
    .log-card {
        background-color: #ffffff !important;
        color: #1f2937 !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .log-card b {
        color: #111827 !important;
    }
    .recommend-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 16px;
        color: #e2e8f0;
    }
    .recommend-card h4 {
        color: #38bdf8 !important;
        margin-top: 0;
        margin-bottom: 12px;
    }
    .priority-high { border-left: 5px solid #ef4444; }
    .priority-medium { border-left: 5px solid #f59e0b; }
    .priority-low { border-left: 5px solid #22c55e; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚡ Affiliate Leak Protocol Engine Pro</h1>", unsafe_allow_html=True)
st.subheader("Global Enterprise Command Center — Next-Gen Multi-Threaded Structural Telemetry")
st.write("Scan deep directories, landing grids, and dynamic link clouds. This system automatically classifies global affiliate networks, parses response parameters, and isolates active inventory leak vectors.")

target_url = st.text_input(
    "🎯 Enter Targeted Asset URL Vector (Blog Link, Linktree Page, Social Bio Endpoint):",
    placeholder="https://yourdomain.com"
)

AFFILIATE_MAP = {
    "amazon": "Amazon Associates Cluster", "amzn.to": "Amazon Associates Cluster",
    "clickbank": "ClickBank Affiliate Network", "shareasale": "ShareASale System Hub",
    "cj.com": "CJ Affiliate Enterprise", "commission-junction": "CJ Affiliate Enterprise",
    "impact.com": "Impact Radius Network node", "impactradius": "Impact Radius Network node",
    "rakuten": "Rakuten LinkSynergy System", "rstyle.me": "LTK / RewardStyle Tracker",
    "rewardstyle": "LTK / RewardStyle Tracker", "skimlinks": "Skimlinks Automated Routing",
    "viglink": "VigLink / Sovrn Monetization Layer", "walmart": "Walmart Commerce Network",
    "ebay.to": "eBay Partner Network (EPN)", "aliexpress": "AliExpress Portal Hub",
    "awin.com": "Awin Global Framework", "awin1": "Awin Global Framework",
    "bit.ly": "Bitly Short URL Wrapper", "tinyurl.com": "TinyURL Proxy Node",
    "cutt.ly": "Cuttly Tracking System", "linktr.ee": "Linktree Matrix Profile",
    "bio.link": "Bio.Link Aggregator Node", "shopmy.us": "ShopMy Creator Grid",
    "hotmart": "Hotmart Platform Distribution", "digistore24": "Digistore24 Revenue Cloud"
}

OUT_OF_STOCK_SIGNATURES = [
    "currently unavailable", "out of stock", "temporarily unavailable", "page not found",
    "item unavailable", "sold out", "404", "error-page", "not available", "404 not found",
    "product unlisted", "this item is no longer available", "product missing", "product unavailable",
    "backorder only", "out of stock online", "temporarily dead node", "product non-existent"
]


def extract_hyperlinks_async(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return None, f"Source Execution Interrupted (HTTP Refusal Trigger: {response.status_code})"

        soup = BeautifulSoup(response.text, 'html.parser')
        discovered_nodes = set()

        for element in soup.find_all(['a', 'link'], href=True):
            cleaned_node = element['href'].strip()
            if cleaned_node.startswith(('http://', 'https://')):
                discovered_nodes.add(cleaned_node)

        return list(discovered_nodes), None
    except Exception as err:
        return None, str(err)


def trace_single_endpoint_health(link_url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        session_instance = requests.get(link_url, headers=headers, timeout=8, allow_redirects=True)
        final_destination_route = session_instance.url

        detected_network = "Standard External Endpoint Node"
        for keyword, label in AFFILIATE_MAP.items():
            if keyword in link_url.lower() or keyword in final_destination_route.lower():
                detected_network = label
                break

        if session_instance.status_code >= 400:
            return {
                "url": link_url,
                "type": "Dead Link",
                "status": f"🔴 Broken Path Framework (HTTP {session_instance.status_code})",
                "network": detected_network,
                "destination": final_destination_route
            }

        dom_payload = session_instance.text.lower()
        for stock_flag in OUT_OF_STOCK_SIGNATURES:
            if stock_flag in dom_payload:
                return {
                    "url": link_url,
                    "type": "Revenue Leak",
                    "status": "🟡 Critical Revenue Leak: Inventory Empty",
                    "network": detected_network,
                    "destination": final_destination_route
                }

        if detected_network != "Standard External Endpoint Node":
            return {
                "url": link_url,
                "type": "Safe Affiliate",
                "status": "🟢 Campaign Verified Active & Monetized",
                "network": detected_network,
                "destination": final_destination_route
            }
        else:
            return {
                "url": link_url,
                "type": "Neutral Route",
                "status": "Standard Structural Route Path",
                "network": detected_network,
                "destination": final_destination_route
            }

    except Exception:
        return {
            "url": link_url,
            "type": "Dead Link",
            "status": "🔴 Telemetry Timeout / Network Resolution Defect",
            "network": "Unknown Network Sector",
            "destination": link_url
        }


if st.button("LAUNCH HIGH-VELOCITY AUDIT ENGINE SEQUENCE"):
    if not target_url:
        st.warning("Action Deferred: Please input an operational target URL sequence.")
    else:
        with st.spinner("⚡ Spawning multi-threaded workers... Running parallel security analytics loops."):
            extracted_nodes, failure_signal = extract_hyperlinks_async(target_url)

            if failure_signal:
                st.error(f"Critical Engine Halt: {failure_signal}")
            elif not extracted_nodes:
                st.info("Scan Terminal: Zero hyperlinks discovered inside target document payload.")
            else:
                with ThreadPoolExecutor(max_workers=25) as execution_pool:
                    telemetry_outputs = list(execution_pool.map(trace_single_endpoint_health, extracted_nodes))

                dead_links_list = [item for item in telemetry_outputs if item["type"] == "Dead Link"]
                revenue_leaks_list = [item for item in telemetry_outputs if item["type"] == "Revenue Leak"]
                safe_affiliate_list = [item for item in telemetry_outputs if item["type"] == "Safe Affiliate"]
                neutral_list = [item for item in telemetry_outputs if item["type"] == "Neutral Route"]

                total = len(telemetry_outputs)
                dead_count = len(dead_links_list)
                leak_count = len(revenue_leaks_list)
                safe_count = len(safe_affiliate_list)

                # Health Score Calculation
                if total > 0:
                    health_score = max(0, 100 - (dead_count * 15 + leak_count * 10))
                else:
                    health_score = 0

                st.markdown("---")

                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                with m_col1:
                    st.markdown(f'''
                        <div class="metric-container-box">
                            <h5 style="color:#94a3b8;margin:0;">TOTAL SCANNED</h5>
                            <h1 style="color:#00f2fe !important;margin:5px 0 0 0;">{total}</h1>
                        </div>
                    ''', unsafe_allow_html=True)
                with m_col2:
                    st.markdown(f'''
                        <div class="metric-container-box">
                            <h5 style="color:#94a3b8;margin:0;">🚨 DEAD LINKS</h5>
                            <h1 style="color:#ff4b4b !important;margin:5px 0 0 0;">{dead_count}</h1>
                        </div>
                    ''', unsafe_allow_html=True)
                with m_col3:
                    st.markdown(f'''
                        <div class="metric-container-box">
                            <h5 style="color:#94a3b8;margin:0;">💸 REVENUE LEAKS</h5>
                            <h1 style="color:#ffaa00 !important;margin:5px 0 0 0;">{leak_count}</h1>
                        </div>
                    ''', unsafe_allow_html=True)
                with m_col4:
                    st.markdown(f'''
                        <div class="metric-container-box">
                            <h5 style="color:#94a3b8;margin:0;">🛡️ SAFE CAMPAIGNS</h5>
                            <h1 style="color:#00cc66 !important;margin:5px 0 0 0;">{safe_count}</h1>
                        </div>
                    ''', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                tab1, tab2, tab3, tab4 = st.tabs([
                    f"🚨 Dead Links Network ({dead_count})",
                    f"💸 Revenue Leakage Core ({leak_count})",
                    f"🛡️ Active Campaigns Hub ({safe_count})",
                    f"🌐 General Structural Map ({len(neutral_list)})"
                ])

                with tab1:
                    st.write("### 🚨 Broken Communication Channels Isolated:")
                    if not dead_links_list:
                        st.success("Target Workspace Verified: Zero broken links flagged on this sector.")
                    else:
                        for idx, item in enumerate(dead_links_list, 1):
                            st.markdown(f"""
                            <div class="log-card">
                                <b>Node Index #{idx}</b><br><br>
                                <b>Originating Link Vector:</b><br>
                                {item['url']}<br><br>
                                <b>System Flag Status:</b> {item['status']}<br><br>
                                <b>Target Segment Identity:</b> {item['network']}
                            </div>
                            """, unsafe_allow_html=True)

                with tab2:
                    st.write("### 💸 Revenue Outflow Hazards Detected (Merchant Inventory Stock-Outs):")
                    if not revenue_leaks_list:
                        st.success("Target Verification Clear: Zero merchant inventory leaks active.")
                    else:
                        for idx, item in enumerate(revenue_leaks_list, 1):
                            st.markdown(f"""
                            <div class="log-card">
                                <b>Leak Event #{idx}</b><br><br>
                                <b>Campaign Component:</b><br>
                                {item['url']}<br><br>
                                <b>Resolved Merchant Landing:</b><br>
                                {item['destination']}<br><br>
                                <b>Telemetry Diagnostic:</b> {item['status']}<br><br>
                                <b>Identified Asset Framework:</b> {item['network']}
                            </div>
                            """, unsafe_allow_html=True)

                with tab3:
                    st.write("### 🛡️ Verified Operating Affiliate Infrastructure Channels:")
                    if not safe_affiliate_list:
                        st.info("Workspace Alert: Zero active high-tier networks identified inside source tree.")
                    else:
                        for idx, item in enumerate(safe_affiliate_list, 1):
                            st.markdown(f"""
                            <div class="log-card">
                                <b>Active Stream #{idx}</b><br><br>
                                <b>Source Tracking Vector:</b><br>
                                {item['url']}<br><br>
                                <b>Final Target Resolution:</b><br>
                                {item['destination']}<br><br>
                                <b>Classified System Network:</b> {item['network']}
                            </div>
                            """, unsafe_allow_html=True)

                with tab4:
                    st.write("### 🌐 Standard Infrastructure Links Map:")
                    if not neutral_list:
                        st.info("Workspace Notification: Zero neutral external link traces found.")
                    else:
                        for idx, item in enumerate(neutral_list, 1):
                            st.text(f"[{idx}] Endpoint Trace Path: {item['url']}")

                # ====================== SMART RECOMMENDATIONS SECTION ======================
                st.markdown("---")
                st.markdown("## 🧠 Smart Action Recommendations")
                st.caption("Based on your scan results, here is exactly what you should do next.")

                # Health Score Display
                if health_score >= 80:
                    score_color = "#22c55e"
                    score_status = "Excellent"
                elif health_score >= 50:
                    score_color = "#f59e0b"
                    score_status = "Needs Attention"
                else:
                    score_color = "#ef4444"
                    score_status = "Critical"

                st.markdown(f"""
                <div class="recommend-card">
                    <h4>📊 Overall Link Health Score</h4>
                    <h1 style="color:{score_color}; margin:8px 0;">{health_score}/100</h1>
                    <p style="margin:0; color:#94a3b8;">Status: <b style="color:{score_color};">{score_status}</b></p>
                </div>
                """, unsafe_allow_html=True)

                # Priority Actions
                if dead_count > 0:
                    st.markdown(f"""
                    <div class="recommend-card priority-high">
                        <h4>🚨 High Priority: Fix Dead Links ({dead_count})</h4>
                        <p><b>What to do:</b></p>
                        <ul>
                            <li>Turant in dead links ko remove ya replace karo. Broken links se user trust aur SEO dono kharab hote hain.</li>
                            <li>Har dead link ko check karke similar working product/link se replace karo.</li>
                            <li>Agar koi product permanently unavailable hai to us section ko completely hata do.</li>
                        </ul>
                        <p><b>How to do:</b> Dead Links Network tab se links copy karke apne content mein jaake replace karo.</p>
                    </div>
                    """, unsafe_allow_html=True)

                if leak_count > 0:
                    st.markdown(f"""
                    <div class="recommend-card priority-medium">
                        <h4>💸 Medium Priority: Fix Revenue Leaks ({leak_count})</h4>
                        <p><b>What to do:</b></p>
                        <ul>
                            <li>Out of stock products se commission nahi milta. In links ko turant update karo.</li>
                            <li>Same category ke alternative products dhoondo jo currently available hain.</li>
                            <li>Amazon/Clickbank etc. mein similar high converting products search karke replace karo.</li>
                        </ul>
                        <p><b>How to do:</b> Revenue Leakage Core tab se destination links dekho aur naya product link lagao.</p>
                    </div>
                    """, unsafe_allow_html=True)

                if safe_count > 0:
                    st.markdown(f"""
                    <div class="recommend-card priority-low">
                        <h4>🛡️ Good News: {safe_count} Active Campaigns Working</h4>
                        <p><b>What to do:</b></p>
                        <ul>
                            <li>In working affiliate links ko promote karo (social media, email, more content).</li>
                            <li>Inhi successful products ke around more content banao.</li>
                            <li>In links ko apne best performing pages pe highlight karo.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                if dead_count == 0 and leak_count == 0:
                    st.markdown("""
                    <div class="recommend-card priority-low">
                        <h4>🎉 Excellent Condition!</h4>
                        <p>Aapke saare links healthy hain. Ab aap scale kar sakte ho:</p>
                        <ul>
                            <li>More content publish karo similar niche mein.</li>
                            <li>In working links ko different platforms pe promote karo.</li>
                            <li>New high-commission products add karna shuru karo.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                # Extra Tips
                st.markdown("""
                <div class="recommend-card">
                    <h4>💡 Pro Tips for Better Results</h4>
                    <ul>
                        <li>Har 15-20 din baad yeh tool se scan karte raho taaki links fresh rahein.</li>
                        <li>Dead links se better hai kam links rakhna, lekin saare working hone chahiye.</li>
                        <li>Amazon links ke liye Amazon Associates se latest product links use karo.</li>
                        <li>Linktree / Bio pages mein zyada se zyada working affiliate links rakho.</li>
                        <li>CSV download karke Excel mein analysis kar sakte ho future ke liye.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                # Download Section
                st.markdown("---")
                st.subheader("📥 Export Complete Network Matrix Package")
                df = pd.DataFrame(telemetry_outputs)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Full Link Telemetry Sheet (.CSV)",
                    data=csv,
                    file_name="complete_link_telemetry_audit.csv",
                    mime="text/csv"
                )