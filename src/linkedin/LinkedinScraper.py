from lxml.html import fromstring


class LinkedinScraper:

    def __init__(self, response_text, url) -> None:
        self.parser = fromstring(response_text)
        self.url = url

    def validate_structure(self):
        if self.parser.xpath("//div[contains(@class, 'article-main__content')]//h3"):
            return "content_type_1"
        if self.parser.xpath("//div[contains(@class, 'article-main__content')]//strong"):
            return "content_type_2"
        else:
            return "general_content"


    def extract_pulse_title_and_author(self):
        
        data = {}

        #Fetch Title
        title = self.parser.xpath("//h1/text()")
        data["title"] = title[0]

        #Fetch Author Details
        author_name = self.parser.xpath("//h3[contains(@class, 'base-main-card__title')]/text()")[0].strip()
        data["author"] = author_name

        linkedin_url = self.parser.xpath("//a[contains(@class, 'base-card__full-link')]/@href")[0].strip()
        data["linkedin_url"] = linkedin_url
        
        bio = self.parser.xpath("//h4[contains(@class, 'base-main-card__subtitle')]/text()")[0].strip()
        data["bio"] = bio

        return data


    def extract_pulse_type1_content(self):
        div = self.parser.xpath("//div[contains(@class, 'article-main__content')]")[0]
        headings = div.xpath(".//h3 | .//strong") 

        result = []
        for _, heading in enumerate(headings):
        
            heading_text = heading.text_content().strip()
            content = []
            sibling = heading.getnext()

            while sibling is not None and sibling.tag not in ['h3', 'strong']:
                content.append(sibling.text_content().strip())
                sibling = sibling.getnext()
            
            result.append({
                "heading": heading_text,
                "content": " ".join(content)
            })

        return result


    def extract_linkedin_post(self):
        
        author_name = self.parser.xpath("//article[contains(@class, 'main-feed-activity-card-with-comments')]//a[contains(@data-tracking-control-name, 'public_post_feed-actor-name')]//text()")
        author_name = ' '.join(author_name).strip() if author_name else None

        linkedin_url = self.parser.xpath("//article[contains(@class, 'main-feed-activity-card-with-comments')]//a[contains(@data-tracking-control-name, 'public_post_feed-actor-name')]//@href")
        linkedin_url = ' '.join(linkedin_url).strip()
        cleaned_url = linkedin_url.split("?")[0] if linkedin_url else None

        bio = self.parser.xpath("//article[contains(@class, 'main-feed-activity-card-with-comments')]//div[contains(@data-test-id, 'main-feed-activity-card__entity-lockup')]//p//text()")
        bio = ' '.join(bio).strip() if bio else None

        post_content = self.parser.xpath("//article[contains(@class, 'main-feed-activity-card-with-comments')]//div[contains(@class, 'attributed-text-segment-list__container')]//p[not(contains(@class, 'comment__text'))]//text()")
        post_content = ' '.join(post_content).strip() if post_content else None

        img_media = self.parser.xpath("//article[contains(@class, 'main-feed-activity-card-with-comments')]//img[contains(@src, 'http')]/@src")
        img_media = ", ".join(img_media).strip() if img_media else None

        video_media = self.parser.xpath("//article[contains(@class, 'main-feed-activity-card-with-comments')]//video[contains(@src, 'http')]/@src")
        video_media = ' '.join(video_media).strip() if video_media else None

        hashtags = self.parser.xpath("//article[contains(@class, 'main-feed-activity-card-with-comments')]//a[contains(text(), '#')]/text()")
        category = hashtags[0] if hashtags else None
        sub_category = ', '.join(hashtags[1:]) if len(hashtags) > 1 else None

        return {
            "author_name": author_name,
            "linkedin_url": cleaned_url,
            "bio": bio,
            "post_content": post_content,
            "image_media": img_media,
            "video_media": video_media,
            "hashtags": {
                "category": category,
                "sub_categeory": sub_category
            }
        }


    def extract_data(self):
        json_data = {}

        category = "unknown"

        if "linkedin.com/blog" in self.url:
            category = "blog"
        elif "linkedin.com/pulse/" in self.url:
            category = "pulse"
        elif "linkedin.com/posts" in self.url:
            category = "posts"
        elif "linkedin.com/business/marketing/blog/" in self.url:
            category = "business"

        if category == "pulse":
            content_type = self.validate_structure()

            if content_type == "content_type_1":
                json_data = self.extract_pulse_title_and_author()
                json_data["blog_content"] = self.extract_pulse_type1_content()
            
            elif content_type == "content_type_2":
                pass
    
        elif category == "posts":
            return self.extract_linkedin_post()
        

        return json_data