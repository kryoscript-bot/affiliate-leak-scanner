import streamlit as st
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from urllib.parse import urlparse, urljoin
import re
import json

st.set_page_config(page_title="Affiliate Leak Protocol Engine Pro v5.7", page_icon="⚡", layout="wide")

st.markdown("""
<style>
.main { background-color: #0b0f19 !important; color: #cbd5e1 !important; }
h1 { color: #00f2fe !important; font-weight: 800 !important; }
.metric-container-box {
    background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
    padding: 22px; border-radius: 16px; text-align: center; margin-bottom: 15px;
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
        <div style="color:#94a3b8; font-size:16px;">Detect. Fix. Monetize. — v5.7 (Fixed Link Extraction)</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("Deep scan blogs, Linktree, YouTube, TikTok, Twitter/X, Instagram & more.")

st.markdown("""
<div class="platform-bar">
    <div class="platform-badge">YouTube</div>
    <div class="platform-badge">TikTok</div>
    <div class="platform-badge">Twitter / X</div>
    <div class="platform-badge">Instagram</div>
    <div class="platform-badge">Linktree</div>
    <div class="platform-badge">Amazon</div>
    <div class="platform-badge">ClickBank</div>
</div>
""", unsafe_allow_html=True)

target_url = st.text_input("🎯 Enter Target URL", placeholder="https://youtu.be/xxxxx")

AFFILIATE_MAP = {
    "amazon.": "Amazon Associates", "amzn.to": "Amazon Associates",
    "clickbank": "ClickBank", "hop.clickbank": "ClickBank",
    "shareasale": "ShareASale", "cj.com": "CJ Affiliate",
    "impact.com": "Impact", "rstyle.me": "LTK",
    "skimlinks": "Skimlinks", "awin.": "Awin",
    "bit.ly": "Bitly", "linktr.ee": "Linktree", "bio.link": "Bio.link",
    "hotmart": "Hotmart", "digistore24": "Digistore24", "gumroad": "Gumroad"
}

OUT_OF_STOCK = [
    "currently unavailable", "out of stock", "temporarily unavailable",
    "item unavailable", "sold out", "product unlisted", "product unavailable",
    "this item is no longer available", "product missing"
]

JUNK = ["i.ytimg.com", "yt3.ggpht.com", "ytimg.com", "ggpht.com", "googleusercontent.com"]

def is_junk(url):
    u = url.lower()
    return any(j in u for j in JUNK) or u.endswith((".jpg", ".png", ".webp", ".gif", ".css", ".js"))

def extract_identity(url):
    if not url: return {"display": "Unknown"}
    u = url.lower()
    parts = [p for p in urlparse(url).path.strip("/").split("/") if p]

    if "youtube.com" in u or "youtu.be" in u:
        if "/@" in u:
            user = u.split("/@")[1].split("/")[0].split("?")[0]
            return {"display": f"YouTube • @{user}"}
        if "/channel/" in u:
            return {"display": f"YouTube • {u.split('/channel/')[1].split('/')[0]}"}
        return {"display": "YouTube"}
    if "tiktok.com" in u and "/@" in u:
        user = u.split("/@")[1].split("/")[0].split("?")[0]
        return {"display": f"TikTok • @{user}"}
    if ("twitter.com" in u or "x.com" in u) and parts:
        return {"display": f"Twitter/X • @{parts[0]}"}
    if "instagram.com" in u and parts and parts[0] not in ["p", "reel"]:
        return {"display": f"Instagram • @{parts[0]}"}
    if "linktr.ee" in u and parts:
        return {"display": f"Linktree • {parts[0]}"}
    if "amazon." in u or "amzn.to" in u:
        return {"display": "Amazon Associates"}
    return {"display": urlparse(url).netloc.replace("www.", "")}

def get_youtube_data(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}
        r = requests.get(url, headers=headers, timeout=15)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")

        # Channel Name
        channel = "Unknown Channel"
        for pat in [r'"ownerChannelName":"([^"]+)"', r'"channelName":"([^"]+)"', r'"author":"([^"]+)"']:
            m = re.search(pat, html)
            if m and len(m.group(1)) > 2:
                channel = m.group(1)
                break
        if channel == "Unknown Channel":
            t = soup.find("title")
            if t: channel = t.text.replace(" - YouTube", "").strip()

        # Description
        desc = ""
        meta = soup.find("meta", {"name": "description"})
        if meta: desc = meta.get("content", "")

        m = re.search(r"ytInitialData\s*=\s*({.+?});", html)
        if m:
            try:
                data = json.loads(m.group(1))
                contents = data.get("contents", {}).get("twoColumnWatchNextResults", {}).get("results", {}).get("results", {}).get("contents", [])
                for item in contents:
                    if "videoSecondaryInfoRenderer" in item:
                        runs = item["videoSecondaryInfoRenderer"].get("description", {}).get("runs", [])
                        desc = " ".join([x.get("text", "") for x in runs])
                        break
            except: pass

        # Links from description
        desc_links = re.findall(r'https?://[^\s<>"\']+', desc or "")
        desc_links = [l.rstrip(".,)") for l in desc_links]

        # Also get some page links (important ones only)
        page_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if href.startswith("http"):
                full = href.split("#")[0]
            elif href.startswith("/"):
                full = urljoin("https://www.youtube.com", href).split("#")[0]
            else:
                continue
            if not is_junk(full) and "youtube.com/watch" not in full and "youtube.com/shorts" not in full:
                page_links.append(full)

        return channel, desc, desc_links, list(set(page_links))[:15]  # limit page links
    except:
        return "Unknown Channel", "", [], []

def analyze(url, source):
    if is_junk(url): return None
    identity = extract_identity(url)
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
        r = requests.get(url, headers=headers, timeout=8, allow_redirects=True)
        final = r.url
        identity = extract_identity(final) if extract_identity(final)["display"] != "Unknown" else identity

        network = "Standard / Unknown"
        check = (url + " " + final).lower()
        for k, v in AFFILIATE_MAP.items():
            if k in check:
                network = v
                break

        if r.status_code >= 400:
            return {"url": url, "final_url": final, "type": "Dead Link", "status": f"🔴 Dead ({r.status_code})", "network": network, "source": source, "identity": identity}

        text = r.text.lower()[:25000]
        for sig in OUT_OF_STOCK:
            if sig in text:
                return {"url": url, "final_url": final, "type": "Revenue Leak", "status": "🟡 Out of Stock", "network": network, "source": source, "identity": identity}

        if network != "Standard / Unknown":
            return {"url": url, "final_url": final, "type": "Safe Affiliate", "status": "🟢 Active", "network": network, "source": source, "identity": identity}

        return {"url": url, "final_url": final, "type": "Neutral", "status": "⚪ Standard", "network": network, "source": source, "identity": identity}
    except:
        return {"url": url, "final_url": url, "type": "Dead Link", "status": "🔴 Failed", "network": "Unknown", "source": source, "identity": identity}

if st.button("🚀 LAUNCH ULTRA AUDIT ENGINE"):
    if not target_url:
        st.warning("Please enter a URL")
    else:
        with st.spinner("⚡ Analyzing..."):
            is_yt = any(x in target_url.lower() for x in ["youtube.com", "youtu.be"])
            
            if is_yt:
                channel, desc, desc_links, page_links = get_youtube_data(target_url)
                links = [(l, "Description") for l in desc_links] + [(l, "Page") for l in page_links]
            else:
                channel = "Unknown"
                desc = ""
                try:
                    headers = {"User-Agent": "Mozilla/5.0"}
                    r = requests.get(target_url, headers=headers, timeout=12)
                    soup = BeautifulSoup(r.text, "html.parser")
                    links = []
                    for a in soup.find_all("a", href=True):
                        href = a["href"].strip()
                        full = urljoin(r.url, href).split("#")[0]
                        if full.startswith("http") and not is_junk(full):
                            links.append((full, "Page"))
                except:
                    links = []

            # unique
            seen = set()
            final_links = []
            for u, s in links:
                if u not in seen:
                    seen.add(u)
                    final_links.append((u, s))

            results = []
            with ThreadPoolExecutor(max_workers=20) as ex:
                futs = {ex.submit(analyze, u, s): u for u, s in final_links}
                for f in as_completed(futs):
                    res = f.result()
                    if res: results.append(res)

            dead = [r for r in results if r["type"] == "Dead Link"]
            leaks = [r for r in results if r["type"] == "Revenue Leak"]
            safe = [r for r in results if r["type"] == "Safe Affiliate"]
            total = len(results)
            score = max(0, 100 - len(dead)*18 - len(leaks)*12)
            if total and len(safe)/total >= 0.5: score += 8
            score = min(100, score)

            if len(safe) == 0:
                st.markdown(f"""
                <div class="no-affiliate-box">
                    <h2 style="margin:0 0 10px 0;color:#fca5a5;">❌ No Affiliate Links Found</h2>
                    <p style="font-size:17px;"><b>{channel}</b> has not added any affiliate links in the description or on this page.</p>
                    <p style="opacity:0.85;margin:0;">Only standard / social links were detected.</p>
                </div>
                """, unsafe_allow_html=True)

            c1,c2,c3,c4,c5 = st.columns(5)
            with c1: st.markdown(f'<div class="metric-container-box"><h5 style="color:#94a3b8;margin:0;">TOTAL</h5><h1 style="color:#00f2fe;margin:6px 0 0;">{total}</h1></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-container-box"><h5 style="color:#94a3b8;margin:0;">DEAD</h5><h1 style="color:#ef4444;margin:6px 0 0;">{len(dead)}</h1></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-container-box"><h5 style="color:#94a3b8;margin:0;">LEAKS</h5><h1 style="color:#f59e0b;margin:6px 0 0;">{len(leaks)}</h1></div>', unsafe_allow_html=True)
            with c4: st.markdown(f'<div class="metric-container-box"><h5 style="color:#94a3b8;margin:0;">SAFE</h5><h1 style="color:#22c55e;margin:6px 0 0;">{len(safe)}</h1></div>', unsafe_allow_html=True)
            with c5: 
                col = "#22c55e" if score>=75 else "#f59e0b" if score>=45 else "#ef4444"
                st.markdown(f'<div class="metric-container-box"><h5 style="color:#94a3b8;margin:0;">SCORE</h5><h1 style="color:{col};margin:6px 0 0;">{score}</h1></div>', unsafe_allow_html=True)

            t1,t2,t3,t4 = st.tabs([f"🚨 Dead ({len(dead)})", f"💸 Leaks ({len(leaks)})", f"🛡️ Safe ({len(safe)})", f"🌐 All ({total})"])

            def card(item, i):
                st.markdown(f"""
                <div class="log-card">
                    <b>#{i} • {item['status']}</b><br>
                    <span class="identity-badge">{item['identity']['display']}</span><br><br>
                    <b>URL:</b> {item['url']}<br>
                    <b>Final:</b> {item['final_url']}<br>
                    <b>Network:</b> {item['network']}<br>
                    <b>Source:</b> {item['source']}
                </div>
                """, unsafe_allow_html=True)

            with t1:
                if not dead: st.success("No dead links found.")
                for i,x in enumerate(dead,1): card(x,i)
            with t2:
                if not leaks: st.success("No revenue leaks found.")
                for i,x in enumerate(leaks,1): card(x,i)
            with t3:
                if not safe: st.info("No safe affiliate links found.")
                for i,x in enumerate(safe,1): card(x,i)
            with t4:
                for i,x in enumerate(results,1): card(x,i)

            if desc:
                with st.expander("📝 Description Preview"):
                    st.write(desc[:1200])

            if len(safe) == 0:
                st.markdown(f"""
                <div class="fix-card">
                    <h4>💡 Recommendation for {channel}</h4>
                    <p>No affiliate links detected. Add high-converting offers from Amazon, ClickBank etc. in the description.</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            df = pd.DataFrame(results)
            st.download_button("📥 Download CSV", df.to_csv(index=False).encode(), "affiliate_report.csv", "text/csv")