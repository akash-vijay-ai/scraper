from linkedin.LinkedinScraper import LinkedinScraper
from x.XScraper import XScraper
from utils.utils import define_output_path, identify_url_type
import requests
from lxml.html import fromstring
import os

url = "https://x.com/HenritheWolf/status/1865018852242853974"

response = requests.get(url)

file_path = define_output_path()

with open(file_path, "wb") as f:
    f.write(response.content)

url_type = identify_url_type(url=url)

if url_type == "linkedin":
    scraper =  LinkedinScraper(response_text=response.content, url=url)

elif url_type == "x":
    scraper = XScraper(url=url)

print(scraper.extract_data())