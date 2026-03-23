import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote


class RedditCollector:
    def __init__(self):
        self.base_url = "https://old.reddit.com/search?q="
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def build_query(self, query):
        query = query.strip()
        if not query:
            return "FC Barcelona"
        if "barcelona" in query.lower() or "barca" in query.lower() or "barça" in query.lower():
            return query
        return f"{query} FC Barcelona"

    def collect_posts(self, query="Barcelona", limit=10):
        results = []
        final_query = self.build_query(query)
        encoded_query = quote(final_query)
        url = f"{self.base_url}{encoded_query}&sort=relevance"

        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
        except requests.RequestException:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.find_all("div", class_="search-result")

        for post in posts:
            title = ""
            post_url = ""
            subreddit = ""
            text = ""
            date = None

            title_tag = post.find("a", class_="search-title")
            if title_tag:
                title = title_tag.get_text(strip=True)
                post_url = title_tag.get("href", "")

            subreddit_tag = post.find("a", class_="search-subreddit-link")
            if subreddit_tag:
                subreddit = subreddit_tag.get_text(strip=True)

            text_tag = post.find("div", class_="search-expando")
            if text_tag:
                text = text_tag.get_text(" ", strip=True)

            time_tag = post.find("time")
            if time_tag and time_tag.get("datetime"):
                date = time_tag.get("datetime")

            if title and post_url:
                results.append({
                    "team": "Barcelona",
                    "source": "reddit",
                    "query": final_query,
                    "title": title,
                    "text": text,
                    "author": "unknown",
                    "subreddit": subreddit if subreddit else "unknown",
                    "date": date,
                    "url": post_url,
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

            if len(results) >= limit:
                break

        return results