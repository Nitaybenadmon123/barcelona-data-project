import tkinter as tk
from tkinter import scrolledtext
import webbrowser

from collectors.news_collector import NewsCollector
from collectors.second_news_collector import SecondNewsCollector
from database.mongo_manager import MongoManager


class BarcelonaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Barcelona Data Collector")
        self.root.geometry("1100x720")
        self.root.configure(bg="#0A2342")

        self.news_collector = NewsCollector()
        self.second_news_collector = SecondNewsCollector()
        self.mongo = MongoManager()

        self.primary_bg = "#0A2342"
        self.secondary_bg = "#A50044"
        self.accent = "#FDB913"
        self.text_dark = "#1A1A1A"
        self.text_light = "#FFFFFF"
        self.button_bg = "#A50044"
        self.button_fg = "#FFFFFF"
        self.output_bg = "#FFFFFF"

        self.link_counter = 0

        self.create_widgets()

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg=self.primary_bg)
        header_frame.pack(fill="x", pady=(10, 0))

        title_label = tk.Label(
            header_frame,
            text="🔵🔴 Barcelona Data Collector",
            font=("Arial", 24, "bold"),
            bg=self.primary_bg,
            fg=self.accent
        )
        title_label.pack(pady=10)

        subtitle_label = tk.Label(
            header_frame,
            text="FC Barcelona Official News + BBC",
            font=("Arial", 11),
            bg=self.primary_bg,
            fg=self.text_light
        )
        subtitle_label.pack(pady=(0, 10))

        search_frame = tk.Frame(self.root, bg=self.primary_bg)
        search_frame.pack(fill="x", padx=20, pady=10)

        search_label = tk.Label(
            search_frame,
            text="Search keyword:",
            font=("Arial", 12, "bold"),
            bg=self.primary_bg,
            fg=self.text_light
        )
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 12),
            width=30,
            bd=2,
            relief="groove"
        )
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_entry.insert(0, "Barcelona")
        self.search_entry.bind("<Return>", lambda event: self.search_all())

        search_button = tk.Button(
            search_frame,
            text="Search",
            command=self.search_all,
            width=12,
            height=1,
            bg=self.accent,
            fg=self.text_dark,
            font=("Arial", 10, "bold"),
            relief="raised",
            bd=2,
            cursor="hand2"
        )
        search_button.grid(row=0, column=2, padx=10, pady=5)

        button_frame = tk.Frame(self.root, bg=self.primary_bg)
        button_frame.pack(fill="x", padx=20, pady=10)

        self.create_button(button_frame, "Collect Barça News", self.collect_news, 0, 0)
        self.create_button(button_frame, "Collect BBC News", self.collect_bbc_news, 0, 1)
        self.create_button(button_frame, "Collect Both", self.collect_both, 0, 2)
        self.create_button(button_frame, "Show Saved Data", self.show_saved_data, 0, 3)
        self.create_button(button_frame, "Show Only Barça News", self.show_only_news, 0, 4)
        self.create_button(button_frame, "Show Only BBC", self.show_only_bbc, 0, 5)

        bottom_button_frame = tk.Frame(self.root, bg=self.primary_bg)
        bottom_button_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.create_button(bottom_button_frame, "Clear Screen", self.clear_output, 0, 0)
        self.create_button(bottom_button_frame, "Show Stats", self.show_stats, 0, 1)

        output_frame = tk.Frame(self.root, bg=self.secondary_bg, bd=3, relief="ridge")
        output_frame.pack(fill="both", expand=True, padx=20, pady=15)

        output_title = tk.Label(
            output_frame,
            text="Output Console",
            font=("Arial", 13, "bold"),
            bg=self.secondary_bg,
            fg=self.text_light
        )
        output_title.pack(anchor="w", padx=10, pady=8)

        self.output_area = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            width=120,
            height=30,
            font=("Consolas", 10),
            bg=self.output_bg,
            fg=self.text_dark,
            insertbackground=self.text_dark,
            bd=2,
            relief="sunken"
        )
        self.output_area.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.write_output("Welcome to Barcelona Data Collector")
        self.write_output("Type a keyword and press Search or Enter.\n")

    def create_button(self, parent, text, command, row, column):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            width=20,
            height=2,
            bg=self.button_bg,
            fg=self.button_fg,
            activebackground=self.accent,
            activeforeground=self.text_dark,
            font=("Arial", 10, "bold"),
            relief="raised",
            bd=2,
            cursor="hand2"
        )
        button.grid(row=row, column=column, padx=6, pady=6)

    def get_query(self):
        query = self.search_entry.get().strip()
        return query if query else "Barcelona"

    def write_output(self, text=""):
        self.output_area.insert(tk.END, text + "\n")
        self.output_area.see(tk.END)

    def write_clickable_link(self, text, url):
        if not url:
            self.write_output(text)
            return

        self.link_counter += 1
        tag_name = f"link_{self.link_counter}"

        start_index = self.output_area.index(tk.INSERT)
        self.output_area.insert(tk.END, text + "\n")
        end_index = self.output_area.index(tk.INSERT)

        self.output_area.tag_add(tag_name, start_index, end_index)
        self.output_area.tag_config(tag_name, foreground="blue", underline=True)

        self.output_area.tag_bind(
            tag_name,
            "<Button-1>",
            lambda event, link=url: webbrowser.open_new_tab(link)
        )
        self.output_area.tag_bind(
            tag_name,
            "<Enter>",
            lambda event: self.output_area.config(cursor="hand2")
        )
        self.output_area.tag_bind(
            tag_name,
            "<Leave>",
            lambda event: self.output_area.config(cursor="xterm")
        )

        self.output_area.see(tk.END)

    def clear_output(self):
        self.output_area.delete(1.0, tk.END)

    def search_all(self):
        self.clear_output()
        query = self.get_query()
        self.write_output(f"Searching for: {query}\n")
        self.collect_news()
        self.collect_bbc_news()

    def collect_news(self):
        query = self.get_query()
        self.write_output(f"Collecting official Barça news for: {query}")

        articles = self.news_collector.collect_latest_news(limit=10, query=query)

        if not articles:
            self.write_output("No matching Barça official news found.")
            self.write_output("-" * 80)
            return

        inserted = self.mongo.save_items(articles)

        self.write_output(f"Collected {len(articles)} Barça official news articles.")
        self.write_output(f"Inserted {inserted} new items into MongoDB.\n")

        for article in articles:
            self.write_output(f"[BARÇA NEWS] {article.get('title')}")
            self.write_clickable_link("🔗 Open article", article.get("url"))
            self.write_output("-" * 80)

    def collect_bbc_news(self):
        query = self.get_query()
        self.write_output(f"Collecting BBC news for: {query}")

        articles = self.second_news_collector.collect_news(query=query, limit=10)

        if not articles:
            self.write_output("No matching BBC news found.")
            self.write_output("-" * 80)
            return

        inserted = self.mongo.save_items(articles)

        self.write_output(f"Collected {len(articles)} BBC news articles.")
        self.write_output(f"Inserted {inserted} new BBC items into MongoDB.\n")

        for article in articles:
            self.write_output(f"[BBC] {article.get('title')}")
            self.write_clickable_link("🔗 Open BBC article", article.get("url"))
            self.write_output("-" * 80)

    def collect_both(self):
        query = self.get_query()
        self.write_output(f"Collecting from both sources for: {query}\n")

        articles_1 = self.news_collector.collect_latest_news(limit=10, query=query)
        articles_2 = self.second_news_collector.collect_news(query=query, limit=10)

        all_items = articles_1 + articles_2

        if not all_items:
            self.write_output("No results found in both sources.")
            self.write_output("-" * 80)
            return

        inserted = self.mongo.save_items(all_items)

        self.write_output(f"Collected {len(articles_1)} FC Barcelona official articles.")
        self.write_output(f"Collected {len(articles_2)} BBC news articles.")
        self.write_output(f"Inserted {inserted} new total items into MongoDB.\n")

    def show_saved_data(self):
        self.write_output("Showing saved data from MongoDB...\n")
        items = self.mongo.get_all_items(limit=20)

        if not items:
            self.write_output("No saved data found.")
            self.write_output("-" * 80)
            return

        for item in items:
            self.write_output(f"Title: {item.get('title')}")
            self.write_output(f"Source: {item.get('source')}")
            self.write_clickable_link("🔗 Open item", item.get("url"))
            self.write_output("-" * 80)

    def show_only_news(self):
        self.write_output("Showing only FC Barcelona official news...\n")
        items = self.mongo.get_items_by_source("news", limit=20)

        if not items:
            self.write_output("No Barça official news found in database.")
            self.write_output("-" * 80)
            return

        for item in items:
            self.write_output(f"[BARÇA NEWS] {item.get('title')}")
            self.write_clickable_link("🔗 Open article", item.get("url"))
            self.write_output("-" * 80)

    def show_only_bbc(self):
        self.write_output("Showing only BBC news...\n")
        items = self.mongo.get_items_by_source("bbc_news", limit=20)

        if not items:
            self.write_output("No BBC news found in database.")
            self.write_output("-" * 80)
            return

        for item in items:
            self.write_output(f"[BBC] {item.get('title')}")
            self.write_clickable_link("🔗 Open BBC article", item.get("url"))
            self.write_output("-" * 80)

    def show_stats(self):
        total = self.mongo.count_items()
        barca_news_count = len(self.mongo.get_items_by_source("news", limit=1000))
        bbc_count = len(self.mongo.get_items_by_source("bbc_news", limit=1000))

        self.write_output("Database Statistics")
        self.write_output(f"Total items: {total}")
        self.write_output(f"FC Barcelona official news items: {barca_news_count}")
        self.write_output(f"BBC news items: {bbc_count}")
        self.write_output("-" * 80)


if __name__ == "__main__":
    root = tk.Tk()
    app = BarcelonaApp(root)
    root.mainloop()