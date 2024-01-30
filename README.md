# Web Crawler Project README

## Introduction

This Python-based project provides a simple web crawler that can be used to explore and download web pages while respecting `robots.txt` rules and incorporating database functionality for storing crawled data.

NB: `robots.txt` are read by `urllib.robotparser`. The rules of this library are that everything that is not explicitely disallowed for an agent-user is allowed.

## Project Components

### 1. Web Crawler (`crawler.py`)

The `crawler.py` script defines the core functionality of the web crawler. It utilizes the `requests` library for making HTTP requests, `BeautifulSoup` for HTML parsing, and incorporates politeness by introducing delays between requests. The crawler follows a breadth-first strategy to explore and download web pages up to a specified limit.
The crawler updates the database for the link with the greatest age, every 3 links added to the database, if their age is greater than 5.

### 2. Database Manager (`crawler_db.py`)

The `crawler_db.py` script provides a simple SQLite database manager (`Crawler_db`) tailored to store information related to crawled web pages. It includes methods for creating a connection, initializing the database, saving data, and updating page ages.

### 3. Example Usage (`main.py`)

The `main.py` script demonstrates an example of using the web crawler and the database manager. It initializes the database, creates a crawler with a seed URL, and initiates the crawling process.

## Setup

1. **Dependencies:** Ensure that you have the necessary Python packages installed. You can install them using the following:

   ```bash
   pip install requests beautifulsoup4
   ```

2. **Database Setup:** The project uses SQLite as the database. The default database file is `pages_db.db`, and the relevant table is `downloaded_pages`.

3. **Run the Project:**

To run the web crawler, you can use the following command format:

```bash
python main.py "https://ensai.fr/" --max_urls 10
```

Replace "https://ensai.fr/" with your desired seed URL, and adjust the --max_urls parameter accordingly. This will initialize the database, create a crawler with a seed URL, and start the crawling process.
You might need to change the `python` command by `python3`.
You should be aware that crawling with the --max_urls parameter set to 100 takes approximately 20 minutes.

For more information on the parameters, you can use the following command:

```bash
python main.py --help
```

## Contributor

- Julia Toukal
