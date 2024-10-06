# pip install streamlit requests bs4
import os
import time
import re

from bs4 import BeautifulSoup
import streamlit as st
import requests
from urllib.parse import urljoin


OUTPUT_FOLDER = "output"
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# 再帰的なクロール関数
def crawl(url, max_depth, current_depth=0, visited=None, progress=None, total_links=None, url_pattern=None):
    if visited is None:
        visited = set()
    if progress is None:
        progress = st.empty()
    if total_links is None:
        total_links = [1]

    if current_depth > max_depth:
        return {}

    if url in visited:
        return {}

    visited.add(url)
    links_info = {}
    links_info[url] = ""

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links_info[url] = re.sub(r"\n{3,}", "\n\n", soup.get_text(separator='\n', strip=True))

        links = soup.find_all('a', href=True)
        filtered_links = [link for link in links if url_pattern is None or re.search(url_pattern, urljoin(url, link['href']))]
        if max_depth > current_depth:
            total_links[0] += len(filtered_links)

        for link in filtered_links:
            abs_link = urljoin(url, link['href'])
            if abs_link not in visited:
                progress.text(f"Crawling... {len(visited)} of approximately {total_links[0]} links processed. Currently processing: {abs_link}")
                time.sleep(0.5)  # サーバーに負荷をかけないようにウェイトを追加
                child_links_info = crawl(abs_link, max_depth, current_depth + 1, visited, progress, total_links, url_pattern)
                links_info.update(child_links_info)

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to retrieve URL {url}: {e}")

    return links_info

# Streamlit UI
def main():
    st.set_page_config(layout="wide")
    st.title("Recursive Web Crawler")
    url = st.text_input("Enter the starting URL:", "https://example.com")
    max_depth = st.slider("Select the maximum depth for crawling:", 1, 5, 2)
    url_pattern = st.text_input("Enter a regex pattern to filter URLs (optional):", "")
    file_name = st.text_input("Enter the file name for the report:", "report.txt")
    crawl_in_progress = st.empty()

    if crawl_in_progress.button("Start Crawling", disabled=False, key='start_crawl_button'):
        crawl_in_progress.button("Start Crawling", disabled=True, key='start_crawl_button_disabled')
        st.write("Crawling... this might take a while.")
        progress = st.empty()
        links_info = crawl(url, max_depth, url_pattern=url_pattern if url_pattern else None, progress=progress)
        progress.write("Crawling completed.")
        crawl_in_progress.button("Start Crawling", disabled=False, key='start_crawl_button_reset')

        if links_info:
            selected_contents = []
            for link in links_info:
                selected_contents.append(f"----------\nURL: {link}\nContent: {links_info[link]}\n----------")

            report_content = "\n\n".join(selected_contents)
            with open(f"{OUTPUT_FOLDER}/{file_name}", "w", encoding="utf-8") as file:
                file.write(report_content)
            st.success(f"Report saved as {file_name}")
if __name__ == "__main__":
    main()