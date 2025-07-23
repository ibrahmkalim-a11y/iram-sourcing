# streamlit_app.py

import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def search_alibaba(product):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.alibaba.com/")
    time.sleep(3)

    search_box = driver.find_element(By.NAME, "SearchText")
    search_box.send_keys(product)
    search_box.submit()
    time.sleep(5)

    listings = driver.find_elements(By.CSS_SELECTOR, "div.organic-gallery-title")
    results = []
    for i in range(min(5, len(listings))):
        try:
            title = listings[i].text.strip()
            link = listings[i].find_element(By.TAG_NAME, "a").get_attribute("href")
            results.append((title, link))
        except:
            continue

    driver.quit()
    return results

st.set_page_config(page_title="IRAM Sourcing Assistant", layout="centered")

st.title("🤖 IRAM Sourcing Assistant")
st.markdown("Search for equipment like hydraulic pumps directly from Alibaba")

product = st.text_input("Enter Product Name", value="CAT 320D hydraulic pump")

if st.button("Search"):
    with st.spinner("Searching Alibaba..."):
        results = search_alibaba(product)
        if results:
            st.success("Top Listings Found:")
            for i, (title, link) in enumerate(results, 1):
                st.markdown(f"**{i}. {title}**\n\n[View Product]({link})")
        else:
            st.error("No results found. Try again.")
