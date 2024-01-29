from crawler import Crawler
from crawler_db import Crawler_db
import argparse

def main(arg):
    crawler_db=Crawler_db()
    conn, cursor = crawler_db.create_conn()
    crawler = Crawler(["https://ensai.fr/"], conn, cursor)
    crawler.crawl()
    crawler_db.close_conn(conn)

def main():
    parser = argparse.ArgumentParser(description='A simple script with command-line arguments.')
    
    # Adding a positional argument for the seed URL
    parser.add_argument('seed_url', type=str, help='Seed URL for the crawler')
    
    # Adding an optional argument for other configurations (if needed)
    parser.add_argument('--output', type=str, help='Output file path')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Access the values of the arguments
    seed_url = args.seed_url
    output_file = args.output
    verbose_mode = args.verbose
    
    # Your crawler logic goes here
    print(f"Seed URL: {seed_url}")
    print(f"Output file: {output_file}")
    print(f"Verbose mode: {verbose_mode}")

if __name__ == "__main__":
    main()

if __name__=="__main__":
    main(arg)
