import requests
from bs4 import BeautifulSoup
from datetime import datetime


class NewsCollector:
    def __init__(self):
        self.base_url = "https://www.fcbarcelona.com"
        self.news_url = "https://www.fcbarcelona.com/en/news/"
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def clean_title(self, title):
        if not title:
            return ""

        garbage_parts = [
            "label.aria.barcelonabadge",
            "label.aria.clock"
        ]

        for part in garbage_parts:
            title = title.replace(part, "")

        return " ".join(title.split()).strip()

    def collect_latest_news(self, limit=10, query="Barcelona"):
        results = []

        response = requests.get(self.news_url, headers=self.headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)

        seen = set()
        query_lower = query.lower().strip()

        for link in links:
            href = link.get("href", "")
            raw_title = link.get_text(" ", strip=True)
            title = self.clean_title(raw_title)

            if not href or not title:
                continue

            if "/news/" not in href:
                continue

            if href.startswith("/"):
                full_url = self.base_url + href
            elif href.startswith("http"):
                full_url = href
            else:
                continue

            if full_url in seen:
                continue

            if query_lower and query_lower not in title.lower():
                continue

            seen.add(full_url)

            results.append({
                "team": "Barcelona",
                "source": "news",
                "query": query,
                "title": title,
                "text": "",
                "date": None,
                "author": "FC Barcelona Official Website",
                "url": full_url,
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            if len(results) >= limit:
                break

        return results