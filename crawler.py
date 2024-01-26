import requests
from bs4 import BeautifulSoup
import time
import urllib.robotparser
from urllib.parse import urlparse
from random import sample

class Crawler:
    def __init__(self, seed_url, max_urls=50):
        self.seed_url = seed_url
        self.max_urls=max_urls
        self.downloaded=set()
        self.frontier = seed_url

    def crawl(self):
        while self.frontier and len(self.downloaded) < self.max_urls:
            current_url = self.frontier.pop(0)
            if current_url not in self.downloaded:
                self.downloaded.add(current_url)
                self.download_page(current_url)
                self.extract_links(current_url)

    def download_page(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                #content = response.text
                with open('crawled_webpages.txt', 'a') as file:
                    file.write(url + '\n')
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")

    def extract_links(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                content = response.text
                soup = BeautifulSoup(content, 'html.parser')
                links_sitemap = self.extract_links_sitemap(url)
                links_found = soup.find_all('a', href=True)
                links = list(set(links_sitemap+links_found))
                indice_to_draw=sample(range(1, len(links)), 5)
                for indice in indice_to_draw: # Exploration de 5 liens maximum par page
                    new_url = links[indice]['href']
                    print(new_url)
                    if self.is_valid_url(new_url) and (new_url not in self.downloaded):
                        self.frontier.append(new_url)
                        time.sleep(3)  # Respecte la politesse en attendant 3 secondes entre chaque appel
        except Exception as e:
            print(f"Error extracting links from {url}: {str(e)}")

    def read_robots(self, url):
        parse_url = urlparse(url)
        reform_base_url = parse_url.scheme+'://'+parse_url.netloc
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(reform_base_url+"/robots.txt")
        rp.read()
        return rp
    
    def extract_links_sitemap(self, url):
        rp = self.read_robots(url)
        links=rp.site_maps()
        for link in links:
            if link[-4:]==".xml":
                links.remove(link)
                links+=self.extract_links_sitemap(link)
        return links
            
    def is_valid_url(self, url):
        rp = self.read_robots(url)
        return rp.can_fetch("*", url)

# Exemple d'utilisation
if __name__ == "__main__":
    #starting_url = "https://ensai.fr/"
    crawler = Crawler(["https://ensai.fr/"])
    crawler.crawl()
    #print(crawler.is_valid_url("https://ensai.fr/"))
    #print(sample(range(0, 5), 3))
    #crawler.extract_links("https://ensai.fr/")
