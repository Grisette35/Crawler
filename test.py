import urllib.robotparser
from urllib.parse import urlparse

import argparse

def main():
    parser = argparse.ArgumentParser(description='A simple script with command-line arguments.')
    
    # Adding a positional argument
    parser.add_argument('input_file', type=str, help='Input file path')
    
    # Adding an optional argument
    parser.add_argument('--output', type=str, help='Output file path')
    
    # Adding a flag argument
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Access the values of the arguments
    input_file = args.input_file
    output_file = args.output
    verbose_mode = args.verbose
    
    # Your script logic goes here
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"Verbose mode: {verbose_mode}")


    #main()
    #from protego import Protego
    #import reppy
    #x = reppy.fetch("https://ensai.fr/robots.txt")
    #x.allowed("https://ensai.fr/contactez-nous/?", "*")
    #rp = Protego.parse("https://twitter.com/robots.txt")
    #print(rp.can_fetch("https://twitter.com/robots.txt", "MyBot"))
print("hello")
    #from robobrowser import RoboBrowser
url = "https://twitter.com/robots.txt"
user_agent = "*"
import requests

def get_robots_txt(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve robots.txt. Status code: {response.status_code}")
            return None

    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

# Example usage:
url = "https://ensai.fr/robots.txt"
robots_content = get_robots_txt(url)

from fnmatch import fnmatch


# Example 3: Multiple wildcards
pattern3 = "/*?lang="
string3 = "https://twitter.com/ensai35?lang=fr"
result3 = fnmatch(string3, pattern3)
#print(f"Pattern: {pattern3}, String: {string3}, Result: {result3}")

#u = urlparse('https://ensai.fr/contactez-nous')
#print(u)
#v = urlparse('/*?lang=')
#print(v)
#w = urlparse('https://ensai.fr/contactez-nous/?')
#print(w)

#from protego import Protego

#rp = Protego.parse("https://twitter.com/robots.txt")
#print(rp.can_fetch("https://twitter.com/ensai35?lang=fr", "*"))

import urllib.robotparser
rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://ensai.fr/robots.txt")
rp.read()
print(rp.can_fetch("*","https://ensai.fr"))

#print(max(None, 3))
    

#rp = urllib.robotparser.RobotFileParser()

#rp.set_url("https://ensai.fr/robots.txt")
#rp.read()
#print(rp.site_maps())
#print(rp.can_fetch("*", "https://ensai.fr/*/trackback"))

#parse_url = urlparse("https://groupebpce.com/")
#reform_base_url = parse_url.scheme+'://'+parse_url.netloc
#print(reform_base_url)

#site_maps()