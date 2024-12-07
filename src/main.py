from linkedin.LinkedinScraper import LinkedinScraper
import requests
from lxml.html import fromstring
import os

url = "https://www.linkedin.com/posts/poonam-soni-9255931b2_jobpreparation-remotejobs-websites-activity-7270398477816205312-o4ql?utm_source=share&utm_medium=member_desktop"

response = requests.get(url)

response_dir = os.path.join(os.path.dirname(__file__), "response")
os.makedirs(response_dir, exist_ok=True)
file_path = os.path.join(response_dir, "test.html")

with open(file_path, "wb") as f:
    f.write(response.content)

scraper =  LinkedinScraper(response_text=response.content, url=url)

print(scraper.extract_data())