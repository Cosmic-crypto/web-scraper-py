from bs4 import BeautifulSoup
import requests
from sys import argv

search = "".join(argv[1:])

if search.strip() == "":
    search = input("Enter a search term: ")

trusted_domains = (
    f"https://bbc.co.uk/search?q={search}",
    f"https://wikipedia.org/wiki/{search}",
    f"https://duckduckgo.com/search?q={search}",
    f"https://edition.cnn.com/search?q={search}"
)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    )
}

with open("scraped_results.txt", "w", encoding="utf-8") as file:
    file.write(f"--search results for {search}--")
    print(f"--search results for {search}--")

try:
    for url in trusted_domains:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        
        except requests.RequestException as e:
            print(f"failed to fetch url {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        page = soup.find_all(["span", "p", "h1", "h2", "h3"])

        if not page:
            print(f"data could not be found from {url}")
            continue
        with open("scraped_results.txt", "a", encoding="utf-8") as file:
            file.write(f"\n--- Results from {url} ---\n\n")
            print(f"--- Results from {url} ---")

            for data in page:
                text = data.get_text(strip=True)

                if text:
                    file.write(f"{text}\n")
                    print(text)

    print(f"All data has been scraped from URLS: {url}!")

except Exception as e:
    print(f"An error occurred: {e}")
