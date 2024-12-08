import os


def identify_url_type(url):

    if "https://www.linkedin.com/" in url:
        return "linkedin"

    elif "https://www.youtube.com/" in url:
        return "youtube"

    elif "https://x.com/" in url:
        return "x"


def define_output_path():
    
    response_dir = os.path.join(os.path.dirname(__file__), "response")
    os.makedirs(response_dir, exist_ok=True)
    file_path = os.path.join(response_dir, "test.html")
    return file_path
