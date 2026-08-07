import streamlit as st
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from collections import OrderedDict
from datetime import datetime
import json

# ============================================================
#          STRONG LINK + USERNAME EXTRACTION ALGORITHM
# ============================================================

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except:
        return False


def clean_url(url: str) -> str:
    tracking = {
        "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
        "fbclid", "gclid", "ref", "source", "mc_cid", "mc_eid", "igshid"
    }
    try:
        parsed = urlparse(url)
        if parsed.query:
            params = []
            for p in parsed.query.split("&"):
                key = p.split("=")[0].lower()
                if key not in tracking:
                    params.append(p)
            clean_q = "&".join(params)
            url = parsed._replace(query=clean_q).geturl()
        if url.endswith("/") and parsed.path not in ("", "/"):
            url = url.rstrip("/")
        return url
    except:
        return url


def extract_username_from_url(url: str):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().replace("www.", "")
        path = unquote(parsed.path).strip("/")
        if not path:
            return None
        parts = path.split("/")

        if domain in ("x.com", "twitter.com"):
            if parts and parts[0] not in ("i", "intent", "share", "search", "hashtag", "explore", "settings"):
                return parts[0]

        if domain in ("instagram.com", "www.instagram.com"):
            if parts and parts[0] not in ("p", "reel", "reels", "stories", "explore", "accounts", "direct"):
                return parts[0]

        if domain in ("youtube.com", "www.youtube.com", "m.youtube.com"):
            if parts:
                if parts[0] in ("c", "user", "channel"):
                    return parts[1] if len(parts) > 1 else None
                if parts[0].startswith("@"):
                    return parts[0][1:]
                return parts[0]

        if domain == "github.com":
            if parts and parts[0] not in ("features", "topics", "collections", "trending", "events", "marketplace", "pricing", "login", "join"):
                return parts[0]

        if "linkedin.com" in domain:
            if len(parts) >= 2 and parts[0] == "in":
                return parts[1]
            if len(parts) >= 2 and parts[0] == "company":
                return parts[1]

        if domain in ("tiktok.com", "www.tiktok.com"):
            if parts and parts[0].startswith("@"):
                return parts[0][1:]
            if parts:
                return parts[0]

        if domain in ("t.me", "telegram.me"):
            if parts:
                return parts[0]

        if parts and re.match(r'^[a-zA-Z0-9._]{2,30}$', parts[0]):
            return parts[0]
    except:
        pass
    return None


def extract_usernames_from_text(text: str) -> list:
    pattern = re.compile(r'(?<!\w)@([a-zA-Z0-9_]{2,30})\b')
    return list(OrderedDict.fromkeys(pattern.findall(text)))


def extract_links_from_text(text: str) -> list:
    url_pattern = re.compile(
        r'https?://[^\s<>"\'\)\]]+|'
        r'www\.[^\s<>"\'\)\]]+',
        re.IGNORECASE
    )
    found = url_pattern.findall(text)
    results = []
    seen = set()

    for raw in found:
        link = raw
        if link.lower().startswith("www."):
            link = "https://" + link
        link = link.rstrip(".,;:!?)]}")
        link = clean_url(link)

        if not is_valid_url(link) or link in seen:
            continue
        seen.add(link)

        username = extract_username_from_url(link)
        results.append({
            "url": link,
            "username": username,
            "domain": urlparse(link).netloc.replace("www.", ""),
            "title": username or link,
            "source": "pasted text"
        })

    pure_usernames = extract_usernames_from_text(text)
    for uname in pure_usernames:
        if any(r.get("username") == uname for r in results):
            continue
        results.append({
            "url": None,
            "username": uname,
            "domain": None,
            "title": f"@{uname}",
            "source": "pasted text"
        })
    return results


