from linkedin.LinkedinScraper import LinkedinScraper
import requests
from lxml.html import fromstring
import os

url = "https://www.linkedin.com/pulse/20140326191638-235001-how-to-write-your-first-blog-post-on-the-linkedin-publishing-platform/"

response = requests.get(url)

response_dir = os.path.join(os.path.dirname(__file__), "response")
os.makedirs(response_dir, exist_ok=True)
file_path = os.path.join(response_dir, "test.html")

with open(file_path, "wb") as f:
    f.write(response.content)

scraper =  LinkedinScraper(response_text=response.content, url=url)

print(scraper.extract_data())