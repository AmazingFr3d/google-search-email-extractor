import datetime
import re

import pandas as pd
import requests


# This function extracts the emails from a given text
def email_ext(text):
    """

    :param text: this modules
    :return:
    """
    reg = re.findall(r"[A-Za-z0-9_%+-.]+"
                     r"@[A-Za-z0-9.-]+"
                     r"\.[A-Za-z]{2,5}", text)

    return reg


# This function gets the first 10 pages of a given keyword/phrase
def site_req(keyword: str):
    """

    :param keyword: the modules search term/keyword
    :return: this function returns a list of extracted emails from the first 10 pages of the search result.

    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    page = 0

    result = []
    location = "United States"
    keyword = keyword.replace(" ", "+")
    sites = ["facebook.com", "twitter.com", "linkedin.com", "instagram.com", "pinterest.com", "tiktok.com"]
    emails = ["gmail.com",
              "yahoo.com",
              "hotmail.com",
              "live.com",
              "aol.com"]
    emails = ["%40" + email for email in emails]
    emails = '"' + '"+"'.join(emails) + '"'

    for site in sites:

        while True:
            url = f'https://www.google.com/search?q="{keyword}"+"{location}"+"{site}"+{emails}&start={page}'
            print(keyword)
            print(site)

            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                break

            text = response.text
            result.extend(email_ext(text))
            print(result)

            if page == 100:
                break

            page = page + 10

    return result


# The functions uses the site_req() function to perform multiple search with multiple keywords/phrases
def google_search(keywords: list):
    result = []

    for keyword in keywords:
        req = site_req(keyword)
        if req:
            result.extend(req)
    print(len(result))
    return result


# This function saves the resulting list from google_search to a csv file
def to_csv(keywords: list):
    date_time = datetime.datetime.now()
    dt = date_time.strftime("%d_%m_%y_%H_%M")
    lists = google_search(keywords)
    df = pd.DataFrame(lists)
    df.to_csv(f'scraped_emails_{dt}.csv', index=False)
