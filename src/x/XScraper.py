import requests
import os
import json
from dotenv import load_dotenv


load_dotenv()

class XScraper:

    def __init__(self, url) -> None:
        self.url = url

    bearer_token = os.getenv("X_BEARER_TOKEN")
    

    def create_tweet_endpoint(self):

        tweet_fields = "tweet.fields=lang,author_id,text,created_at"
        media_fields = "media.fields=preview_image_url,url"

        ids = self.url.split("/")[-1]
        ids = "ids=" + str(ids)
        api_endpoint = "https://api.twitter.com/2/tweets?{}&{}&expansions=attachments.media_keys&{}".format(ids, tweet_fields,media_fields)
        return api_endpoint


    def create_user_endpoint(self):

        usernames = "usernames=" + self.url.split("/")[-1]
        user_fields = "user.fields=description,created_at,profile_image_ur,description,location,name"
        url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
        
        return url


    def bearer_oauth(self, r):

        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2Lookup"
        return r



    def connect_to_endpoint(self, url):

        response = requests.request("GET", url, auth=self.bearer_oauth)
        print(response.status_code)

        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        
        return response.json()



    def extract_tweet_data(self):

        api_endoint = self.create_tweet_endpoint()
        json_response = self.connect_to_endpoint(api_endoint)
                
        return json.dumps(json_response, indent=4, sort_keys=True)
    

    def extract_user_data(self):

        api_endoint = self.create_user_endpoint()
        json_response = self.connect_to_endpoint(api_endoint)
                
        return json.dumps(json_response, indent=4, sort_keys=True)



    def extract_data(self):
        
        category = self.url.split("/")[-2]

        if category == "status":
            return self.extract_tweet_data()
        
        else:
            return self.extract_user_data()
        
        
        


    