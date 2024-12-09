from linkedin.LinkedinScraper import LinkedinScraper
from x.XScraper import XScraper
from youtube.YoutubeScraper import YoutubeScraper
from utils.utils import define_output_path, identify_url_type
import requests

url = "https://www.youtube.com/watch?v=5CmAKm1wWW0"

url_type = identify_url_type(url=url)

response = requests.get(url)
file_path = define_output_path()

with open(file_path, "wb") as f:
    f.write(response.content)

if url_type == "linkedin":
    scraper =  LinkedinScraper(response_text=response.content, url=url)

elif url_type == "x":
    scraper = XScraper(url=url)

elif url_type == "youtube":
    scraper = YoutubeScraper(response_text=response.content, url=url)

print(scraper.extract_data())