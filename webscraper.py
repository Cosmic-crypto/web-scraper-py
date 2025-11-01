from bs4 import BeautifulSoup
from requests import get, RequestException
from sys import argv

search = "".join(argv[1:])

if search.strip() == "": # if the user has not provided a search term the user will be prompted to enter one
    # ensures that a search term is provided

    while True:
        search = input("Enter a search term: ")

        if search.strip() != "":
            break
        else:
            print("Please enter a search term.")

trusted_domains = (
    f"https://bbc.co.uk/search?q={search}",
    f"https://wikipedia.org/wiki/{search}",
    f"https://duckduckgo.com/search?q={search}",
    f"https://edition.cnn.com/search?q={search}"
)

#-------------------
# creates user agent
#-------------------
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    )
}

#-------------------
# opens a file to write what search results are being scraped and where it's being scraped from
#-------------------
with open("scraped_results.txt", "w", encoding="utf-8") as file:
    file.write(f"--search results for {search}--")
    print(f"--search results for {search}--")

#-------------------
# scrapes the data from the trusted domains
#-------------------
try:
    for url in trusted_domains:
        try:
            response = get(url, headers=headers) # sends a GET request to the URL to get the HTML content
            response.raise_for_status() # raises an exception if the request was unsuccessful
        
        except RequestException as e: # handles any exceptions that may occur
            print(f"failed to fetch url {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser") # creates the html parser
        page = soup.find_all(["span", "p", "h1", "h2", "h3"]) # defines all the data and tags to be scraped

        # ensures that the data is found and else it will go to the next loop
        if not page:
            print(f"data could not be found from {url}")
            continue
        
        #-------------------
        # writes the data to the file
        #-------------------
        with open("scraped_results.txt", "a", encoding="utf-8") as file:
            file.write(f"\n--- Results from {url} ---\n\n")
            print(f"--- Results from {url} ---")

            for data in page:
                text = data.get_text(strip=True)

                # ensures that the text is not empty
                if text:
                    file.write(f"{text}\n")
                    print(text)
            file.write("All data has been scraped from URLS: {url}!") # writes a message to the file to let the user know that the data has been scraped
    print(f"All data has been scraped from URLS: {url}!") # prints a message to the console to let the user know that the data has been scraped

except Exception as e: # handles any exceptions that may occur
    print(f"An error occurred: {e}")
