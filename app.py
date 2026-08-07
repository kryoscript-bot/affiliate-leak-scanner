from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin, urlparse, unquote
from datetime import datetime, timezone
from collections import OrderedDict

app = Flask(__name__)

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
#                          ROUTES
# ============================================================

@app.route("/")
def index():
    return HTML_PAGE


@app.route("/api/extract", methods=["POST"])
def api_extract():
    data = request.get_json(silent=True) or {}
    mode = data.get("mode", "text")

    if mode == "url":
        url = (data.get("url") or "").strip()
        if not url:
            return jsonify({"success": False, "error": "URL is required"}), 400
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        if not is_valid_url(url):
            return jsonify({"success": False, "error": "Invalid URL"}), 400
        return jsonify(extract_links_from_url(url))
    else:
        text = data.get("text") or ""
        if not text.strip():
            return jsonify({"success": False, "error": "Text is required"}), 400
        links = extract_links_from_text(text)
        return jsonify({
            "success": True,
            "page_title": "Extracted from text",
            "total": len(links),
            "links": links
        })


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "time": datetime.now(timezone.utc).isoformat()})


# ============================================================
#                    COMPLETE FRONTEND (HTML + JS)
# ============================================================

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkVault — Smart Link + Username Extractor</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .link-card { transition: all 0.2s ease; }
        .link-card:hover { transform: translateY(-2px); }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 dark:bg-slate-900 dark:text-slate-100 min-h-screen">

    <nav class="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16 items-center">
                <div class="flex items-center gap-3">
                    <div class="w-9 h-9 bg-indigo-600 rounded-lg flex items-center justify-center">
                        <i class="fas fa-link text-white text-lg"></i>
                    </div>
                    <div>
                        <h1 class="text-xl font-bold tracking-tight">LinkVault</h1>
                        <p class="text-xs text-slate-500 dark:text-slate-400">Links + Username Extractor</p>
                    </div>
                </div>
                <div class="flex items-center gap-3">
                    <button id="themeToggle" class="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition">
                        <i class="fas fa-moon dark:hidden"></i>
                        <i class="fas fa-sun hidden dark:inline"></i>
                    </button>
                    <button id="exportBtn" class="hidden sm:flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition">
                        <i class="fas fa-download"></i> Export
                    </button>
                </div>
            </div>
        </div>
    </nav>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-700 p-6 mb-8">
            <div class="flex flex-wrap gap-3 mb-5">
                <button id="modeText" class="mode-btn px-4 py-2 rounded-lg text-sm font-medium bg-indigo-600 text-white">
                    <i class="fas fa-align-left mr-2"></i>From Text
                </button>
                <button id="modeUrl" class="mode-btn px-4 py-2 rounded-lg text-sm font-medium bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-200">
                    <i class="fas fa-globe mr-2"></i>From Website URL
                </button>
            </div>

            <div id="textPanel">
                <textarea id="inputText" rows="5" 
                    class="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none resize-none text-sm"
                    placeholder="Paste any text containing links or @usernames...&#10;&#10;Example:&#10;https://x.com/elonmusk  @nasa  https://instagram.com/natgeo  www.github.com/torvalds"></textarea>
            </div>

            <div id="urlPanel" class="hidden">
                <input id="inputUrl" type="url" 
                    class="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none text-sm"
                    placeholder="https://example.com/page">
                <p class="mt-2 text-xs text-slate-500">Enter any public webpage URL to extract all links + usernames</p>
            </div>

            <div class="mt-5 flex flex-wrap items-center gap-3">
                <button id="extractBtn" class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-xl transition flex items-center gap-2">
                    <i class="fas fa-magic"></i>
                    <span>Extract Links</span>
                </button>
                <button id="clearBtn" class="px-4 py-2.5 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-xl transition text-sm">
                    Clear
                </button>
                <div id="status" class="text-sm text-slate-500 ml-auto"></div>
            </div>
        </div>

        <div id="resultsHeader" class="hidden mb-5 flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-4">
                <div class="text-sm">
                    <span class="font-semibold text-indigo-600 dark:text-indigo-400" id="linkCount">0</span> items found
                </div>
                <div class="h-4 w-px bg-slate-300 dark:bg-slate-600"></div>
                <div class="relative">
                    <i class="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm"></i>
                    <input id="searchInput" type="text" placeholder="Search..." 
                        class="pl-9 pr-4 py-2 text-sm rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 focus:ring-2 focus:ring-indigo-500 outline-none w-56">
                </div>
            </div>
            <div class="flex items-center gap-2">
                <select id="sortSelect" class="text-sm rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 px-3 py-2 outline-none">
                    <option value="default">Original Order</option>
                    <option value="username">Sort by Username</option>
                    <option value="domain">Sort by Domain</option>
                    <option value="title">Sort by Title</option>
                </select>
                <button id="saveAllBtn" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium rounded-lg transition">
                    <i class="fas fa-save mr-1"></i> Save All
                </button>
            </div>
        </div>

        <div id="linksContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-10"></div>

        <div id="emptyState" class="text-center py-20">
            <div class="w-20 h-20 bg-indigo-100 dark:bg-indigo-900/30 rounded-full flex items-center justify-center mx-auto mb-5">
                <i class="fas fa-link text-3xl text-indigo-600 dark:text-indigo-400"></i>
            </div>
            <h2 class="text-xl font-semibold mb-2">No links yet</h2>
            <p class="text-slate-500 dark:text-slate-400 max-w-md mx-auto">
                Paste text with links/@usernames or enter a website URL and click <strong>Extract Links</strong>
            </p>
        </div>

        <div id="savedSection" class="hidden mt-12">
            <div class="flex items-center justify-between mb-5">
                <h2 class="text-lg font-semibold flex items-center gap-2">
                    <i class="fas fa-bookmark text-indigo-600"></i> Saved
                    <span id="savedCount" class="text-sm font-normal text-slate-500">(0)</span>
                </h2>
                <button id="clearSavedBtn" class="text-sm text-red-600 hover:text-red-700">Clear All</button>
            </div>
            <div id="savedContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"></div>
        </div>
    </main>

    <div id="toast" class="fixed bottom-6 right-6 bg-slate-800 text-white px-5 py-3 rounded-xl shadow-lg transform translate-y-20 opacity-0 transition-all duration-300 z-50 text-sm font-medium"></div>