def extract_links_from_url(page_url: str, timeout: int = 12) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        resp = requests.get(page_url, headers=headers, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        final_url = resp.url
        soup = BeautifulSoup(resp.content, "lxml")
        page_title = soup.title.string.strip() if soup.title and soup.title.string else ""

        results = []
        seen = set()

        for a in soup.find_all("a", href=True):
            href = a.get("href", "").strip()
            if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
                continue

            absolute = urljoin(final_url, href)
            absolute = clean_url(absolute)

            if not is_valid_url(absolute) or absolute in seen:
                continue
            seen.add(absolute)

            anchor_text = a.get_text(strip=True)[:100]
            username = extract_username_from_url(absolute)
            title = username or anchor_text or absolute

            results.append({
                "url": absolute,
                "username": username,
                "domain": urlparse(absolute).netloc.replace("www.", ""),
                "title": title,
                "source": final_url
            })

        return {
            "success": True,
            "page_title": page_title,
            "page_url": final_url,
            "total": len(results),
            "links": results
        }
    except Exception as e:
        return {"success": False, "error": str(e), "links": []}


# ============================================================
#                      STREAMLIT UI
# ============================================================

st.set_page_config(
    page_title="LinkVault — Link + Username Extractor",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; margin-bottom: 0.2rem; }
    .sub-header { color: #64748b; font-size: 1rem; margin-bottom: 1.5rem; }
    .username-badge {
        background: #e0e7ff; color: #3730a3;
        padding: 3px 10px; border-radius: 20px;
        font-size: 0.85rem; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🔗 LinkVault</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Smart Link + Username Extractor</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Settings")
    mode = st.radio("Extraction Mode", ["From Text", "From Website URL"], index=0)
    st.markdown("---")
    st.markdown("### Features")
    st.markdown("""
    - Full clean links  
    - Username detection  
    - X, Instagram, GitHub, YouTube, TikTok, LinkedIn, Telegram  
    - Tracking parameters remove  
    - Search & Export
    """)

if mode == "From Text":
    text_input = st.text_area(
        "Paste text containing links or @usernames",
        height=180,
        placeholder="Example:\nhttps://x.com/elonmusk\n@nasa\nhttps://instagram.com/natgeo\nwww.github.com/torvalds"
    )
    extract_btn = st.button("🚀 Extract Links + Usernames", type="primary", use_container_width=True)

    if extract_btn:
        if not text_input.strip():
            st.warning("Please paste some text first.")
        else:
            with st.spinner("Extracting..."):
                results = extract_links_from_text(text_input)
                st.session_state["results"] = results
                st.session_state["source"] = "Extracted from text"

else:
    url_input = st.text_input("Enter Website URL", placeholder="https://example.com/page")
    extract_btn = st.button("🚀 Extract Links + Usernames", type="primary", use_container_width=True)

    if extract_btn:
        if not url_input.strip():
            st.warning("Please enter a URL.")
        else:
            with st.spinner("Fetching page and extracting..."):
                result = extract_links_from_url(url_input.strip())
                if result["success"]:
                    st.session_state["results"] = result["links"]
                    st.session_state["source"] = result.get("page_title") or result.get("page_url")
                else:
                    st.error(f"Error: {result.get('error', 'Unknown error')}")
                    st.session_state["results"] = []

if "results" in st.session_state and st.session_state["results"]:
    results = st.session_state["results"]

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Found", len(results))
    with col2:
        st.metric("With Username", sum(1 for r in results if r.get("username")))
    with col3:
        st.metric("Full Links", sum(1 for r in results if r.get("url")))

    search = st.text_input("🔍 Search results", placeholder="Search by username, domain or link...")

    filtered = results
    if search.strip():
        q = search.lower()
        filtered = [
            r for r in results
            if q in (r.get("username") or "").lower()
            or q in (r.get("url") or "").lower()
            or q in (r.get("domain") or "").lower()
            or q in (r.get("title") or "").lower()
        ]

    st.write(f"Showing **{len(filtered)}** results")

    for item in filtered:
        with st.container():
            if item.get("username"):
                st.markdown(f'<span class="username-badge">@{item["username"]}</span>', unsafe_allow_html=True)
            if item.get("url"):
                st.markdown(f"🔗 [{item['url']}]({item['url']})")
            else:
                st.caption("No full link available")
            if item.get("domain"):
                st.caption(f"Domain: {item['domain']}")
            st.markdown("---")

    st.markdown("### Export")
    export_data = json.dumps(results, indent=2, ensure_ascii=False)
    st.download_button(
        label="📥 Download JSON",
        data=export_data,
        file_name=f"linkvault_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        use_container_width=True
    )
else:
    st.info("👆 Choose a mode, enter text or URL, and click Extract to get started.")