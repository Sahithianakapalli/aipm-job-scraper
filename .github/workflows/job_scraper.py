import os
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

# Target job boards or specific company pages you want to monitor
TARGET_URLS = [
    "https://news.ycombinator.com/jobs", 
]

def scrape_jobs():
    print("Starting AI Product Manager job scraper...")

    for url in TARGET_URLS:
        try:
            response = app.scrape(url, formats=['markdown'])
            content = response.get('markdown', '')

            keywords = ["ai product manager", "artificial intelligence product", "technical product manager", "tpm"]
            found_matches = [kw for kw in keywords if kw in content.lower()]

            if found_matches:
                print(f"[MATCH FOUND] Relevant roles found on: {url}")
            else:
                print(f"No direct matches on: {url}")

        except Exception as e:
            print(f"Error scraping {url}: {e}")

if __name__ == "__main__":
    scrape_jobs()
