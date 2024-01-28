import requests
from bs4 import BeautifulSoup
import time
import urllib.robotparser
from urllib.parse import urlparse
from random import sample
from crawler_db import Crawler_db

class Crawler:
    def __init__(self, seed_url, conn, cursor, max_urls=50):
        self.seed_url = seed_url
        self.max_urls = max_urls
        self.downloaded = set()
        self.frontier = seed_url
        self.content_current_url = None  # Pour éviter un trop grand nombre de requêtes à la page
        self.conn = conn
        self.cursor = cursor

    def crawl(self):
        while self.frontier and len(self.downloaded) < self.max_urls:
            current_url = self.frontier.pop(0)
            #print(current_url)
            #print(self.downloaded)
            if current_url not in self.downloaded:
                self.downloaded.add(current_url)
                self.download_page(current_url)
                time.sleep(5)  # Attendre au moins 5s avant de download une autre page
                self.extract_links(current_url)

    def download_page(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                content = response.text
                self.content_current_url=content

                crawler_db=Crawler_db()

                if crawler_db.url_in_db(self.conn, self.cursor, url)==0:
                    crawler_db.save_to_database(self.conn, self.cursor, url, self.content_current_url)
                crawler_db.mettre_a_jour_age(self.conn, self.cursor, url)
                with open('crawled_webpages.txt', 'a') as file:
                    file.write(url + '\n')
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")

    def extract_links(self, url):
        #try:
            #response = requests.get(url)
            #if response.status_code == 200:
                #content = response.text
        soup = BeautifulSoup(self.content_current_url, 'html.parser')
                
        rp = self.read_robots(url)
        links_sitemap = self.extract_links_sitemap(rp,url)
        links_found = soup.find_all('a', href=True)
        links = list(set(links_sitemap+links_found))
                
        indice_to_draw=sample(range(len(links)), min(len(links),5))
                
        for indice in indice_to_draw: # Exploration de 5 liens maximum par page
            new_url = links[indice]['href']
            #print(new_url)
            if self.actual_url(new_url):
                if self.reform_url_robots(new_url)!=self.reform_url_robots(url):
                    try:
                        rp=self.read_robots(new_url)
                    
                        if self.is_valid_url(rp, new_url) and (new_url not in self.downloaded):
                            self.frontier.append(new_url)
                            time.sleep(3)  # Respecte la politesse en attendant 3 secondes entre chaque appel
                    except Exception as e:
                        print(f"Error reading robots.txt of {url}: {str(e)}")
        #except Exception as e:
            #print(f"Error extracting links from {url}: {str(e)}")

    def actual_url(self, url):
        parse_url = urlparse(url)
        if parse_url.scheme=='mailto':
            return False
        return True

    def reform_url_robots(self, url):
        parse_url = urlparse(url)
        #print(url)
        #print(parse_url)
        reform_base_url = parse_url.scheme+'://'+parse_url.netloc
        return reform_base_url+"/robots.txt"

    def read_robots(self, url):
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(self.reform_url_robots(url))
        rp.read()
        return rp
    
    def extract_links_sitemap(self,rp, url):
        links=rp.site_maps()
        if links is None:
            return []
        for link in links:
            if link[-4:]==".xml":
                links.remove(link)
                links+=self.extract_links_sitemap(rp,link)
        return links
            
    def is_valid_url(self, rp, url):
        return rp.can_fetch("*", url)

    def crawler_delay(self, rp, url):
        delay=rp.crawl_delay(url)
        if delay is None:
            delay=0
        return delay
        

# Exemple d'utilisation
if __name__ == "__main__":
    #starting_url = "https://ensai.fr/"
    crawler = Crawler(["https://ensai.fr/"])
    crawler.crawl()
    #print(crawler.is_valid_url("https://ensai.fr/"))
    #print(sample(range(0, 5), 3))
    #crawler.extract_links("https://ensai.fr/")
