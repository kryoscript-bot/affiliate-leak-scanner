import streamlit as st
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from urllib.parse import urlparse, urljoin
from collections import Counter
import time

st.set_page_config(
    page_title="Affiliate Leak Protocol Engine Pro v5.0 Ultra",
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
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.04);
        text-align: center;
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
        padding: 18px 20px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .log-card b { color: #111827 !important; }
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
    .fix-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        border: 1px solid #4f46e5;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 14px;
        color: #e0e7ff;
    }
    .fix-card h4 {
        color: #a5b4fc !important;
        margin-top: 0;
        margin-bottom: 10px;
    }
    .logo-container {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 6px;
    }
    .logo-icon {
        font-size: 52px;
        background: linear-gradient(135deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 12px rgba(0, 242, 254, 0.5));
    }
    .tagline {
        color: #94a3b8;
        font-size: 16.5px;
        font-weight: 500;
        margin-top: 3px;
    }
    </style>
""", unsafe_allow_html=True)

# ====================== HEADER ======================
st.markdown("""
<div class="logo-container">
    <div class="logo-icon">⚡</div>
    <div>
        <h1 style="margin:0; padding:0;">Affiliate Leak Protocol Engine Pro</h1>
        <div class="tagline">Detect. Fix. Monetize. — Ultra-Advanced Link Intelligence System v5.0</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("Deep-scan any blog, Linktree, bio page or content hub. Automatically classify affiliate networks, detect dead links, inventory leaks, and generate precise recovery actions + Auto-Fix suggestions.")

target_url = st.text_input(
    "🎯 Enter Target URL (Blog / Linktree / Bio / Landing Page):",
    placeholder="https://yourdomain.com"
)

# ====================== DATA ======================
AFFILIATE_MAP = {
    "amazon.": "Amazon Associates", "amzn.to": "Amazon Associates", "amzn.eu": "Amazon Associates",
    "clickbank": "ClickBank", "hop.clickbank": "ClickBank",
    "shareasale": "ShareASale", "shareasale.com": "ShareASale",
    "cj.com": "CJ Affiliate", "commission-junction": "CJ Affiliate",
    "impact.com": "Impact", "impactradius": "Impact",
    "rakuten": "Rakuten Advertising", "linksynergy": "Rakuten Advertising",
    "rstyle.me": "LTK / RewardStyle", "rewardstyle": "LTK / RewardStyle",
    "skimlinks": "Skimlinks", "go.skimresources": "Skimlinks",
    "viglink": "Sovrn / VigLink", "sovrn": "Sovrn / VigLink",
    "walmart": "Walmart Affiliates", "ebay.": "eBay Partner Network", "ebay.to": "eBay Partner Network",
    "aliexpress": "AliExpress", "awin.": "Awin", "awin1.com": "Awin",
    "bit.ly": "Bitly (Shortener)", "tinyurl.com": "TinyURL", "cutt.ly": "Cuttly",
    "linktr.ee": "Linktree", "bio.link": "Bio.link", "shopmy.us": "ShopMy",
    "hotmart": "Hotmart", "digistore24": "Digistore24", "payhip": "Payhip",
    "gumroad": "Gumroad", "teachable": "Teachable", "kartra": "Kartra"
}

OUT_OF_STOCK_SIGNATURES = [
    "currently unavailable", "out of stock", "temporarily unavailable", "page not found",
    "item unavailable", "sold out", "404", "not available", "product unlisted",
    "this item is no longer available", "product missing", "product unavailable",
    "backorder only", "out of stock online", "we could not find that page",
    "sorry, we couldn't find that page", "this product is no longer available",
    "item not available", "currently not available", "product has been removed"
]

# ====================== CORE FUNCTIONS ======================
def extract_hyperlinks(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=14)
        if response.status_code != 200:
            return None, f"HTTP {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")
        base_url = response.url
        links = set()

        for tag in soup.find_all(["a", "link", "area"], href=True):
            href = tag["href"].strip()
            if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
                continue
            full_url = urljoin(base_url, href)
            if full_url.startswith(("http://", "https://")):
                links.add(full_url.split("#")[0])

        return list(links), None
    except Exception as e:
        return None, str(e)


