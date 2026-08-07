import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

# Page Configuration
st.set_page_config(page_title="Affiliate Leak Scanner", page_icon="🔍", layout="wide")

st.title("🔍 Free Affiliate Link & Revenue Leak Scanner")
st.write("Apne blog post ka URL daalein aur check karein ki koi affiliate link broken ya Out of Stock toh nahi hai!")

# User Input
blog_url = st.text_input("Enter your Blog Post URL:", placeholder="https://blogspot.com")

def extract_links(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_color != 200:
            return None, f"Error: Blog page load nahi ho payi (Status Code: {response.status_code})"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        
        # Blog ke saare links nikalna
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Generic links ko filter karna (jaise home, category, tags)
            if "amazon" in href or "affiliate" in href or "amzn" in href or "click" in href:
                links.append(href)
                
        return list(set(links)), None
    except Exception as e:
        return None, str(e)

def check_link_status(link):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(link, headers=headers, timeout=10, allow_redirects=True)
        
        # 1. Check if broken link (404, 500 etc)
        if response.status_code >= 400:
            return "❌ Broken / Link Dead (Status Code: " + str(response.status_code) + ")"
        
        # 2. Check Amazon specific Out of Stock keywords in HTML
        page_source = response.text.lower()
        out_of_stock_keywords = ["currently unavailable", "out of stock", "temporary unavailable", "page not found"]
        
        for keyword in out_of_stock_keywords:
            if keyword in page_source:
                return "⚠️ Revenue Leak: Product Out of Stock / Page Dead"
                
        return "✅ Active & Safe"
    except Exception:
        return "❓ Timeout / Double Check Manually"

# Scanner Logic
if st.button("Scan Blog Now"):
    if not blog_url:
        st.warning("Kripya pehle ek URL enter karein.")
    else:
        with st.spinner("Aapka blog scan ho raha hai... Kripya thoda intezar karein."):
            found_links, error = extract_links(blog_url)
            
            if error:
                st.error(f"Kuch galti hui: {error}")
            elif not found_links:
                st.info("Is page par koi Amazon ya tracked affiliate links nahi mile.")
            else:
                st.success(f"Kul {len(found_links)} affiliate links mile! Unka status niche hai:")
                
                # Results Display Table
                for index, link in enumerate(found_links, 1):
                    status = check_link_status(link)
                    
                    # Formatting based on status
                    if "✅" in status:
                        st.success(f"**Link #{index}:** {link} — **{status}**")
                    elif "⚠️" in status:
                        st.warning(f"**Link #{index}:** {link} — **{status}**")
                    else:
                        st.error(f"**Link #{index}:** {link} — **{status}**")

