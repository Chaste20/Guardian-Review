
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime




#json_filename = 'reviews.json'
#Header to set the requests as a browser requests
headers = {
    'authority': 'www.amazon.in',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
# URL of The amazon Review page
#reviews_url = 'https://www.amazon.in/Zebronics-Zeb-Comfort-Wired-Mouse-Black/dp/B07L94YR16/ref=sr_1_1_sspa?crid=2AAL7N4FWCKKQ&dib=eyJ2IjoiMSJ9.EXZ0OtfR7azIv6lxw1qxvVsRn2S8UTl7iKZ9Tt7FHyS-vREIjAJZTPDq0dSQCkb8_vE53rBQxhccZNH0Qz4o6kzWaZvQZBf5Q7RlVTSzwZ22DgPOSFKUC3hfv_8ZPU1zEVtyEHFx7xc90IlEZa6cywyc7ZShmS8L5NX3HK8vntejpY8J6e3NQK98W4elNeFDBlTJtR24Wdim6pWYPwBpMuILIqyu4QhAyBCG79Mnyig.c6VHP7vhqYeUdjJeE1cNjW2E9BKQ7ruzoEUXpapPWFQ&dib_tag=se&keywords=mouse&qid=1705727576&sprefix=mo%2Caps%2C564&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1'
reviews_url = url

# Define Page No
len_page = 2


# Extra Data as Html object from amazon Review page
def reviewsHtml(url, len_page):
    
    # Empty List define to store all pages html data
    soups = []
    
    # Loop for gather all 3000 reviews from 300 pages via range
    for page_no in range(1, len_page + 1):
        
        # parameter set as page no to the requests body
        params = {
            'ie': 'UTF8',
            'reviewerType': 'all_reviews',
            'filterByStar': 'critical',
            'pageNumber': page_no,
        }
        
        # Request make for each page
        response = requests.get(url, headers=headers)
        
        # Save Html object by using BeautifulSoup4 and lxml parser
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Add single Html page data in master soups list
        soups.append(soup)
        
    return soups

# Grab Reviews name, description, date, stars, title from HTML
def getReviews(html_data):

    # Create Empty list to Hold all data
    data_dicts = []
    
    # Select all Reviews BOX html using css selector
    boxes = html_data.select('div[data-hook="review"]')
    
    # Iterate all Reviews BOX 
    for box in boxes:
        
        # Select Name using css selector and cleaning text using strip()
        # If Value is empty define value with 'N/A' for all.
        try:
            name = box.select_one('[class="a-profile-name"]').text.strip()
        except Exception as e:
            name = 'N/A'

        try:
            stars = box.select_one('[data-hook="review-star-rating"]').text.strip().split(' out')[0]
        except Exception as e:
            stars = 'N/A'   

        try:
            title = box.select_one('[data-hook="review-title"]').text.strip()
        except Exception as e:
            title = 'N/A'

        try:
            # Convert date str to dd/mm/yyy format
            datetime_str = box.select_one('[data-hook="review-date"]').text.strip().split(' on ')[-1]
            date = datetime.strptime(datetime_str, '%B %d, %Y').strftime("%d/%m/%Y")
        except Exception as e:
            date = 'N/A'

        try:
            description = box.select_one('[data-hook="review-body"]').text.strip()
        except Exception as e:
            description = 'N/A'

        # create Dictionary with al review data 
        data_dict = {
            'Name' : name,
            'Stars' : stars,
            'Title' : title,
            'Date' : date,
            'Description' : description
        }

        # Add Dictionary in master empty List
        data_dicts.append(data_dict)
    
    return data_dicts

# Grab all HTML
html_datas = reviewsHtml(reviews_url, len_page)

# Empty List to Hold all reviews data
reviews = []


# Iterate all Html page 
for html_data in html_datas:
    
    # Grab review data
    review = getReviews(html_data)
    
    # add review data in reviews empty list
    reviews += review

    # Create a dataframe with reviews Data
df_reviews = pd.DataFrame(reviews)
#df_reviews

df_reviews.to_csv('reviews.csv', index=False)
#df_reviews.to_json(json_filename, orient='records', lines=True)