def analyze_link(link_url):
    start = time.time()
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        resp = requests.get(link_url, headers=headers, timeout=9, allow_redirects=True)
        elapsed = round(time.time() - start, 2)
        final_url = resp.url
        status_code = resp.status_code
        text = resp.text.lower()
        title = ""
        try:
            soup = BeautifulSoup(resp.text, "html.parser")
            if soup.title and soup.title.string:
                title = soup.title.string.lower()
        except:
            pass

        detected = "Standard / Unknown"
        check_str = (link_url + " " + final_url).lower()
        for key, name in AFFILIATE_MAP.items():
            if key in check_str:
                detected = name
                break

        if status_code >= 400:
            return {
                "url": link_url,
                "final_url": final_url,
                "type": "Dead Link",
                "status": f"🔴 Dead (HTTP {status_code})",
                "network": detected,
                "response_time": elapsed,
                "severity": "Critical"
            }

        combined = text + " " + title
        for sig in OUT_OF_STOCK_SIGNATURES:
            if sig in combined:
                return {
                    "url": link_url,
                    "final_url": final_url,
                    "type": "Revenue Leak",
                    "status": "🟡 Out of Stock / Unavailable",
                    "network": detected,
                    "response_time": elapsed,
                    "severity": "High"
                }

        if detected != "Standard / Unknown":
            return {
                "url": link_url,
                "final_url": final_url,
                "type": "Safe Affiliate",
                "status": "🟢 Active & Monetized",
                "network": detected,
                "response_time": elapsed,
                "severity": "Low"
            }

        return {
            "url": link_url,
            "final_url": final_url,
            "type": "Neutral",
            "status": "⚪ Standard Link",
            "network": detected,
            "response_time": elapsed,
            "severity": "Low"
        }

    except Exception:
        return {
            "url": link_url,
            "final_url": link_url,
            "type": "Dead Link",
            "status": "🔴 Timeout / Connection Failed",
            "network": "Unknown",
            "response_time": None,
            "severity": "Critical"
        }


def calculate_advanced_score(results):
    if not results:
        return 0, {}

    total = len(results)
    dead = sum(1 for r in results if r["type"] == "Dead Link")
    leaks = sum(1 for r in results if r["type"] == "Revenue Leak")
    safe = sum(1 for r in results if r["type"] == "Safe Affiliate")
    neutral = sum(1 for r in results if r["type"] == "Neutral")

    score = 100
    score -= dead * 18
    score -= leaks * 11
    score -= neutral * 1.5

    if total > 0:
        safe_ratio = safe / total
        if safe_ratio >= 0.6:
            score += 8
        elif safe_ratio >= 0.4:
            score += 4

    score = max(0, min(100, round(score)))

    breakdown = {
        "dead": dead,
        "leaks": leaks,
        "safe": safe,
        "neutral": neutral,
        "total": total
    }
    return score, breakdown


