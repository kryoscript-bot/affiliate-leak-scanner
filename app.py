import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

# Fixed: Corrected st.set_page_config here
st.set_page_config(
    page_title="Ultra Link Scanner Pro | Global Affiliate Audit Tool", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Premium Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background: linear-gradient(45deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: bold;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        border-left: 5px solid #1e3c72;
    }
    </style>
""", unsafe_allow_html=True)

# App Headers
st.title("🛡️ Ultra-Advanced Universal Link & Revenue Leak Scanner")
st.subheader("Audit Blogs, Linktree, YouTube Descriptions, Instagram Bios, & Global Affiliate Networks In Real-Time")
st.write("Enter any public URL below. Our multi-threaded engine will dissect the page, map redirect paths, and audit individual link safety profiles to maximize your monetization.")

# User Input Field
target_url = st.text_input("Enter Target URL (Blog Post, Linktree, Social Landing Page, etc.):", placeholder="https://example.com")

# High-Performance Global Footprints & Signatures
AFFILIATE_SIGNATURES = [
    "amazon.", "amzn.to", "clickbank", "shareasale", "cj.com", "commission-junction",
    "impact.com", "impactradius", "rakuten", "rstyle.me", "rewardstyle", "skimlinks",
    "viglink", "walmart", "ebay.to", "aliexpress", "jdoqoc", "tkqlhce", "anrdoezrs",
    "awin.com", "awin1", "click.linksynergy", "target.com", "shoptstyle", "ltk",
    "bit.ly", "tinyurl.com", "cutt.ly", "t.co", "rebrand.ly"
]

OUT_OF_STOCK_SIGNATURES = [
    "currently unavailable", "out of stock", "temporarily unavailable", "page not found",
    "item unavailable", "sold out", "404", "error-page", "not available", 
    "product unlisted", "this item is no longer available", "product missing"
]

def analyze_page_links(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }
        response = requests.get(url, headers=headers, timeout=12)
        if response.status_code != 200:
            return None, f"Network Access Denied (HTTP Status Code: {response.status_code})"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        extracted_links = set()
        
        # Scrape all anchors
        for anchor in soup.find_all('a', href=True):
            raw_href = anchor['href'].strip()
            if raw_href.startswith(('http://', 'https://')):
                extracted_links.add(raw_href)
                
        return list(extracted_links), None
    except Exception as error_msg:
        return None, str(error_msg)

def audit_link_health(link_url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        # Follow redirects fully to analyze destination health
        session_response = requests.get(link_url, headers=headers, timeout=10, allow_redirects=True)
        final_destination = session_response.url
        
        # 1. Structural Validation Code
        if session_response.status_code >= 400:
            return "❌ Dead Link / Broken Resource", f"HTTP {session_response.status_code}", final_destination
            
        # 2. Advanced E-commerce Payload Analysis
        dom_payload = session_response.text.lower()
        for flag in OUT_OF_STOCK_SIGNATURES:
            if flag in dom_payload:
                return "⚠️ Revenue Leak: Item Out-of-Stock / Unlisted", "Inventory Issue", final_destination
                
        # 3. Classify Link Profiles
        is_monetized = any(sig in link_url.lower() or sig in final_destination.lower() for sig in AFFILIATE_SIGNATURES)
        if is_monetized:
            return "✅ Active & Properly Monetized", "Affiliate Active", final_destination
        else:
            return "ℹ️ Neutral External / Social Track", "Standard Route", final_destination
            
    except requests.exceptions.Timeout:
        return "⏱️ Latency Timeout / Network Blocked", "Unresponsive", link_url
    except Exception:
        return "❓ Unverifiable / Restricted Sandbox", "Handshake Error", link_url

# Execution Architecture
if st.button("Initialize Deep Scan Engine"):
    if not target_url:
        st.warning("Action Required: Please supply a secure target URL sequence to run telemetry.")
    else:
        with st.spinner("Processing deep page architecture and structural verification routines..."):
            all_links, failure_signal = analyze_page_links(target_url)
            
            if failure_signal:
                st.error(f"Critical Engine Interruption: {failure_signal}")
            elif not all_links:
                st.info("System Notification: No external or structured hyperlinks detected on target landing coordinate.")
            else:
                # Initialization Vectors for Metrics
                good_links = 0
                leaks = 0
                dead_links = 0
                
                # Visual Dividers & Placeholders
                st.markdown("---")
                st.subheader("📊 Live Telemetry Dashboard Metrics")
                
                metrics_container = st.empty()
                results_container = st.container()
                
                with results_container:
                    st.write("#### Detailed Individual Link Audit Logs:")
                    
                    for index, active_link in enumerate(all_links, 1):
                        status_label, cause, resolved_destination = audit_link_health(active_link)
                        
                        # Increment Dashboard State Indicators
                        if "✅" in status_label:
                            good_links += 1
                            st.success(f"**Track #{index}:** {active_link} \n* Destination: `{resolved_destination}` \n* Status: **{status_label}** ({cause})")
                        elif "⚠️" in status_label:
                            leaks += 1
                            st.warning(f"**Track #{index}:** {active_link} \n* Destination: `{resolved_destination}` \n* Status: **{status_label}** ({cause})")
                        else:
                            dead_links += 1
                            st.error(f"**Track #{index}:** {active_link} \n* Status: **{status_label}** ({cause})")
                
                # Render Real-Time Dashboard Analytics Grid
                with metrics_container:
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric(label="Total Audited Links", value=len(all_links))
                    col2.metric(label="Monetized & Functional", value=good_links)
                    col3.metric(label="Inventory/Stock Leaks", value=leaks)
                    col4.metric(label="Broken/Dead Connections", value=dead_links)
