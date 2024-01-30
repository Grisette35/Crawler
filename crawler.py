import requests
from bs4 import BeautifulSoup
import time
import socket
import urllib.robotparser
from urllib.parse import urlparse
from random import sample
from crawler_db import Crawler_db

class Crawler:
    def __init__(self, seed_url, conn, cursor, max_urls=100):
        """
        Initializes the Crawler object.

        Parameters:
        - seed_url (str or list of str): The starting URL or list of URLs.
        - conn: Database connection object.
        - cursor: Database cursor object.
        - max_urls (int, optional): Maximum number of URLs to crawl. Default is 100.
        """
        self.seed_url = seed_url
        self.max_urls = max_urls
        self.downloaded = set()
        self.frontier = [seed_url]
        self.content_current_url = None  # Avoid too many requests and respect politeness
        self.conn = conn
        self.cursor = cursor

    def crawl(self):
        """
        Initiates the crawling process until the frontier is empty or the maximum URLs are reached.
        """
        while self.frontier and len(self.downloaded) < self.max_urls:
            current_url = self.frontier.pop(0)
            if len(self.downloaded)%5==0:
                print(f"{len(self.downloaded)} URLs have been parsed")
            if current_url not in self.downloaded:
                self.downloaded.add(current_url)
                self.download_page(current_url)
                time.sleep(5)  # Attendre au moins 5s avant de download une autre page
                self.extract_links(current_url)

    def download_page(self, url):
        """
        Downloads the content of a web page and saves it to the database.

        Parameters:
        - url (str): The URL of the web page to download.
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                content = response.text
                self.content_current_url=content

                crawler_db=Crawler_db()

                if crawler_db.url_in_db(self.conn, self.cursor, url)==0:
                    crawler_db.save_to_database(self.conn, self.cursor, url, self.content_current_url)
                crawler_db.mettre_a_jour_age(self.conn, self.cursor, url)
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")

    def extract_links(self, url):
        """
        Extracts links from a web page, adds valid links to the frontier for further crawling.

        Parameters:
        - url (str): The URL of the web page to extract links from.
        """
        soup = BeautifulSoup(self.content_current_url, 'html.parser')

        try:
            rp = self.read_robots(url)
            links_sitemap = self.extract_links_sitemap(rp,url)
            links_found = soup.find_all('a', href=True)
            links_found = [link['href'] for link in links_found]
            links = list(set(links_sitemap+links_found))
                
            indice_to_draw=sample(range(len(links)), min(len(links),15)) # Exploration de 15 liens maximum par page
                
            for indice in indice_to_draw:
                print(links[indice])
                new_url = links[indice]
                if self.actual_url(new_url):
                    if self.reform_url_robots(new_url)!=self.reform_url_robots(url):
                        try:
                            rp=self.read_robots(new_url)
                    
                            if self.is_valid_url(rp, new_url) and (new_url not in self.downloaded):
                                self.frontier.append(new_url)
                                time.sleep(3)  # Respecte la politesse en attendant 3 secondes entre chaque appel
                        except Exception as e:
                            print(f"Error reading robots.txt of {url}: {str(e)}")
        except Exception as e:
            print(f"Error extracting links from {url}: {str(e)}")

    def actual_url(self, url):
        """
        Checks whether the provided URL is a valid web page URL.

        Parameters:
        - url (str): The URL to be validated.

        Returns:
        - bool: True if the URL is considered a valid web page URL, False otherwise.
        """
        parse_url = urlparse(url)
        if parse_url.scheme=='mailto' or parse_url.netloc=='' or parse_url.scheme=='':
            return False
        return True

    def reform_url_robots(self, url):
        """
        Forms the URL for the `robots.txt` file based on the given web page URL.

        Parameters:
        - url (str): The web page URL.

        Returns:
        - str: The URL for the `robots.txt` file corresponding to the given web page URL.
        """
        parse_url = urlparse(url)
        reform_base_url = parse_url.scheme+'://'+parse_url.netloc
        return reform_base_url+"/robots.txt"

    def read_robots(self, url):
        """
        Reads and parses the content of the `robots.txt` file for a given URL.

        Parameters:
        - url (str): The web page URL for which the `robots.txt` file needs to be read.

        Returns:
        - urllib.robotparser.RobotFileParser: An instance of the `RobotFileParser` class containing the parsed rules.
        """
        socket.setdefaulttimeout(5)  # To avoid that some rp.read() might be stuck
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(self.reform_url_robots(url))
        rp.read()
        return rp
    
    def extract_links_sitemap(self,rp, url):
        """
        Extracts links from the sitemap provided by the `robots.txt` rules.
        It recursively follows sitemap links that end with ".xml" to retrieve additional URLs.

        Parameters:
        - rp (urllib.robotparser.RobotFileParser): The parsed `robots.txt` rules for the given URL.
        - url (str): The web page URL.

        Returns:
        - list: A list of URLs extracted from the sitemap.
        """
        links=rp.site_maps()
        if links is None:
            return []
        for link in links:
            if link[-4:]==".xml":
                links.remove(link)
                links+=self.extract_links_sitemap(rp,link)
        return links
            
    def is_valid_url(self, rp, url):
        """
        Checks whether a given URL is allowed by the `robots.txt` rules.
        It uses the `can_fetch` method of the `RobotFileParser` class.

        Parameters:
        - rp (urllib.robotparser.RobotFileParser): The parsed `robots.txt` rules for the given URL.
        - url (str): The URL to be checked.

        Returns:
        - bool: True if the URL is allowed, False otherwise.
        """
        return rp.can_fetch("*", url)

    def write_downloaded(self):
        """
        Writes the downloaded URLs to 'crawled_webpages.txt' in the current directory.

        Parameters:
        - None

        Returns:
        - None
        """
        all_urls=""
        for url in list(self.downloaded):
            all_urls+=url+'\n'
        with open('crawled_webpages.txt', 'a') as file:
                    file.write(all_urls)
