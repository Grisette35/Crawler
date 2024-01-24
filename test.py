import urllib.robotparser
from urllib.parse import urlparse

rp = urllib.robotparser.RobotFileParser()

rp.set_url("https://ensai.fr/robots.txt")
rp.read()
print(rp.site_maps())
#print(rp.can_fetch("*", "https://ensai.fr/*/trackback"))

#parse_url = urlparse("https://groupebpce.com/")
#reform_base_url = parse_url.scheme+'://'+parse_url.netloc
#print(reform_base_url)

#site_maps()