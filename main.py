from crawler import Crawler
from crawler_db import Crawler_db

def main(arg):
    crawler_db=Crawler_db()
    conn, cursor = crawler_db.create_conn()
    crawler = Crawler(["https://ensai.fr/"], conn, cursor)
    crawler.crawl()
    crawler_db.close_conn(conn)

if __name__=="__main__":
    main(arg)