<script>
let currentLinks = [];
let currentMode = "text";

const modeTextBtn = document.getElementById("modeText");
const modeUrlBtn = document.getElementById("modeUrl");
const textPanel = document.getElementById("textPanel");
const urlPanel = document.getElementById("urlPanel");
const inputText = document.getElementById("inputText");
const inputUrl = document.getElementById("inputUrl");
const extractBtn = document.getElementById("extractBtn");
const clearBtn = document.getElementById("clearBtn");
const statusEl = document.getElementById("status");
const linksContainer = document.getElementById("linksContainer");
const emptyState = document.getElementById("emptyState");
const resultsHeader = document.getElementById("resultsHeader");
const linkCount = document.getElementById("linkCount");
const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");
const saveAllBtn = document.getElementById("saveAllBtn");
const savedSection = document.getElementById("savedSection");
const savedContainer = document.getElementById("savedContainer");
const savedCount = document.getElementById("savedCount");
const clearSavedBtn = document.getElementById("clearSavedBtn");
const exportBtn = document.getElementById("exportBtn");
const themeToggle = document.getElementById("themeToggle");
const toast = document.getElementById("toast");

function initTheme() {
    if (localStorage.getItem("theme") === "dark" ||
        (!localStorage.getItem("theme") && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
        document.documentElement.classList.add("dark");
    }
}
themeToggle.addEventListener("click", () => {
    document.documentElement.classList.toggle("dark");
    localStorage.setItem("theme", document.documentElement.classList.contains("dark") ? "dark" : "light");
});
initTheme();

modeTextBtn.addEventListener("click", () => {
    currentMode = "text";
    modeTextBtn.className = "mode-btn px-4 py-2 rounded-lg text-sm font-medium bg-indigo-600 text-white";
    modeUrlBtn.className = "mode-btn px-4 py-2 rounded-lg text-sm font-medium bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-200";
    textPanel.classList.remove("hidden");
    urlPanel.classList.add("hidden");
});
modeUrlBtn.addEventListener("click", () => {
    currentMode = "url";
    modeUrlBtn.className = "mode-btn px-4 py-2 rounded-lg text-sm font-medium bg-indigo-600 text-white";
    modeTextBtn.className = "mode-btn px-4 py-2 rounded-lg text-sm font-medium bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-200";
    urlPanel.classList.remove("hidden");
    textPanel.classList.add("hidden");
});

extractBtn.addEventListener("click", async () => {
    let payload = { mode: currentMode };
    if (currentMode === "text") {
        const text = inputText.value.trim();
        if (!text) { showToast("Please paste some text first", "error"); return; }
        payload.text = text;
    } else {
        const url = inputUrl.value.trim();
        if (!url) { showToast("Please enter a URL", "error"); return; }
        payload.url = url;
    }

    setLoading(true);
    statusEl.textContent = "Extracting...";

    try {
        const res = await fetch("/api/extract", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!data.success) {
            showToast(data.error || "Failed", "error");
            statusEl.textContent = "";
            setLoading(false);
            return;
        }
        currentLinks = data.links || [];
        renderLinks(currentLinks);
        statusEl.textContent = data.page_title ? `Source: ${data.page_title}` : "";
        showToast(`Found ${currentLinks.length} items`);
    } catch (err) {
        showToast("Server error", "error");
        statusEl.textContent = "";
    } finally {
        setLoading(false);
    }
});

clearBtn.addEventListener("click", () => {
    inputText.value = "";
    inputUrl.value = "";
    currentLinks = [];
    renderLinks([]);
    statusEl.textContent = "";
});

function renderLinks(links) {
    if (!links || links.length === 0) {
        linksContainer.innerHTML = "";
        emptyState.classList.remove("hidden");
        resultsHeader.classList.add("hidden");
        return;
    }
    emptyState.classList.add("hidden");
    resultsHeader.classList.remove("hidden");
    linkCount.textContent = links.length;

    let filtered = [...links];
    const query = searchInput.value.toLowerCase().trim();
    if (query) {
        filtered = filtered.filter(l =>
            (l.url || "").toLowerCase().includes(query) ||
            (l.username || "").toLowerCase().includes(query) ||
            (l.title || "").toLowerCase().includes(query) ||
            (l.domain || "").toLowerCase().includes(query)
        );
    }

    const sort = sortSelect.value;
    if (sort === "domain") filtered.sort((a, b) => (a.domain || "").localeCompare(b.domain || ""));
    else if (sort === "username") filtered.sort((a, b) => (a.username || "").localeCompare(b.username || ""));
    else if (sort === "title") filtered.sort((a, b) => (a.title || "").localeCompare(b.title || ""));

    linksContainer.innerHTML = filtered.map((item, idx) => {
        const hasUsername = !!item.username;
        const hasLink = !!item.url;
        return `
        <div class="link-card bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl p-4 shadow-sm hover:shadow-md">
            <div class="flex items-center justify-between gap-2 mb-2">
                <div class="flex items-center gap-2 min-w-0">
                    ${hasUsername ? `
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-300">
                            @${escapeHtml(item.username)}
                        </span>
                    ` : `
                        <span class="text-sm font-medium text-slate-700 dark:text-slate-200 truncate">
                            ${escapeHtml(item.title || "No username")}
                        </span>
                    `}
                </div>
                <button onclick="saveLink(${idx})" class="text-slate-400 hover:text-emerald-600 transition p-1" title="Save">
                    <i class="fas fa-bookmark"></i>
                </button>
            </div>
            ${hasLink ? `
                <div class="mb-3">
                    <a href="${escapeHtml(item.url)}" target="_blank" rel="noopener"
                       class="text-sm text-indigo-600 dark:text-indigo-400 hover:underline break-all">
                        ${escapeHtml(item.url)}
                    </a>
                </div>
            ` : `<div class="mb-3 text-sm text-slate-400 italic">No full link</div>`}
            <div class="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
                <span>${item.domain ? escapeHtml(item.domain) : "—"}</span>
                <div class="flex gap-3">
                    \( {hasLink ? `<button onclick="copyLink(' \){escapeHtml(item.url)}')" class="hover:text-indigo-600" title="Copy Link"><i class="fas fa-copy"></i></button>` : ""}
                    \( {hasUsername ? `<button onclick="copyLink('@ \){escapeHtml(item.username)}')" class="hover:text-indigo-600" title="Copy Username"><i class="fas fa-user"></i></button>` : ""}
                </div>
            </div>
        </div>`;
    }).join("");
}

searchInput.addEventListener("input", () => renderLinks(currentLinks));
sortSelect.addEventListener("change", () => renderLinks(currentLinks));

function getSaved() {
    try { return JSON.parse(localStorage.getItem("linkvault_saved") || "[]"); } 
    catch { return []; }
}
function setSaved(arr) {
    localStorage.setItem("linkvault_saved", JSON.stringify(arr));
    renderSaved();
}
function saveLink(idx) {
    const item = currentLinks[idx];
    if (!item) return;
    const saved = getSaved();
    const key = item.url || item.username;
    if (saved.some(s => (s.url || s.username) === key)) {
        showToast("Already saved"); return;
    }
    saved.unshift({ ...item, savedAt: new Date().toISOString() });
    setSaved(saved);
    showToast("Saved");
}
saveAllBtn.addEventListener("click", () => {
    if (!currentLinks.length) return;
    const saved = getSaved();
    let added = 0;
    currentLinks.forEach(item => {
        const key = item.url || item.username;
        if (!saved.some(s => (s.url || s.username) === key)) {
            saved.unshift({ ...item, savedAt: new Date().toISOString() });
            added++;
        }
    });
    setSaved(saved);
    showToast(added ? `${added} items saved` : "All already saved");
});

function renderSaved() {
    const saved = getSaved();
    savedCount.textContent = `(${saved.length})`;
    if (saved.length === 0) {
        savedSection.classList.add("hidden");
        return;
    }
    savedSection.classList.remove("hidden");
    savedContainer.innerHTML = saved.map((item, idx) => `
        <div class="link-card bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl p-4">
            <div class="flex items-start justify-between gap-2 mb-2">
                <div>
                    ${item.username ? `
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-300 mb-1">
                            @${escapeHtml(item.username)}
                        </span>` : ""}
                    ${item.url ? `
                        <a href="${escapeHtml(item.url)}" target="_blank" class="block text-sm text-indigo-600 dark:text-indigo-400 hover:underline break-all">
                            ${escapeHtml(item.url)}
                        </a>` : `<div class="text-sm text-slate-500">@${escapeHtml(item.username)}</div>`}
                </div>
                <button onclick="removeSaved(${idx})" class="text-slate-400 hover:text-red-500 p-1">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join("");
}
function removeSaved(idx) {
    const saved = getSaved();
    saved.splice(idx, 1);
    setSaved(saved);
    showToast("Removed");
}
clearSavedBtn.addEventListener("click", () => {
    if (confirm("Clear all saved items?")) {
        setSaved([]);
        showToast("Cleared");
    }
});

exportBtn.addEventListener("click", () => {
    const saved = getSaved();
    const data = saved.length ? saved : currentLinks;
    if (!data.length) { showToast("Nothing to export", "error"); return; }
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `linkvault-${new Date().toISOString().slice(0,10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    showToast("Exported");
});

function setLoading(loading) {
    extractBtn.disabled = loading;
    extractBtn.innerHTML = loading
        ? `<i class="fas fa-spinner fa-spin"></i> <span>Extracting...</span>`
        : `<i class="fas fa-magic"></i> <span>Extract Links</span>`;
}
function showToast(msg, type = "success") {
    toast.textContent = msg;
    toast.className = `fixed bottom-6 right-6 px-5 py-3 rounded-xl shadow-lg transform transition-all duration-300 z-50 text-sm font-medium ${
        type === "error" ? "bg-red-600" : "bg-slate-800"
    } translate-y-0 opacity-100`;
    setTimeout(() => toast.classList.add("translate-y-20", "opacity-0"), 2500);
}
function escapeHtml(str) {
    if (!str) return "";
    return String(str).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#039;");
}
function copyLink(text) {
    navigator.clipboard.writeText(text).then(() => showToast("Copied!"));
}
renderSaved();
</script>
</body>
</html>
'''

if __name__ == "__main__":
    print("\\n🚀 LinkVault is running!")
    print("➡️  Open: http://127.0.0.1:5000\\n")
    app.run(host="0.0.0.0", port=5000, debug=True)