# ====================== MAIN APP ======================
if st.button("🚀 LAUNCH ULTRA AUDIT ENGINE"):
    if not target_url:
        st.warning("Please enter a valid target URL.")
    else:
        with st.spinner("⚡ Running advanced multi-threaded analysis..."):
            links, error = extract_hyperlinks(target_url)

            if error:
                st.error(f"Failed to fetch page: {error}")
            elif not links:
                st.info("No valid hyperlinks found on this page.")
            else:
                results = []
                with ThreadPoolExecutor(max_workers=30) as executor:
                    future_to_url = {executor.submit(analyze_link, url): url for url in links}
                    for future in as_completed(future_to_url):
                        results.append(future.result())

                dead_list = [r for r in results if r["type"] == "Dead Link"]
                leak_list = [r for r in results if r["type"] == "Revenue Leak"]
                safe_list = [r for r in results if r["type"] == "Safe Affiliate"]
                neutral_list = [r for r in results if r["type"] == "Neutral"]

                score, breakdown = calculate_advanced_score(results)
                networks = Counter([r["network"] for r in results if r["network"] != "Standard / Unknown"])

                # ========== METRICS ==========
                st.markdown("---")
                c1, c2, c3, c4, c5 = st.columns(5)
                with c1:
                    st.markdown(f'<div class="metric-container-box"><h5 style="color:#94a3b8;margin:0;">TOTAL LINKS</h5><h1 style="color:#00f2fe;margin:6px 0 0 0;">{breakdown["total"]}</h1></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="metric-container-box"><h5 style="color:#94a3b8;margin:0;">DEAD LINKS</h5><h1 style="color:#ef4444;margin:6px 0 0 0;">{breakdown["dead"]}</h1></div>', unsafe_allow_html=True)
                with c3:
                    st.markdown(f'<div class="metric-container-box"><h5 style="color:#94a3b8;margin:0;">REVENUE LEAKS</h5><h1 style="color:#f59e0b;margin:6px 0 0 0;">{breakdown["leaks"]}</h1></div>', unsafe_allow_html=True)
                with c4:
                    st.markdown(f'<div class="metric-container-box"><h5 style="color:#94a3b8;margin:0;">SAFE AFFILIATES</h5><h1 style="color:#22c55e;margin:6px 0 0 0;">{breakdown["safe"]}</h1></div>', unsafe_allow_html=True)
                with c5:
                    color = "#22c55e" if score >= 75 else "#f59e0b" if score >= 50 else "#ef4444"
                    st.markdown(f'<div class="metric-container-box"><h5 style="color:#94a3b8;margin:0;">HEALTH SCORE</h5><h1 style="color:{color};margin:6px 0 0 0;">{score}</h1></div>', unsafe_allow_html=True)

                # ========== TABS ==========
                tab1, tab2, tab3, tab4 = st.tabs([
                    f"🚨 Dead Links ({len(dead_list)})",
                    f"💸 Revenue Leaks ({len(leak_list)})",
                    f"🛡️ Safe Affiliates ({len(safe_list)})",
                    f"🌐 All Links ({len(results)})"
                ])

                with tab1:
                    if not dead_list:
                        st.success("No dead links found.")
                    for i, item in enumerate(dead_list, 1):
                        st.markdown(f"""
                        <div class="log-card">
                            <b>#{i} • {item['status']}</b><br><br>
                            <b>Original:</b> {item['url']}<br>
                            <b>Final Destination:</b> {item['final_url']}<br>
                            <b>Network:</b> {item['network']}
                        </div>
                        """, unsafe_allow_html=True)

                with tab2:
                    if not leak_list:
                        st.success("No revenue leaks detected.")
                    for i, item in enumerate(leak_list, 1):
                        st.markdown(f"""
                        <div class="log-card">
                            <b>#{i} • {item['status']}</b><br><br>
                            <b>Original:</b> {item['url']}<br>
                            <b>Final Destination:</b> {item['final_url']}<br>
                            <b>Network:</b> {item['network']}
                        </div>
                        """, unsafe_allow_html=True)

                with tab3:
                    if not safe_list:
                        st.info("No active affiliate campaigns detected.")
                    for i, item in enumerate(safe_list, 1):
                        st.markdown(f"""
                        <div class="log-card">
                            <b>#{i} • {item['status']}</b><br><br>
                            <b>Original:</b> {item['url']}<br>
                            <b>Final Destination:</b> {item['final_url']}<br>
                            <b>Network:</b> {item['network']}
                        </div>
                        """, unsafe_allow_html=True)

                with tab4:
                    for i, item in enumerate(results, 1):
                        st.text(f"[{i}] {item['type']} | {item['network']} → {item['url']}")

                # ========== SMART RECOMMENDATIONS ==========
                st.markdown("---")
                st.markdown("## 🧠 Ultra Smart Recommendations")

                if score >= 80:
                    status, color = "Excellent", "#22c55e"
                elif score >= 60:
                    status, color = "Good", "#3b82f6"
                elif score >= 40:
                    status, color = "Needs Attention", "#f59e0b"
                else:
                    status, color = "Critical", "#ef4444"

                st.markdown(f"""
                <div class="recommend-card">
                    <h4>📊 Advanced Health Score</h4>
                    <h1 style="color:{color}; margin:6px 0;">{score}/100</h1>
                    <p style="margin:0; color:#94a3b8;">Status: <b style="color:{color}">{status}</b></p>
                </div>
                """, unsafe_allow_html=True)

                if dead_list:
                    st.markdown(f"""
                    <div class="recommend-card priority-high">
                        <h4>🚨 Critical: {len(dead_list)} Dead Links Found</h4>
                        <p><b>Action Required:</b></p>
                        <ul>
                            <li>Remove or replace every dead link immediately.</li>
                            <li>Broken links hurt SEO, user trust, and conversion rate.</li>
                            <li>Prioritize high-traffic pages first.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                if leak_list:
                    st.markdown(f"""
                    <div class="recommend-card priority-medium">
                        <h4>💸 High Priority: {len(leak_list)} Revenue Leaks</h4>
                        <p><b>Action Required:</b></p>
                        <ul>
                            <li>These products are out of stock → zero commission.</li>
                            <li>Find alternative products in the same niche and update links.</li>
                            <li>Check Amazon, ClickBank, ShareASale for similar offers.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                if safe_list:
                    st.markdown(f"""
                    <div class="recommend-card priority-low">
                        <h4>🛡️ {len(safe_list)} Healthy Affiliate Campaigns</h4>
                        <p><b>Opportunity:</b></p>
                        <ul>
                            <li>These links are working and monetized.</li>
                            <li>Promote them more (social, email, content upgrades).</li>
                            <li>Create more content around these winning products.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                # ====================== AUTO-FIX SUGGESTIONS ======================
                st.markdown("---")
                st.markdown("## 🔧 Auto-Fix Suggestions")
                st.caption("Intelligent, prioritized actions you can take right now to recover lost commissions.")

                # 1. Dead Links Auto-Fix
                if dead_list:
                    st.markdown(f"""
                    <div class="fix-card">
                        <h4>🚨 Auto-Fix Plan: Dead Links ({len(dead_list)})</h4>
                        <p><b>Priority:</b> Critical &nbsp;|&nbsp; <b>Impact:</b> High (SEO + Trust + Conversions)</p>
                        <p><b>Recommended Actions:</b></p>
                        <ol>
                            <li>Immediately remove all dead links from your content.</li>
                            <li>Replace them with currently working alternative products from the same niche.</li>
                            <li>If no good alternative exists, delete the entire section/paragraph containing the dead link.</li>
                            <li>Update your sitemap and request re-indexing after fixing (for SEO recovery).</li>
                        </ol>
                        <p><b>Quick Search Queries you can use:</b></p>
                        <ul>
                            <li>“best alternative to [product name] 2025”</li>
                            <li>“[product category] best sellers site:amazon.com”</li>
                            <li>“high converting [niche] offers ClickBank”</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                # 2. Revenue Leaks Auto-Fix
                if leak_list:
                    st.markdown(f"""
                    <div class="fix-card">
                        <h4>💸 Auto-Fix Plan: Revenue Leaks / Out of Stock ({len(leak_list)})</h4>
                        <p><b>Priority:</b> High &nbsp;|&nbsp; <b>Impact:</b> Direct Commission Loss</p>
                        <p><b>Recommended Actions:</b></p>
                        <ol>
                            <li>Open each out-of-stock link and note the product category.</li>
                            <li>Search for similar in-stock products on the same network (Amazon, ClickBank, etc.).</li>
                            <li>Replace the old affiliate link with the new working one.</li>
                            <li>Add a small note like “Updated: New Recommended Product” if needed.</li>
                        </ol>
                        <p><b>Best Places to Find Replacements:</b></p>
                        <ul>
                            <li>Amazon Associates → Search same category + sort by Best Sellers / Featured</li>
                            <li>ClickBank Marketplace → Filter by Gravity + Category</li>
                            <li>ShareASale / Impact / Awin → Search similar merchant offers</li>
                            <li>Google: “best [product type] 2025” + your affiliate network name</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                # 3. General Optimization Auto-Fix
                st.markdown(f"""
                <div class="fix-card">
                    <h4>🛠️ General Auto-Optimization Suggestions</h4>
                    <p><b>Do these regularly:</b></p>
                    <ul>
                        <li>Re-run this tool every <b>10–15 days</b> to catch new dead or out-of-stock links early.</li>
                        <li>Keep a backup list of 2–3 alternative products for every main offer you promote.</li>
                        <li>Prefer direct affiliate links instead of multiple shortener redirects when possible.</li>
                        <li>Focus more traffic on your <b>Safe Affiliate</b> links (they are already converting).</li>
                        <li>Download the CSV report and maintain a simple change log (Date → Fixed X links).</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                # Network Summary
                if networks:
                    st.markdown("### 📡 Detected Affiliate Networks")
                    net_text = " • ".join([f"{k} ({v})" for k, v in networks.most_common(8)])
                    st.info(net_text)

                # Download
                st.markdown("---")
                st.subheader("📥 Export Full Report")
                df = pd.DataFrame(results)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download Complete Analysis (CSV)",
                    data=csv,
                    file_name="affiliate_leak_ultra_report.csv",
                    mime="text/csv"
                )