import streamlit as st
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from urllib.parse import urlparse, urljoin
import re
import json

st.set_page_config(
    page_title="Affiliate Leak Protocol Engine Pro v5.6",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .main { background-color: #0b0f19 !important; color: #cbd5e1 !important; font-family: 'Inter', sans-serif; }
    h1 { color: #00f2fe !important; font-weight: 800 !important; letter-spacing: -1.5px; text-shadow: 0 0 15px rgba(0,242,254,0.25); }
    .metric-container-box {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        padding: 22px; border-radius: 16px; text-align: center; margin-bottom: 15px;
        border: 1px solid rgba(255,255,255,0.04);
    }
    .stButton>button {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #0b0f19 !important; border-radius: 12px !important; padding: 16px 36px !important;
        font-weight: 800 !important; font-size: 18px !important; border: none !important; width: 100%;
    }
    .log-card {
        background: #ffffff !important; color: #1f2937 !important; padding: 18px 20px;
        border-radius: 12px; margin-bottom: 12px; border: 1px solid #e5e7eb;
    }
    .no-affiliate-box {
        background: linear-gradient(135deg, #450a0a 0%, #7f1d1d 100%);
        border: 1px solid #ef4444; border-radius: 14px; padding: 24px;
        margin-bottom: 20px; color: #fecaca; text-align: center;
    }
    .identity-badge {
        display: inline-block; background: #e0f2fe; color: #0369a1;
        padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; margin-top: 6px;
    }
    .platform-bar { display: flex; flex-wrap: wrap; gap: 10px; margin: 16px 0; opacity: 0.8; }
    .platform-badge {
        background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.12);
        color: #94a3b8; padding: 6px 14px; border-radius: 20px; font-size: 13px;
    }
    .fix-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        border: 1px solid #4f46e5; border-radius: 14px; padding: 20px; margin-bottom: 14px; color: #e0e7ff;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex; align-items:center; gap:16px; margin-bottom:8px;">
    <div style="font-size:52px; background:linear-gradient(135deg,#00f2fe,#4facfe); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">⚡</div>
    <div>
        <h1 style="margin:0;">Affiliate Leak Protocol Engine Pro</h1>
        <div style="color:#94a3b8; font-size:16px;">Detect. Fix. Monetize. — Ultra Advanced v5.6</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("Deep scan blogs, Linktree, YouTube, TikTok, Twitter/X, Instagram & more. Extracts platform + username and detects dead & out-of-stock affiliate links.")

st.markdown("""
<div class="platform-bar">
    <div class="platform-badge">YouTube</div>
    <div class="platform-badge">TikTok</div>
    <div class="platform-badge">Twitter / X</div>
    <div class="platform-badge">Instagram</div>
    <div class="platform-badge">Linktree</div>
    <div class="platform-badge">Amazon</div>
    <div class="platform-badge">ClickBank</div>
    <div class="platform-badge">ShareASale</div>
</div>
""", unsafe_allow_html=True)

target_url = st.text_input("🎯 Enter Target URL", placeholder="https://youtu.be/xxxxx or https://linktr.ee/username")

AFFILIATE_MAP = {
    "amazon.": "Amazon Associates", "amzn.to": "Amazon Associates",
    "clickbank": "ClickBank", "hop.clickbank": "ClickBank",
    "shareasale": "ShareASale", "cj.com": "CJ Affiliate",
    "impact.com": "Impact", "impactradius": "Impact",
    "rakuten": "Rakuten", "rstyle.me": "LTK",
    "skimlinks": "Skimlinks", "viglink": "Sovrn",
    "awin.": "Awin", "awin1.com": "Awin",
    "bit.ly": "Bitly", "linktr.ee": "Linktree", "bio.link": "Bio.link",
    "hotmart": "Hotmart", "digistore24": "Digistore24", "gumroad": "Gumroad"
}

OUT_OF_STOCK = [
    "currently unavailable", "out of stock", "temporarily unavailable",
    "item unavailable", "sold out", "product unlisted", "product unavailable",
    "this item is no longer available", "product missing", "backorder only"
]

# Junk domains to ignore (especially on YouTube)
JUNK_DOMAINS = [
    "i.ytimg.com", "yt3.ggpht.com", "ytimg.com", "googleusercontent.com",
    "ggpht.com", "youtu.be/generate", "youtube.com/embed", "youtube.com/s"
]

def is_junk_link(url: str) -> bool:
    url_lower = url.lower()
    for junk in JUNK_DOMAINS:
        if junk in url_lower:
            return True
    if url_lower.endswith((".jpg", ".png", ".gif", ".webp", ".svg", ".css", ".js")):
        return True
    return False

def extract_platform_identity(url: str) -> dict:
    if not url:
        return {"platform": "Unknown", "username": "Unknown", "display": "Unknown"}

    url_lower = url.lower()
    parsed = urlparse(url)
    parts = [p for p in parsed.path.strip("/").split("/") if p]

    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        if "/@" in url_lower:
            username = url_lower.split("/@")[1].split("/")[0].split("?")[0]
            return {"platform": "YouTube", "username": f"@{username}", "display": f"YouTube • @{username}"}
        if "/channel/" in url_lower:
            cid = url_lower.split("/channel/")[1].split("/")[0].split("?")[0]
            return {"platform": "YouTube", "username": cid, "display": f"YouTube • {cid}"}
        if len(parts) > 1 and parts[0] in ["c", "user"]:
            return {"platform": "YouTube", "username": f"@{parts[1]}", "display": f"YouTube • @{parts[1]}"}
        return {"platform": "YouTube", "username": "Unknown", "display": "YouTube"}

    if "tiktok.com" in url_lower:
        if "/@" in url_lower:
            username = url_lower.split("/@")[1].split("/")[0].split("?")[0]
            return {"platform": "TikTok", "username": f"@{username}", "display": f"TikTok • @{username}"}
        return {"platform": "TikTok", "username": "Unknown", "display": "TikTok"}

    if "twitter.com" in url_lower or "x.com" in url_lower:
        if parts and parts[0] not in ["i", "intent", "home", "search"]:
            return {"platform": "Twitter/X", "username": f"@{parts[0]}", "display": f"Twitter/X • @{parts[0]}"}
        return {"platform": "Twitter/X", "username": "Unknown", "display": "Twitter/X"}

    if "instagram.com" in url_lower:
        if parts and parts[0] not in ["p", "reel", "stories", "explore"]:
            return {"platform": "Instagram", "username": f"@{parts[0]}", "display": f"Instagram • @{parts[0]}"}
        return {"platform": "Instagram", "username": "Unknown", "display": "Instagram"}

    if "linktr.ee" in url_lower and parts:
        return {"platform": "Linktree", "username": parts[0], "display": f"Linktree • {parts[0]}"}

    if "amazon." in url_lower or "amzn.to" in url_lower:
        return {"platform": "Amazon", "username": "Associates", "display": "Amazon Associates"}

    domain = parsed.netloc.replace("www.", "") if parsed.netloc else "Unknown"
    return {"platform": domain, "username": "Unknown", "display": domain}


def extract_youtube_data(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            return "Unknown Channel", "", []

        html = resp.text
        soup = BeautifulSoup(html, "html.parser")

        # === Strong Channel Name Extraction ===
        channel_name = "Unknown Channel"

        # Method 1: JSON patterns
        patterns = [
            r'"ownerChannelName"\s*:\s*"([^"]+)"',
            r'"channelName"\s*:\s*"([^"]+)"',
            r'"author"\s*:\s*"([^"]+)"',
            r'"ownerText"\s*:\s*\{\s*"runs"\s*:\s*\[\s*\{\s*"text"\s*:\s*"([^"]+)"',
        ]
        for p in patterns:
            match = re.search(p, html)
            if match:
                name = match.group(1).strip()
                if name and len(name) > 1 and "YouTube" not in name:
                    channel_name = name
                    break

        # Method 2: Meta / link tags
        if channel_name == "Unknown Channel":
            for selector in [
                {"property": "og:video:tag"},
                {"itemprop": "name"},
                {"name": "author"}
            ]:
                tag = soup.find("meta", selector) or soup.find("link", selector)
                if tag and tag.get("content"):
                    channel_name = tag["content"]
                    break

        # Method 3: Title fallback
        if channel_name == "Unknown Channel":
            title = soup.find("title")
            if title and title.text:
                t = title.text.replace(" - YouTube", "").strip()
                if " - " in t:
                    channel_name = t.split(" - ")[-1].strip()
                else:
                    channel_name = t

        # Description
        description = ""
        desc_meta = soup.find("meta", {"name": "description"})
        if desc_meta and desc_meta.get("content"):
            description = desc_meta["content"]

        # Better description from ytInitialData
        match = re.search(r"ytInitialData\s*=\s*({.+?});", html)
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

        # Extract links from description only (cleaner)
        desc_links = []
        if description:
            found = re.findall(r'https?://[^\s<>"\']+', description)
            desc_links = [l.rstrip(".,)") for l in found]

        return channel_name, description, desc_links

    except Exception:
        return "Unknown Channel", "", []


def extract_links(url):
    if any(x in url.lower() for x in ["youtube.com", "youtu.be"]):
        channel, desc, desc_links = extract_youtube_data(url)
        return {
            "is_youtube": True,
            "channel": channel,
            "description": desc,
            "links": [(l, "Description") for l in desc_links]
        }, None

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = requests.get(url, headers=headers, timeout=14)
        if resp.status_code != 200:
            return None, f"HTTP {resp.status_code}"

        soup = BeautifulSoup(resp.text, "html.parser")
        base = resp.url
        links = []
        for tag in soup.find_all(["a", "link"], href=True):
            href = tag["href"].strip()
            if not href or href.startswith(("#", "javascript:", "mailto:")):
                continue
            full = urljoin(base, href).split("#")[0]
            if full.startswith("http") and not is_junk_link(full):
                links.append((full, "Page"))
        return {"is_youtube": False, "channel": "Unknown", "links": links}, None
    except Exception as e:
        return None, str(e)


def analyze_link(link_url, source="Page"):
    identity = extract_platform_identity(link_url)

    if is_junk_link(link_url):
        return None  # skip junk

    try:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
        resp = requests.get(link_url, headers=headers, timeout=8, allow_redirects=True)
        final_url = resp.url

        # Update identity from final URL
        final_id = extract_platform_identity(final_url)
        if final_id["username"] != "Unknown":
            identity = final_id

        detected = "Standard / Unknown"
        check = (link_url + " " + final_url).lower()
        for key, name in AFFILIATE_MAP.items():
            if key in check:
                detected = name
                break

        if resp.status_code >= 400:
            return {
                "url": link_url, "final_url": final_url, "type": "Dead Link",
                "status": f"🔴 Dead (HTTP {resp.status_code})",
                "network": detected, "source": source, "identity": identity
            }

        text = resp.text.lower()[:30000]  # limit for speed
        for sig in OUT_OF_STOCK:
            if sig in text:
                return {
                    "url": link_url, "final_url": final_url, "type": "Revenue Leak",
                    "status": "🟡 Out of Stock / Unavailable",
                    "network": detected, "source": source, "identity": identity
                }

        if detected != "Standard / Unknown":
            return {
                "url": link_url, "final_url": final_url, "type": "Safe Affiliate",
                "status": "🟢 Active & Monetized",
                "network": detected, "source": source, "identity": identity
            }

        return {
            "url": link_url, "final_url": final_url, "type": "Neutral",
            "status": "⚪ Standard Link",
            "network": detected, "source": source, "identity": identity
        }
    except:
        return {
            "url": link_url, "final_url": link_url, "type": "Dead Link",
            "status": "🔴 Timeout / Failed",
            "network": "Unknown", "source": source, "identity": identity
        }


def calculate_score(results):
    if not results:
        return 0, {"total": 0, "dead": 0, "leaks": 0, "safe": 0}
    total = len(results)
    dead = sum(1 for r in results if r["type"] == "Dead Link")
    leaks = sum(1 for r in results if r["type"] == "Revenue Leak")
    safe = sum(1 for r in results if r["type"] == "Safe Affiliate")

    score = 100 - (dead * 18) - (leaks * 12)
    if total > 0 and safe / total >= 0.5:
        score += 8
    score = max(0, min(100, round(score)))
    return score, {"total": total, "dead": dead, "leaks": leaks, "safe": safe}


if st.button("🚀 LAUNCH ULTRA AUDIT ENGINE"):
    if not target_url:
        st.warning("Please enter a valid URL.")
    else:
        with st.spinner("⚡ Running upgraded analysis..."):
            data, error = extract_links(target_url)

            if error:
                st.error(error)
            else:
                channel_name = data.get("channel", "Unknown Channel")
                description = data.get("description", "")
                raw_links = data.get("links", [])

                # Remove duplicates + junk
                seen = set()
                clean_links = []
                for url, source in raw_links:
                    if url not in seen and not is_junk_link(url):
                        seen.add(url)
                        clean_links.append((url, source))

                results = []
                with ThreadPoolExecutor(max_workers=20) as executor:
                    futures = {executor.submit(analyze_link, url, src): url for url, src in clean_links}
                    for future in as_completed(futures):
                        res = future.result()
                        if res:
                            results.append(res)

                dead_list = [r for r in results if r["type"] == "Dead Link"]
                leak_list = [r for r in results if r["type"] == "Revenue Leak"]
                safe_list = [r for r in results if r["type"] == "Safe Affiliate"]
                score, breakdown = calculate_score(results)

                # No Affiliate Box
                if breakdown["safe"] == 0:
                    st.markdown(f"""
                    <div class="no-affiliate-box">
                        <h2 style="margin:0 0 10px 0; color:#fca5a5;">❌ No Affiliate Links Found</h2>
                        <p style="font-size:17px;">
                            <b>{channel_name}</b> has not added any affiliate links in the description or on this page.
                        </p>
                        <p style="opacity:0.85; margin:0;">Only standard / social links were detected.</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Metrics
                st.markdown("---")
                c1, c2, c3, c4, c5 = st.columns(5)
                with c1:
                    st.markdown(f'<div class="metric-container-box"><h5 style="color:#94a3b8;margin:0;">TOTAL</h5><h1 style="color:#00f2fe;margin:6px 0 0;">{breakdown["total"]}</h1></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="metric-container-box"><h5 style="color:#94a3b8;margin:0;">DEAD</h5><h1 style="color:#ef4444;margin:6px 0 0;">{breakdown["dead"]}</h1></div>', unsafe_allow_html=True)
                with c3:
                    st.markdown(f'<div class="metric-container-box"><h5 style="color:#94a3b8;margin:0;">LEAKS</h5><h1 style="color:#f59e0b;margin:6px 0 0;">{breakdown["leaks"]}</h1></div>', unsafe_allow_html=True)
                with c4:
                    st.markdown(f'<div class="metric-container-box"><h5 style="color:#94a3b8;margin:0;">SAFE</h5><h1 style="color:#22c55e;margin:6px 0 0;">{breakdown["safe"]}</h1></div>', unsafe_allow_html=True)
                with c5:
                    color = "#22c55e" if score >= 75 else "#f59e0b" if score >= 45 else "#ef4444"
                    st.markdown(f'<div class="metric-container-box"><h5 style="color:#94a3b8;margin:0;">SCORE</h5><h1 style="color:{color};margin:6px 0 0;">{score}</h1></div>', unsafe_allow_html=True)

                # Tabs
                tab1, tab2, tab3, tab4 = st.tabs([
                    f"🚨 Dead ({len(dead_list)})",
                    f"💸 Leaks ({len(leak_list)})",
                    f"🛡️ Safe ({len(safe_list)})",
                    f"🌐 All ({len(results)})"
                ])

                def render(item, idx):
                    ident = item.get("identity", {}).get("display", "Unknown")
                    st.markdown(f"""
                    <div class="log-card">
                        <b>#{idx} • {item['status']}</b><br>
                        <span class="identity-badge">{ident}</span><br><br>
                        <b>URL:</b> {item['url']}<br>
                        <b>Final:</b> {item['final_url']}<br>
                        <b>Network:</b> {item['network']}<br>
                        <b>Source:</b> {item['source']}
                    </div>
                    """, unsafe_allow_html=True)

                with tab1:
                    if not dead_list: st.success("No dead links found.")
                    for i, item in enumerate(dead_list, 1): render(item, i)

                with tab2:
                    if not leak_list: st.success("No revenue leaks found.")
                    for i, item in enumerate(leak_list, 1): render(item, i)

                with tab3:
                    if not safe_list: st.info("No safe affiliate links found.")
                    for i, item in enumerate(safe_list, 1): render(item, i)

                with tab4:
                    for i, item in enumerate(results, 1): render(item, i)

                if description:
                    with st.expander("📝 Description Preview"):
                        st.write(description[:1200] + ("..." if len(description) > 1200 else ""))

                st.markdown("---")
                if breakdown["safe"] == 0:
                    st.markdown(f"""
                    <div class="fix-card">
                        <h4>💡 Recommendation for {channel_name}</h4>
                        <p>No affiliate links detected. Consider adding high-converting offers from Amazon, ClickBank, or other networks in the description.</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")
                st.subheader("📥 Export Report")
                df = pd.DataFrame(results)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV Report", data=csv, file_name="affiliate_scan_v56.csv", mime="text/csv")