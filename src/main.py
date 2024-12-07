from linkedin.LinkedinScraper import LinkedinScraper
from utils.utils import define_output_path, identify_url_type
import requests
from lxml.html import fromstring
import os

url = "https://www.linkedin.com/blog/member/career/manage-your-day-like-tony-robbins-richard-branson-and-other-productive-people"

response = requests.get(url)

file_path = define_output_path()

with open(file_path, "wb") as f:
    f.write(response.content)

url_type = identify_url_type(url=url)

if url_type == "linkedin":
    scraper =  LinkedinScraper(response_text=response.content, url=url)

print(scraper.extract_data())