from urllib.parse import urlparse

url="http://careers.disneylandparis.com/fr"

parse_url = urlparse(url)

reform_base_url = parse_url.scheme+'://'+parse_url.netloc+"/robots.txt"

print(parse_url)
print(reform_base_url)