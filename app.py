import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

# 2026 Production Grade Page Configuration
st.set_page_config(
    page_title="Enterprise Link Telemetry Engine", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-End Cyber Styling & UI Accents
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    div[data-testid="stMetricValue"] { font-size: 38px !important; font-weight: 800 !important; color: #58a6ff !important; }
    .stButton>button {
        background: linear-gradient(135deg, #23a6d5 0%, #23d5ab 100%) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        letter-spacing: 1px;
        border: none !important;
        box-shadow: 0 4px 15px rgba(35, 213, 171, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton>button:hover {
        transform: scale(1.02) translateY(-3px);
        box-shadow: 0 8px 25px rgba(35, 213, 171, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Main Dashboard Interface Headers
st.title("⚡ Enterprise-Grade Link Telemetry & Revenue Leak Scanner")
st.subheader("Deep Multi-Threaded Structural Analysis for Global Networks, Affiliate Endpoints, and Social Bios")
st.write("Fueled by high-performance concurrent processing. This system maps nested redirections and identifies active inventory blocks instantly across international frameworks.")

# User Landing Node Sequence Entry
target_url = st.text_input("Deploy Telemetry Scan Vector (Enter Targeted Domain/Post/Bio URL):", placeholder="https://high-volume-affiliate-portal.com")

# Highly Updated Digital Signatures & Triggers
AFFILIATE_SIGNATURES = [
    "amazon.", "amzn.to", "clickbank", "shareasale", "cj.com", "commission-junction",
    "impact.com", "impactradius", "rakuten", "rstyle.me", "rewardstyle", "skimlinks",
    "viglink", "walmart", "ebay.to", "aliexpress", "jdoqoc", "tkqlhce", "anrdoezrs",
    "awin.com", "awin1", "click.linksynergy", "target.com", "shoptstyle", "ltk",
    "bit.ly", "tinyurl.com", "cutt.ly", "t.co", "rebrand.ly", "linktr.ee", "bio.link",
    "shopmy.us", "knoji", "hotmart", "digistore24", "partnerstack", "refersion"
]

OUT_OF_STOCK_SIGNATURES = [
    "currently unavailable", "out of stock", "temporarily unavailable", "page not found",
    "item unavailable", "sold out", "404", "error-page", "not available", "404 not found",
    "product unlisted", "this item is no longer available", "product missing", "product unavailable",
    "oops!", "sorry, the page you requested", "product no longer exists", "stock empty"
]

def extract_hyperlinks_async(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        }
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return None, f"Network Access Blocked (HTTP Refusal Code: {response.status_code})"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        discovered_nodes = set()
        
        # Standard and Advanced Script-Level Fallback Extraction
        for element in soup.find_all(['a', 'link', 'area'], href=True):
            cleaned_node = element['href'].strip()
            if cleaned_node.startswith(('http://', 'https://')):
                discovered_nodes.add(cleaned_node)
                
        # Data-attribute deep parsing logic for reactive UI networks
        for custom_element in soup.find_all(attrs={"data-href": True}):
            cleaned_node = custom_element['data-href'].strip()
            if cleaned_node.startswith(('http://', 'https://')):
                discovered_nodes.add(cleaned_node)
                
        return list(discovered_nodes), None
    except Exception as network_fault:
        return None, str(network_fault)

def trace_single_endpoint_health(link_url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        # Threaded validation mapping with automatic system loop tracking
        session_instance = requests.get(link_url, headers=headers, timeout=8, allow_redirects=True)
        final_destination_route = session_instance.url
        
        if session_instance.status_code >= 400:
            return {"url": link_url, "status": "❌ Broken Connection", "cause": f"HTTP {session_instance.status_code}", "destination": final_destination_route}
            
        page_payload = session_instance.text.lower()
        for stock_flag in OUT_OF_STOCK_SIGNATURES:
            if stock_flag in page_payload:
                return {"url": link_url, "status": "⚠️ Monetization Leak", "cause": "Inventory Out-of-Stock", "destination": final_destination_route}
                
        monetization_vector = any(sig in link_url.lower() or sig in final_destination_route.lower() for sig in AFFILIATE_SIGNATURES)
        if monetization_vector:
            return {"url": link_url, "status": "✅ Optimized Affiliate", "cause": "Monetized Route Operational", "destination": final_destination_route}
        else:
            return {"url": link_url, "status": "ℹ️ Standard Traversal", "cause": "Clean Unmonetized Path", "destination": final_destination_route}
            
    except requests.exceptions.Timeout:
        return {"url": link_url, "status": "⏱️ Latency Breach", "cause": "Timeout (>8s)", "destination": link_url}
    except Exception:
        return {"url": link_url, "status": "❓ Shielded Ecosystem", "cause": "Restricted Access Path", "destination": link_url}

# Parallel Processing Concurrency Management Matrix
if st.button("Trigger High-Velocity Diagnostic Optimization"):
    if not target_url:
        st.warning("Action Deferred: Paste an endpoint coordinate to spin up background parallel execution threads.")
    else:
        with st.spinner("Spawning synchronous multi-threaded worker pools... Processing asset tree structure."):
            extracted_node_list, critical_signal = extract_hyperlinks_async(target_url)
            
            if critical_signal:
                st.error(f"Execution Interrupted: {critical_signal}")
            elif not extracted_node_list:
                st.info("Telemetry Empty: Zero active hypermedia tags extracted from the source DOM payload.")
            else:
                # Concurrent Thread Distribution Pipeline (Max 25 Workers in Parallel)
                with ThreadPoolExecutor(max_workers=25) as execution_pool:
                    telemetry_outputs = list(execution_pool.map(trace_single_endpoint_health, extracted_node_list))
                
                # Metric Processing & Analysis Mapping
                total_audited = len(telemetry_outputs)
                functional_nodes = sum(1 for item in telemetry_outputs if "✅" in item["status"])
                leak_nodes = sum(1 for item in telemetry_outputs if "⚠️" in item["status"])
                broken_nodes = sum(1 for item in telemetry_outputs if "❌" in item["status"] or "⏱️" in item["status"])
                
                st.markdown("---")
                st.subheader("📊 Network Performance Diagnostic Dashboard")
                
                # Visual Metric Grid Generation
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Hyperlinks Mapped", total_audited)
                col2.metric("Active Campaigns", functional_nodes)
                col3.metric("Identified Revenue Leaks", leak_nodes)
                col4.metric("Dead Drop Elements", broken_nodes)
                
                st.markdown("### 📋 Structured Performance Manifest Log")
                
                # Structured Layout Presentation
                for track_idx, log in enumerate(telemetry_outputs, 1):
                    if "✅" in log["status"]:
                        st.success(f"**[{track_idx}] {log['status']}** \n* Source Vector: {log['url']} \n* Verified Target: `{log['destination']}` \n* Diagnostic Flag: {log['cause']}")
                    elif "⚠️" in log["status"]:
                        st.warning(f"**[{track_idx}] {log['status']}** \n* Source Vector: {log['url']} \n* Verified Target: `{log['destination']}` \n* Diagnostic Flag: {log['cause']}")
                    else:
                        st.error(f"**[{track_idx}] {log['status']}** \n* Source Vector: {log['url']} \n* Diagnostic Flag: {log['cause']}")
                
                # Premium Data Operational Feature: Direct Export Engine
                st.markdown("---")
                st.subheader("📥 Export Enterprise Telemetry Package")
                data_frame_manifest = pd.DataFrame(telemetry_outputs)
                csv_payload = data_frame_manifest.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="Download Full Link Intelligence Sheet (.CSV)",
                    data=csv_payload,
                    file_name="link_telemetry_audit_report.csv",
                    mime="text/csv"
                )
