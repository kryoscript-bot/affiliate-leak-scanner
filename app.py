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

                st.markdown("---")

                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                with m_col1:
                    st.markdown(f'''
                        <div class="metric-container-box">
                            <h5 style="color:#94a3b8;margin:0;">TOTAL SCANNED</h5>
                            <h1 style="color:#00f2fe !important;margin:5px 0 0 0;">{len(telemetry_outputs)}</h1>
                        </div>
                    ''', unsafe_allow_html=True)
                with m_col2:
                    st.markdown(f'''
                        <div class="metric-container-box">
                            <h5 style="color:#94a3b8;margin:0;">🚨 DEAD LINKS</h5>
                            <h1 style="color:#ff4b4b !important;margin:5px 0 0 0;">{len(dead_links_list)}</h1>
                        </div>
                    ''', unsafe_allow_html=True)
                with m_col3:
                    st.markdown(f'''
                        <div class="metric-container-box">
                            <h5 style="color:#94a3b8;margin:0;">💸 REVENUE LEAKS</h5>
                            <h1 style="color:#ffaa00 !important;margin:5px 0 0 0;">{len(revenue_leaks_list)}</h1>
                        </div>
                    ''', unsafe_allow_html=True)
                with m_col4:
                    st.markdown(f'''
                        <div class="metric-container-box">
                            <h5 style="color:#94a3b8;margin:0;">🛡️ SAFE CAMPAIGNS</h5>
                            <h1 style="color:#00cc66 !important;margin:5px 0 0 0;">{len(safe_affiliate_list)}</h1>
                        </div>
                    ''', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                tab1, tab2, tab3, tab4 = st.tabs([
                    f"🚨 Dead Links Network ({len(dead_links_list)})",
                    f"💸 Revenue Leakage Core ({len(revenue_leaks_list)})",
                    f"🛡️ Active Campaigns Hub ({len(safe_affiliate_list)})",
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