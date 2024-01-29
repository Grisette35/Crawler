import argparse
from crawler import Crawler
from crawler_db import Crawler_db

def parse_args():
    """
    Parses command-line arguments using argparse.

    Returns:
    - argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Web Crawler Example")
    parser.add_argument(
        "seed_url",
        type=str,
        help="The seed URL to start crawling from."
    )
    parser.add_argument(
        "--max_urls",
        type=int,
        default=100,
        help="Maximum number of URLs to crawl. Default is 100."
    )
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_args()

    # Initialize database
    crawler_db = Crawler_db()
    conn, cursor = crawler_db.create_conn()
    crawler_db.initialize_database(conn, cursor)

    # Create a Crawler object with user-specified parameters
    crawler = Crawler(seed_url=args.seed_url, conn=conn, cursor=cursor, max_urls=args.max_urls)

    # Start crawling
    crawler.crawl()

    # Close the database connection
    crawler_db.close_conn(conn)

if __name__ == "__main__":
    main()
