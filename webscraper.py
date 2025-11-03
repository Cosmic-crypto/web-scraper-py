from bs4 import BeautifulSoup
from requests import get, RequestException
from sys import argv
from argparse import ArgumentParser


#-------------------
# creates a function that gets the search term from either argparse, sys.argv, or user input
#-------------------
def get_search_term() -> str:
    parser = ArgumentParser(description="Search scraper tool")
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
    elif len(argv) > 1:
        # skip the script name
        return " ".join(argv[1:])

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
        search_ = input("Enter a search term: ")

        if search_.strip() != "":
            break
        else:
            print("Please enter a search term.")


#-------------------
# defines the trusted domains
#-------------------
trusted_domains = [
    f"https://bbc.co.uk/search?q={search_}",
    f"https://wikipedia.org/wiki/{search_}",
    f"https://duckduckgo.com/search?q={search_}",
    f"https://edition.cnn.com/search?q={search_}"
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

print(f"trusted_URLs: {trusted_URLs} would you like to add any more domains?")
choice = input("y/n: ").lower().strip()

#-------------------
# allows the user to add more domains
#-------------------

if choice == "y":
    while True:
        try:
            while True:
                domain = input("Enter a URL: ").strip()

                if domain.lower() in ("break", "exit", "quit", "stop"):
                    break

                # saftey check to ensure the URL is valid
                response = get(domain, headers=headers) # picks the last url and checks it
                
                if response.status_code == 200 and domain not in trusted_domains: # makes sure the URL is valid and not already in the list
                    trusted_domains.append(domain)
                    print("URL added successfully.")
                else:
                    print("Failed to add URL.")

        # allows the user to exit the loop
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

#-------------------
# opens a file to write what search results are being scraped and where it's being scraped from
#-------------------
with open("scraped_results.txt", "w", encoding="utf-8") as file:
    file.write(f"--search results for {search_}--\n")
    print(f"--search results for {search_}--")


#-------------------
# creates a function that scrapes the data from the trusted domains
#-------------------
def scrape(trusted_URLs: tuple[str, ...] | list[str], headers: dict, filename: str, times: int = 1) -> None:
    for time in range(times):
        try:
            for url in trusted_URLs:
                try:
                    response = get(url, headers=headers)  # sends a GET request to the URL to get the HTML content
                    response.raise_for_status()  # raises an exception if the request was unsuccessful

                except RequestException as e:  # handles any exceptions that may occur
                    print(f"failed to fetch url {url}: {e}")
                    continue

                soup = BeautifulSoup(response.text, "html.parser")  # creates the html parser
                page = soup.find_all(["span", "p", "h1", "h2", "h3"])  # defines all the data and tags to be scraped

                # ensures that the data is found and else it will go to the next loop
                if not page:
                    print(f"data could not be found from {url}")
                    continue

                #-------------------
                # writes the data to the file
                # prints the data out to the console
                #-------------------
                with open(filename, "a", encoding="utf-8") as file:
                    file.write(f"\n--- Results from {url} ---\n\n")
                    print(f"--- Results from {url} ---")

                    for data in page:
                        text = data.get_text(strip=True)

                        # ensures that the text is not empty
                        if text:
                            file.write(f"{text}\n")
                            print(text)

            # writes and prints a message to let the user know that the data has been scraped
            with open(filename, "a", encoding="utf-8") as file:
                file.write("\nAll data has been scraped from the provided URLs!\n")
            print("All data has been scraped from the provided URLs!")

        except Exception as e:  # handles any exceptions that may occur
            print(f"An error occurred: {e}")



#-------------------
# runs the scraper if the script is not run as a module
#-------------------
if __name__ == "__main__":
    scrape(trusted_domains, headers_, "scraped_results.txt")
