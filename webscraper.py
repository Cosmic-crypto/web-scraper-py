from bs4 import BeautifulSoup as _BeautifulSoup
from requests import get as _get, RequestException as _RequestException
from urllib.parse import quote_plus as _quote_plus
from sys import argv as _argv
from argparse import ArgumentParser as _ArgumentParser
from webbrowser import open_new_tab as _open_new_tab
from random import uniform as _uniform
from time import sleep as _sleep
from google import genai as _genai
from os import path as _path

#-------------------
# creates a function that gets the search term from either argparse, sys.argv, or user input
#-------------------
def get_search_term() -> str:
    parser = _ArgumentParser(description="Search scraper tool")
    parser.add_argument(
        "-s", "--search",
        type=str,
        help="Search term (e.g., -s python)"
    )

    # Parse known args (ignore others so script doesn’t crash if mixed)
    args, unknown = parser.parse_known_args()

    # If -s or --search was used
    if args.search:
        return args.search

    # Else if a plain arg was passed (e.g., python script.py hello)
    elif len(_argv) > 1:
        # skip the script name
        return " ".join(_argv[1:])

    # Else prompt interactively
    else:
        return input("Enter a search term: ").strip()


#-------------------
# gets the search term and ensures it’s not empty
#-------------------
search_ = get_search_term()

if search_.strip() == "":  # if the user has not provided a search term the user will be prompted to enter one

    # ensures that a search term is provided
    while True:
        try:
            search_ = input("Enter a search term: ")

            if search_.strip() != "":
                break
            else:
                print("Please enter a search term.")

        # allows the user to exit the loop
        except KeyboardInterrupt:  
            print("\nGoodbye!")
            break

# creates a function that encodes a search term for the urls
def encode_search(search_term: str) -> str:
    return _quote_plus(search_term)

#-------------------
# creates a function that gets the AI summary of the data
#-------------------
def AI_summary(data: str, API_KEY: str) -> str:
    client = _genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"summarize this: {data}"
    )
    return response.text

#-------------------
# defines the trusted domains
#-------------------
trusted_domains = [
    f"https://bbc.co.uk/search?q={encode_search(search_)}",
    f"https://wikipedia.org/wiki/{encode_search(search_)}",
    f"https://duckduckgo.com/search?q={encode_search(search_)}",
    f"https://edition.cnn.com/search?q={encode_search(search_)}",
    f"https://wolframalpha.com/input/?i={encode_search(search_)}"
]

#-------------------
# creates user agent
#-------------------
headers_ = {
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
    file.write(f"--search results for {search_}--\n")
    print(f"--search results for {search_}--")


#-------------------
# creates a function that scrapes the data from the trusted domains
#-------------------
def scrape(trusted_URLs: tuple[str, ...] | list[str], filename: str, times: int = 1, headers: dict = headers_, api_key: str) -> None:
    with open(filename, "a", encoding="utf-8") as file:
        # the loop allows you to scrape the data multiple times
        for _ in range(times):
            try:
                for url in trusted_URLs:
                    try:
                        response = _get(url, headers=headers)  # sends a GET request to the URL to get the HTML content
                        response.raise_for_status()  # raises an exception if the request was unsuccessful

                    except _RequestException:  # handles any exceptions that may occur
                        print(f"failed to fetch url {url}")
                        continue

                    soup = _BeautifulSoup(response.text, "html.parser")  # creates the html parser
                    page = soup.find_all(["span", "p", "h1", "h2", "h3"])  # defines all the data and tags to be scraped

                    # ensures that the data is found and else it will go to the next loop
                    if not page:
                        print(f"data could not be found from {url}")
                        continue

                    #-------------------
                    # writes the data to the file
                    # prints the data out to the console
                    #-------------------
                    file.write(f"\n--- Results from {url} ---\n\n")
                    print(f"--- Results from {url} ---")

                    for data in page:
                        text = data.get_text(strip=True)

                        # ensures that the text is not empty
                        if text:
                            file.write(f"{text}\n")
                            print(text)
                            
                            # Store AI summary to avoid double calls
                            summary = AI_summary(text, api_key)
                            print(summary)
                            file.write(f"\nAI Summary: {summary}\n")

                # writes and prints a message to let the user know that the data has been scraped
                file.write("\nAll data has been scraped from the provided URLs!\n")
                print("All data has been scraped from the provided URLs!")
                _sleep(_uniform(1, 7))

            except Exception as e:  # handles any exceptions that may occur 
                print(f"An error occurred: {e}")

#-------------------
# creates a function that opens the trusted domains in the default browser
#-------------------
def open_browser(trusted_URLs: tuple[str, ...] | list[str]):
    # loops through all the trusted domains and opens them in a new tab
    for url in trusted_URLs:
        _open_new_tab(url)


#-------------------
# runs the scraper and opens the browser (optional) if the script is not run as a module
#-------------------
if __name__ == "__main__":
    API_key = None

    if _path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "=" in line:
                        key, value = line.split("=", 1)
                        if key.strip().lower() == "genai_key":
                            API_key = value.strip()
    else:
        print("No .env file found")

    if not API_key:
        raise ValueError("API key not found! Please set GENAI_KEY in .env")
    
    print(f"trusted URLs: {trusted_domains}\n would you like to add any more domains?")
    choice = input("y/n: ").lower().strip()

    #-------------------
    # allows the user to add more domains
    #-------------------

    if choice == "y":
        try:
            while True:
                domain = input("Enter a URL: ").strip()

                if domain.lower() in ("break", "exit", "quit", "stop"):
                    break

                # saftey check to ensure the URL is valid
                response = _get(domain, headers=headers_) # picks the last url and checks it
                
                if response.status_code == 200 and domain not in trusted_domains: # makes sure the URL is valid and not already in the list
                    trusted_domains.append(domain)
                    print("URL added successfully.")
                else:
                    print("Failed to add URL.")

        # allows the user to exit the loop
        except KeyboardInterrupt:
            print("\nGoodbye!")

    trusted_domains = tuple(trusted_domains)

    scrape(trusted_domains, "scraped_results.txt", api_key=API_key)
    
    choice = input("Open browser? (y/n): ").lower().strip()
    
    if choice in ("yes", "y"):
        open_browser(trusted_domains)
