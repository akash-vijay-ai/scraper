from lxml.html import fromstring

class LinkedinScraper:

    def __init__(self, response_text, url) -> None:
        self.parser = fromstring(response_text)
        self.url = url


    def extract_linkedin_blog(self):
        
        title = self.parser.xpath("//h1/text()")
        title = ' '.join(title).strip()

        author_name = self.parser.xpath("//div[contains(@class, 'author-profile')]//a//text()")
        author_name = ' '.join(author_name).strip()
        cleaned_author_name = author_name.split("by ")[1]

        bio = self.parser.xpath("//div[contains(@class, 'author-profile')]//p//text()")
        bio = ' '.join(bio).strip()
        cleaned_bio = bio.split(" \n")[0]

        content = self.parser.xpath("//div[contains(@class, 'component component-migratedContent')]//text()")
        content = ' '.join(content).strip()

        category = self.url.split("/")[-2:-1]
       

        return {
            "title": title,
            "author": cleaned_author_name,
            "bio": cleaned_bio,
            "content": content,
            "category": category
        }


    def extract_pulse(self):

        title = self.parser.xpath("//h1/text()")
        title = ' '.join(title).strip()

        author_name = self.parser.xpath("//h3[contains(@class, 'base-main-card__title')]/text()")
        author_name = ' '.join(author_name).strip()

        linkedin_url = self.parser.xpath("//a[contains(@class, 'base-card__full-link')]/@href")
        linkedin_url = ' '.join(linkedin_url).strip()
        
        bio = self.parser.xpath("//h4[contains(@class, 'base-main-card__subtitle')]/text()")
        bio = ' '.join(bio).strip()

        text_content = self.parser.xpath("//div[contains(@class, 'article-main__content')]//text()")
        cleaned_text = [text.strip() for text in text_content if text.strip()]
        cleaned_text = ' '.join(cleaned_text)   

        return {
            "title": title,
            "author": author_name,
            "linkedin_url": linkedin_url,
            "bio": bio,
            "content": cleaned_text
        }



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

        if "linkedin.com/blog" in self.url:
            return self.extract_linkedin_blog()

        elif "linkedin.com/pulse/" in self.url:
            return self.extract_pulse()
        
        elif "linkedin.com/posts" in self.url:
            return self.extract_linkedin_post()
        
        elif "linkedin.com/business/marketing/blog/" in self.url:
            pass

        elif "linkedin.com/in/" in self.url:
            pass

        else:
            return {"Error": "Unidentified format"}
            