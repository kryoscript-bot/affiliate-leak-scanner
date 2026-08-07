import streamlit as st
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

# Page setup
st.set_page_config(page_title="Affiliate Scanner Pro", layout="wide")

# UI Headers
st.markdown("<h1>⚡ Affiliate Leak Protocol Engine Pro</h1>", unsafe_allow_html=True)
st.subheader("Global Enterprise Command Center — Next-Gen Multi-Threaded Structural Telemetry")
st.write("Scan deep directories, landing grids, and dynamic link clouds. This system automatically classifies global affiliate networks, parses response parameters, and isolates active inventory leak vectors.")

# Target URL Input
target_url = st.text_input("🎯 Enter Targeted Asset URL Vector:", placeholder="https://yourdomain.com")

# Network Mapping Data
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
    "product unlisted", "this item is no longer available", "product missing", "product unavailable"
]

def extract_hyperlinks_async(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
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
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        session_instance = requests.get(link_url, headers=headers, timeout=8, allow_redirects=True)
        final_destination_route = session_instance.url
        detected_network = "Standard External Endpoint Node"
        for keyword, label in AFFILIATE_MAP.items():
            if keyword in link_url.lower() or keyword in final_destination_route.lower():
                detected_network = label
                break
        if session_instance.status_code >= 400:
            return {"url": link_url, "type": "Dead Link", "status": f"🔴 Broken Path Framework (HTTP {session_instance.status_code})", "network": detected_network, "destination": final_destination_route}
        dom_payload = session_instance.text.lower()
        for stock_flag in OUT_OF_STOCK_SIGNATURES:
            if stock_flag in dom_payload:
                return {"url": link_url, "type": "Revenue Leak", "status": "🟡 Critical Revenue Leak: Inventory Empty", "network": detected_network, "destination": final_destination_route}
        if detected_network != "Standard External Endpoint Node":
            return {"url": link_url, "type": "Safe Affiliate", "status": "🟢 Campaign Verified Active & Monetized", "network": detected_network, "destination": final_destination_route}
        else:
            return {"url": link_url, "type": "Neutral Route", "status": "Standard Structural Route Path", "network": detected_network, "destination": final_destination_route}
    except Exception:
        return {"url": link_url, "type": "Dead Link", "status": "🔴 Telemetry Timeout / Network Resolution Defect", "network": "Unknown Network Sector", "destination": link_url}

# Run Engine Logic
if st.button("LAUNCH HIGH-VELOCITY AUDIT ENGINE SEQUENCE"):
    if not target_url:
        st.warning("Action Deferred: Please input an operational target URL sequence.")
    else:
        with st.spinner("⚡ Running parallel security analytics loops..."):
            extracted_nodes, failure_signal = extract_hyperlinks_async(target_url)
            if failure_signal:
                st.error(f"Critical Engine Halt: {failure_signal}")
            elif not extracted_nodes:
                st.info("Scan Terminal: Zero hyperlinks discovered.")
            else:
                with ThreadPoolExecutor(max_workers=25) as execution_pool:
                    telemetry_outputs = list(execution_pool.map(trace_single_endpoint_health, extracted_nodes))
                
                dead_links_list = [item for item in telemetry_outputs if item["type"] == "Dead Link"]
                revenue_leaks_list = [item for item in telemetry_outputs if item["type"] == "Revenue Leak"]
                safe_affiliate_list = [item for item in telemetry_outputs if item["type"] == "Safe Affiliate"]
                neutral_list = [item for item in telemetry_outputs if item["type"] == "Neutral Route"]
                
                st.markdown("---")
                
                # Metrics Display
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("TOTAL SCANNED", len(telemetry_outputs))
                col2.metric("DEAD LINKS 🔴", len(dead_links_list))
                col3.metric("REVENUE LEAKS 🟡", len(revenue_leaks_list))
                col4.metric("SAFE CAMPAIGNS 🟢", len(safe_affiliate_list))
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Tabs Layout with Flat Strings
                tab1, tab2, tab3, tab4 = st.tabs(["🔴 Dead Links", "🟡 Revenue Leaks", "🟢 Active Campaigns", "🌐 General Map"])
                
                with tab1:
                    st.write("### 🚨 Broken Communication Channels Isolated:")
                    if not dead_links_list:
                        st.success("Zero broken links flagged on this sector.")
                    for idx, item in enumerate(dead_links_list, 1):
                        st.write(f"**Index #{idx}** | **Link:** {item['url']} | **Status:** {item['status']} | **Network:** {item['network']}")
                        
                with tab2:
                    st.write("### 💸 Revenue Outflow Hazards Detected (Out-of-Stock):")
                    if not revenue_leaks_list:
                        st.success("Zero merchant inventory leaks active.")
                    for idx, item in enumerate(revenue_leaks_list, 1):
                        st.write(f"**Leak #{idx}** | **Link:** {item['url']} | **Network:** {item['network']} | **Status:** {item['status']}")
                        
                with tab3:
                    st.write("### 🛡️ Verified Operating Affiliate Channels:")
                    if not safe_affiliate_list:
                        st.info("Zero active affiliate networks identified.")
                    for idx, item in enumerate(safe_affiliate_list, 1):
                        st.write(f"**Campaign #{idx}** | **Link:** {item['url']} | **Platform:** {item['network']} | **Target:** {item['destination']}")
                        
                with tab4:
                    st.write("### 🌐 Standard Infrastructure Links Map:")
                    if not neutral_list:
                        st.info("Zero neutral external link traces found.")
                    for idx, item in enumerate(neutral_list, 1):
                        st.text(f"[{idx}] Endpoint Trace Path: {item['url']}")
                        
                st.markdown("---")
                df = pd.DataFrame(telemetry_outputs)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(label="Download Full Link Telemetry Sheet (.CSV)", data=csv, file_name="complete_link_telemetry_audit.csv", mime="text/csv")
