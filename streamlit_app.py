# streamlit_app.py

import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_alibaba_results(product):
    search_query = product.replace(" ", "+")
    url = f"https://www.alibaba.com/trade/search?SearchText={search_query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    product_cards = soup.find_all("div", class_="organic-gallery-title")

    results = []
    for card in product_cards[:5]:
        try:
            title = card.get_text(strip=True)
            link = card.find("a")["href"]
            if not link.startswith("http"):
                link = "https:" + link
            results.append((title, link))
        except:
            continue
    return results

st.set_page_config(page_title="IRAM Sourcing Assistant", layout="centered")

st.title("🤖 IRAM Sourcing Assistant")
st.markdown("Search for heavy equipment like hydraulic pumps directly from Alibaba")

product = st.text_input("Enter Product Name", value="CAT 320D hydraulic pump")

if st.button("Search"):
    with st.spinner("Searching Alibaba..."):
        results = fetch_alibaba_results(product)
        if results:
            st.success("Top Listings Found:")
            for i, (title, link) in enumerate(results, 1):
                st.markdown(f"**{i}. {title}**\n
[🔗 View Product]({link})")
        else:
            st.error("No results found or blocked by Alibaba. Try simpler keywords.")
