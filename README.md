DuckDuckGo Trusted Link Scraper
Overview

This Python script searches DuckDuckGo for a user-specified query, identifies links from a predefined list of trusted domains, and scrapes textual content (headings and paragraphs) from those pages. All scraped data is saved to a text file for further use.

Features

* Accepts user input for search queries.

* Uses DuckDuckGo search results to locate relevant links.

* Filters links to only include trusted domains:

  * GitHub

  * Reddit

  * Stack Overflow

  * Wikipedia

  * BBC

  * GeeksforGeeks
   (feel free to change this!)

Automatically decodes DuckDuckGo’s redirect URLs.

Scrapes headings (```h1```, ```h2```, ```h3```) and paragraph (```p```) text.

Saves the scraped content to scraped_results.txt.

Prints progress and scraped content to the console.

Requirements

Python 3.7+

Required Python packages:

``` bash
pip install requests beautifulsoup4
```

Usage

Clone or download the repository.

Run the script:

``` bash
python scraper.py
```
Example run:
```
Enter your search term when prompted:

Enter a search term: web scraper
```

The script will display the trusted links found and scrape their content.

All scraped text will be saved to scraped_results.txt in the current directory.

How It Works:

1 DuckDuckGo Search

* The script performs a DuckDuckGo search using the user-provided query.

* It sends a request with a custom User-Agent to simulate a real browser.

2 Link Extraction & Decoding

* Extracts all <a> elements from the search results.

* Decodes DuckDuckGo’s redirect links (/l/?uddg=...) to get actual URLs.

3 Trusted Domain Filtering

* Checks each decoded link against a list of trusted domains.

* Only links matching trusted domains are scraped.

4 Content Scraping

* Fetches each trusted page.

* Extracts text from headings (```h1```, ```h2```, ```h3```) and paragraphs (```p```).

* Saves the content to a text file and prints it to the console.

Notes

Make sure to respect each website’s terms of service.

Use the script responsibly to avoid overloading servers.

The script works best with static content; dynamic JavaScript content may not be fully captured.

License

This project is provided for educational purposes. No redistribution of scraped content is allowed without permission from the respective website.

feel free to edit this in any way you feel suit and give me feedback, also i'd say 85% code is me 15% is chatgpt, so credits: chatgpt!
