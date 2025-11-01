🕵️ Web Multi-Site Scraper

A lightweight Python script that scrapes text content (headings, paragraphs, and spans) from a few trusted news and information domains — including BBC, Wikipedia, DuckDuckGo, and CNN — based on a user-provided search term.

📦 Features

✅ Scrapes multiple trusted domains automatically
✅ Works with command-line arguments (argv) or interactive input
✅ Collects all text data into a single file (scraped_results.txt)
✅ Handles connection errors gracefully
✅ Uses a modern browser-like user agent header

🧰 Requirements

Make sure you have Python 3.8+ installed.
Then install the required libraries:

```bash
pip install requests beautifulsoup4
```

🚀 Usage
Option 1: Pass a search term as a command-line argument
```
python webscraper.py python
```

Option 2: Run it without arguments (it will prompt you)
```
python webscraper.py
```

Then type your search term when asked:

```
Enter a search term: python
```

⚙️ How It Works

The script takes a search term from the command line or user input.

It constructs four URLs:

https://bbc.co.uk/search?q=TERM

https://wikipedia.org/wiki/TERM

https://duckduckgo.com/search?q=TERM

https://edition.cnn.com/search?q=TERM

It fetches each page using the requests library and parses it with BeautifulSoup.

It extracts visible text from `<span>`, `<p>`, `<h1>`, `<h2>`, and `<h3>` tags.

It saves all text content into scraped_results.txt and prints it to the terminal.

🗂️ Output

All results are saved in:

scraped_results.txt


Each domain’s section is clearly separated:

```
--- Results from https://bbc.co.uk/search?q=python ---


Python is a programming language...
BBC News - Technology - Python in AI...
```

🧱 Example Run
```
python webscraper.py AI


🖨️ Output:

--search results for AI--
--- Results from https://bbc.co.uk/search?q=AI ---
BBC News - AI is transforming business...
--- Results from https://wikipedia.org/wiki/AI ---
Artificial intelligence (AI) is...
```

The same content is also stored in scraped_results.txt.

⚠️ Notes

Some sites (like DuckDuckGo or CNN) may restrict automated scraping.

If you get empty results, the site may require a more advanced approach (like Selenium).

Always check a website’s robots.txt before scraping.

feel free to edit this to anypoint
