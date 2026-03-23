import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote


class SecondNewsCollector:
    def __init__(self):
        self.base_search_url = "https://www.bbc.co.uk/search?q="
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def collect_news(self, query="Barcelona", limit=10):
        results = []

        final_query = f"{query} FC Barcelona"
        url = self.base_search_url + quote(final_query)

        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
        except requests.RequestException:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)

        seen = set()

        for link in links:
            href = link.get("href", "")
            title = link.get_text(" ", strip=True)

            if not href or not title:
                continue

            if "bbc" not in href and not href.startswith("/"):
                continue

            if href.startswith("/"):
                full_url = "https://www.bbc.co.uk" + href
            else:
                full_url = href

            if full_url in seen:
                continue

            title_lower = title.lower()
            query_lower = query.lower()

            if query_lower not in title_lower and "barcelona" not in title_lower:
                continue

            seen.add(full_url)

            results.append({
                "team": "Barcelona",
                "source": "bbc_news",
                "query": query,
                "title": title,
                "text": "",
                "date": None,
                "author": "BBC Sport",
                "url": full_url,
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            if len(results) >= limit:
                break

        return results