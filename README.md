# Web Crawler Project README

## Introduction

This Python-based project provides a simple web crawler that can be used to explore and download web pages while respecting `robots.txt` rules and incorporating database functionality for storing crawled data.

## Project Components

### 1. Web Crawler (`crawler.py`)

The `crawler.py` script defines the core functionality of the web crawler. It utilizes the `requests` library for making HTTP requests, `BeautifulSoup` for HTML parsing, and incorporates politeness by introducing delays between requests. The crawler follows a breadth-first strategy to explore and download web pages up to a specified limit.

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

3. **Run the Example:**

   ```bash
   python main.py
   ```

   This will initialize the database, create a crawler with a seed URL, and start the crawling process.

## Customization

Feel free to customize the project based on your specific requirements:

- Adjust the seed URL, maximum URLs to crawl, and other parameters in `main.py`.
- Modify database-related parameters or use a different database system in `crawler_db.py`.
- Tune the crawler's politeness settings, delay durations, or add additional functionality in `crawler.py`.

## Notes

- Ensure compliance with web scraping policies and respect the terms of service of the websites being crawled.
- Adapt the code to handle different website structures, handle exceptions, and improve error handling.

## Contributor

- Julia Toukal
