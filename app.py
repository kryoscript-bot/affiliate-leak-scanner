import streamlit as st
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from urllib.parse import urlparse, urljoin
from collections import Counter
import time
import re
import json

st.set_page_config(
    page_title="Affiliate Leak Protocol Engine Pro v5.3",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .main { background-color: #0b0f19 !important; color: #cbd5e1 !important; font-family: 'Inter', sans-serif; }
    h1 { color: #00f2fe !important; font-weight: 800 !important; letter-spacing: -1.5px; text-shadow: 0 0 15px rgba(0,242,254,0.25); margin-bottom: 5px; }
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
    .recommend-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 16px;
        color: #e2e8f0;
    }
    .recommend-card h4 { color: #38bdf8 !important; margin-top: 0; margin-bottom: 12px; }
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
    .fix-card h4 { color: #a5b4fc !important; margin-top: 0; margin-bottom: 10px; }
    .no-affiliate-box {
        background: linear-gradient(135deg, #450a0a 0%, #7f1d1d 100%);
        border: 1px solid #ef4444;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        color: #fecaca;
        text-align: center;
    }
    .logo-container { display: flex; align-items: center; gap: 16px; margin-bottom: 6px; }
    .logo-icon {
        font-size: 52px;
        background: linear-gradient(135deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 12px rgba(0, 242, 254, 0.5));
    }
    .tagline { color: #94a3b8; font-size: 16.5px; font-weight: 500; margin-top: 3px; }
    .platform-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 18px 0 10px 0;
        opacity: 0.75;
    }
    .platform-badge {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #94a3b8;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        backdrop-filter: blur(6px);
    }
    .identity-badge {
        display: inline-block;
        background: #e0f2fe;
        color: #0369a1;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin-top: 6px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="logo-container">
    <div class="logo-icon">⚡</div>
    <div>
        <h1 style="margin:0; padding:0;">Affiliate Leak Protocol Engine Pro</h1>
        <div class="tagline">Detect. Fix. Monetize. — Ultra-Advanced Link Intelligence System v5.3</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("Deep-scan blogs, Linktree, bio pages, YouTube, TikTok, Twitter/X and more. Automatically detect platform + username/ID of every link.")

st.markdown("""
<div class="platform-bar">
    <div class="platform-badge">YouTube</div>
    <div class="platform-badge">TikTok</div>
    <div class="platform-badge">Twitter / X</div>
    <div class="platform-badge">Instagram</div>
    <div class="platform-badge">Facebook</div>
    <div class="platform-badge">Linktree</div>
    <div class="platform-badge">Amazon</div>
    <div class="platform-badge">ClickBank</div>
    <div class="platform-badge">ShareASale</div>
    <div class="platform-badge">Impact</div>
    <div class="platform-badge">Awin</div>
</div>
""", unsafe_allow_html=True)

target_url = st.text_input(
    "🎯 Enter Target URL (Blog / Linktree / Bio / YouTube / TikTok / Twitter etc.):",
    placeholder="https://yourdomain.com or https://youtu.be/xxxxx or https://www.tiktok.com/@user"
)

AFFILIATE_MAP = {
    "amazon.": "Amazon Associates", "amzn.to": "Amazon Associates", "amzn.eu": "Amazon Associates",
    "clickbank": "ClickBank", "hop.clickbank": "ClickBank",
    "shareasale": "ShareASale",
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

def extract_platform_identity(url: str) -> dict:
    """Extract platform and username/ID from URL"""
    url_lower = url.lower()
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    parts = path.split("/") if path else []

    # YouTube
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        if "/@" in url_lower:
            username = url_lower.split("/@")[1].split("/")[0].split("?")[0]
            return {"platform": "YouTube", "username": f"@{username}", "display": f"YouTube • @{username}"}
        if "/channel/" in url_lower:
            channel_id = url_lower.split("/channel/")[1].split("/")[0].split("?")[0]
            return {"platform": "YouTube", "username": channel_id, "display": f"YouTube • {channel_id}"}
        if "/c/" in url_lower or "/user/" in url_lower:
            username = parts[1] if len(parts) > 1 else "Unknown"
            return {"platform": "YouTube", "username": f"@{username}", "display": f"YouTube • @{username}"}
        return {"platform": "YouTube", "username": "Unknown", "display": "YouTube"}

    # TikTok
    if "tiktok.com" in url_lower:
        if "/@" in url_lower:
            username = url_lower.split("/@")[1].split("/")[0].split("?")[0]
            return {"platform": "TikTok", "username": f"@{username}", "display": f"TikTok • @{username}"}
        return {"platform": "TikTok", "username": "Unknown", "display": "TikTok"}

    # Twitter / X
    if "twitter.com" in url_lower or "x.com" in url_lower or "t.co" in url_lower:
        if len(parts) >= 1 and parts[0] not in ["i", "intent", "share", "home"]:
            username = parts[0].split("?")[0]
            if username:
                return {"platform": "Twitter / X", "username": f"@{username}", "display": f"Twitter/X • @{username}"}
        return {"platform": "Twitter / X", "username": "Unknown", "display": "Twitter / X"}

    # Instagram
    if "instagram.com" in url_lower:
        if len(parts) >= 1 and parts[0] not in ["p", "reel", "stories", "explore"]:
            username = parts[0].split("?")[0]
            return {"platform": "Instagram", "username": f"@{username}", "display": f"Instagram • @{username}"}
        return {"platform": "Instagram", "username": "Unknown", "display": "Instagram"}

    # Facebook
    if "facebook.com" in url_lower or "fb.com" in url_lower:
        if len(parts) >= 1:
            username = parts[0].split("?")[0]
            if username and username not in ["profile.php", "pages", "groups"]:
                return {"platform": "Facebook", "username": username, "display": f"Facebook • {username}"}
        return {"platform": "Facebook", "username": "Unknown", "display": "Facebook"}

    # Linktree
    if "linktr.ee" in url_lower:
        if len(parts) >= 1:
            username = parts[0].split("?")[0]
            return {"platform": "Linktree", "username": username, "display": f"Linktree • {username}"}
        return {"platform": "Linktree", "username": "Unknown", "display": "Linktree"}

    # Bio.link
    if "bio.link" in url_lower:
        if len(parts) >= 1:
            username = parts[0].split("?")[0]
            return {"platform": "Bio.link", "username": username, "display": f"Bio.link • {username}"}

    # Amazon
    if "amazon." in url_lower or "amzn.to" in url_lower:
        return {"platform": "Amazon", "username": "Associates", "display": "Amazon Associates"}

    # Default
    domain = parsed.netloc.replace("www.", "")
    return {"platform": domain, "username": "Unknown", "display": domain}


def is_youtube_url(url):
    return any(x in url.lower() for x in ["youtube.com", "youtu.be"])

def extract_youtube_info(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            return None, None, [], "Failed to fetch page"

        html = resp.text
        soup = BeautifulSoup(html, "html.parser")

        channel_name = "Unknown Channel"
        channel_tag = soup.find("link", {"itemprop": "name"})
        if channel_tag and channel_tag.get("content"):
            channel_name = channel_tag["content"]
        else:
            meta = soup.find("meta", {"name": "title"})
            if meta and meta.get("content"):
                channel_name = meta["content"].split("-")[-1].strip() if "-" in meta["content"] else meta["content"]

        description = ""
        desc_tag = soup.find("meta", {"name": "description"})
        if desc_tag and desc_tag.get("content"):
            description = desc_tag["content"]

        match = re.search(r"var ytInitialData = ({.*?});", html)
        if match:
            try:
                data = json.loads(match.group(1))
                contents = data.get("contents", {}).get("twoColumnWatchNextResults", {}).get("results", {}).get("results", {}).get("contents", [])
                for item in contents:
                    if "videoSecondaryInfoRenderer" in item:
                        runs = item["videoSecondaryInfoRenderer"].get("description", {}).get("runs", [])
                        description = " ".join([r.get("text", "") for r in runs])
                        break
            except:
                pass

        desc_links = set()
        if description:
            found = re.findall(r'https?://[^\s<>"\']+', description)
            for link in found:
                desc_links.add(link.rstrip(".,)"))

        all_links = set()
        for tag in soup.find_all(["a", "link"], href=True):
            href = tag["href"].strip()
            if href.startswith(("http://", "https://")):
                all_links.add(href.split("#")[0])
            elif href.startswith("/"):
                all_links.add(urljoin("https://www.youtube.com", href).split("#")[0])

        return channel_name, description, list(desc_links), list(all_links)
    except Exception as e:
        return None, None, [], str(e)


def extract_hyperlinks(url):
    if is_youtube_url(url):
        channel, desc, desc_links, all_links = extract_youtube_info(url)
        return {
            "is_youtube": True,
            "channel": channel,
            "description": desc,
            "desc_links": desc_links,
            "all_links": all_links
        }, None
    else:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
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
            return {"is_youtube": False, "all_links": list(links)}, None
        except Exception as e:
            return None, str(e)


def analyze_link(link_url, source="Page"):
    start = time.time()
    identity = extract_platform_identity(link_url)

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
        resp = requests.get(link_url, headers=headers, timeout=9, allow_redirects=True)
        elapsed = round(time.time() - start, 2)
        final_url = resp.url
        text = resp.text.lower()
        title = ""
        try:
            soup = BeautifulSoup(resp.text, "html.parser")
            if soup.title and soup.title.string:
                title = soup.title.string.lower()
        except:
            pass

        # Update identity from final URL if better
        final_identity = extract_platform_identity(final_url)
        if final_identity["username"] != "Unknown":
            identity = final_identity

        detected = "Standard / Unknown"
        check_str = (link_url + " " + final_url).lower()
        for key, name in AFFILIATE_MAP.items():
            if key in check_str:
                detected = name
                break

        if resp.status_code >= 400:
            return {
                "url": link_url, "final_url": final_url, "type": "Dead Link",
                "status": f"🔴 Dead (HTTP {resp.status_code})", "network": detected,
                "source": source, "identity": identity, "response_time": elapsed, "severity": "Critical"
            }

        combined = text + " " + title
        for sig in OUT_OF_STOCK_SIGNATURES:
            if sig in combined:
                return {
                    "url": link_url, "final_url": final_url, "type": "Revenue Leak",
                    "status": "🟡 Out of Stock / Unavailable", "network": detected,
                    "source": source, "identity": identity, "response_time": elapsed, "severity": "High"
                }

        if detected != "Standard / Unknown":
            return {
                "url": link_url, "final_url": final_url, "type": "Safe Affiliate",
                "status": "🟢 Active & Monetized", "network": detected,
                "source": source, "identity": identity, "response_time": elapsed, "severity": "Low"
            }

        return {
            "url": link_url, "final_url": final_url, "type": "Neutral",
            "status": "⚪ Standard Link", "network": detected,
            "source": source, "identity": identity, "response_time": elapsed, "severity": "Low"
        }
    except:
        return {
            "url": link_url, "final_url": link_url, "type": "Dead Link",
            "status": "🔴 Timeout / Connection Failed", "network": "Unknown",
            "source": source, "identity": identity, "response_time": None, "severity": "Critical"
        }


def calculate_score(results):
    if not results:
        return 0, {}
    total = len(results)
    dead = sum(1 for r in results if r["type"] == "Dead Link")
    leaks = sum(1 for r in results if r["type"] == "Revenue Leak")
    safe = sum(1 for r in results if r["type"] == "Safe Affiliate")
    neutral = sum(1 for r in results if r["type"] == "Neutral")

    score = 100 - (dead * 18) - (leaks * 11) - (neutral * 1.5)
    if total > 0 and (safe / total) >= 0.5:
        score += 6
    score = max(0, min(100, round(score)))
    return score, {"dead": dead, "leaks": leaks, "safe": safe, "neutral": neutral, "total": total}


# ====================== MAIN ======================
if st.button("🚀 LAUNCH ULTRA AUDIT ENGINE"):
    if not target_url:
        st.warning("Please enter a valid URL.")
    else:
        with st.spinner("⚡ Analyzing page + extracting platform identities..."):
            data, error = extract_hyperlinks(target_url)

            if error:
                st.error(f"Error: {error}")
            else:
                is_youtube = data.get("is_youtube", False)
                channel_name = data.get("channel", "Unknown")
                description = data.get("description", "")
                desc_links = data.get("desc_links", [])
                all_links = data.get("all_links", [])

                links_with_source = []
                for link in desc_links:
                    links_with_source.append((link, "Description"))
                for link in all_links:
                    if link not in desc_links:
                        links_with_source.append((link, "Page / Other"))

                seen = set()
                unique_links = []
                for link, source in links_with_source:
                    if link not in seen:
                        seen.add(link)
                        unique_links.append((link, source))

                results = []
                with ThreadPoolExecutor(max_workers=25) as executor:
                    futures = {executor.submit(analyze_link, url, source): (url, source) for url, source in unique_links}
                    for future in as_completed(futures):
                        results.append(future.result())

                dead_list = [r for r in results if r["type"] == "Dead Link"]
                leak_list = [r for r in results if r["type"] == "Revenue Leak"]
                safe_list = [r for r in results if r["type"] == "Safe Affiliate"]
                neutral_list = [r for r in results if r["type"] == "Neutral"]

                score, breakdown = calculate_score(results)

                if len(safe_list) == 0:
                    st.markdown(f"""
                    <div class="no-affiliate-box">
                        <h2 style="margin-top:0; color:#fca5a5;">❌ No Affiliate Links Found</h2>
                        <p style="font-size:18px; margin-bottom:8px;">
                            <b>{channel_name}</b> has not added any affiliate links in the description or on this page.
                        </p>
                        <p style="margin:0; opacity:0.9;">
                            Only standard links (social media, playlists, internal links, etc.) were detected.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

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

                tab1, tab2, tab3, tab4 = st.tabs([
                    f"🚨 Dead Links ({len(dead_list)})",
                    f"💸 Revenue Leaks ({len(leak_list)})",
                    f"🛡️ Safe Affiliates ({len(safe_list)})",
                    f"🌐 All Links with Identity ({len(results)})"
                ])

                def render_card(item, idx):
                    identity_display = item.get("identity", {}).get("display", "Unknown")
                    st.markdown(f"""
                    <div class="log-card">
                        <b>#{idx} • {item['status']}</b><br>
                        <span class="identity-badge">{identity_display}</span><br><br>
                        <b>Original:</b> {item['url']}<br>
                        <b>Final:</b> {item['final_url']}<br>
                        <b>Network:</b> {item['network']}<br>
                        <b>Source:</b> {item['source']}
                    </div>
                    """, unsafe_allow_html=True)

                with tab1:
                    if not dead_list:
                        st.success("No dead links found.")
                    for i, item in enumerate(dead_list, 1):
                        render_card(item, i)

                with tab2:
                    if not leak_list:
                        st.success("No revenue leaks detected.")
                    for i, item in enumerate(leak_list, 1):
                        render_card(item, i)

                with tab3:
                    if not safe_list:
                        st.info("No active affiliate campaigns found.")
                    for i, item in enumerate(safe_list, 1):
                        render_card(item, i)

                with tab4:
                    st.write("### All Links with Platform Identity")
                    for i, item in enumerate(results, 1):
                        render_card(item, i)

                if is_youtube and description:
                    with st.expander("📝 Video Description Preview"):
                        st.write(description[:1500] + ("..." if len(description) > 1500 else ""))

                st.markdown("---")
                st.markdown("## 🧠 Smart Recommendations & Auto-Fix")

                if len(safe_list) == 0:
                    st.markdown(f"""
                    <div class="fix-card">
                        <h4>💡 Suggestion for {channel_name}</h4>
                        <p>No affiliate links were found on this page.</p>
                        <p><b>Recommended actions:</b></p>
                        <ul>
                            <li>Add relevant product, tool, or course affiliate links in the description.</li>
                            <li>Choose high-converting offers from Amazon, ClickBank, or other networks.</li>
                            <li>Clearly label the links (e.g. “Recommended tool”, “Get it here”).</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")
                st.subheader("📥 Export Full Report")
                df = pd.DataFrame(results)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download Complete Analysis (CSV)", data=csv, file_name="affiliate_scan_report.csv", mime="text/csv")