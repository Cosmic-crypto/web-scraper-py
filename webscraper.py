import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse, parse_qs

trusted_domains = (
    "github.com",
    "reddit.com",
    "stackoverflow.com",
    "wikipedia.org",
    "bbc.co.uk",
    "geeksforgeeks.org",
)

search = input("Enter a search term: ").strip()
url = f"https://duckduckgo.com/html/?q={search}"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    )
}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Extract all hrefs
raw_links = [a["href"] for a in soup.find_all("a", href=True)]

decoded_links = []
for href in raw_links:
    if "/l/?" in href and "uddg=" in href:
        # DuckDuckGo wraps external links like: /l/?uddg=<encoded target>
        query = parse_qs(urlparse(href).query)
        decoded = unquote(query.get("uddg", [""])[0])
        decoded_links.append(decoded)
    elif href.startswith("http"):
        decoded_links.append(href)

# Filter only trusted ones
trusted_links = [
    link for link in decoded_links
    if any(domain in link for domain in trusted_domains)
]

if not trusted_links:
    print("No trusted links found.")
else:
    print(f"Found {len(trusted_links)} trusted links:")
    for link in trusted_links:
        print(" -", link)

# Scrape each trusted link
with open("scraped_results.txt", "w", encoding="utf-8") as file:
    for link in trusted_links:
        print(f"\nScraping {link}...\n")
        try:
            page_response = requests.get(link, headers=headers, timeout=10)
            page_response.raise_for_status()

            page_soup = BeautifulSoup(page_response.text, "html.parser")
            elements = page_soup.find_all(["p", "h1", "h2", "h3"])

            for el in elements:
                text = el.get_text(strip=True)
                if text:
                    file.write(f"{text}\n\n")
                    print(text)

        except Exception as e:
            print(f"Failed to scrape {link}: {e}")
