# amazon.py

import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def process_product_url(product_url, len_page=4):
    headers = {
        'authority': 'www.amazon.in',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
   # product_url = 'https://www.amazon.in/TeckNet-Ergonomic-Wireless-Chromebook-Adjustment/dp/B015NBTAOW/ref=sr_1_3?dib=eyJ2IjoiMSJ9.B8_ra3fwf_qbARNiC8cpwhm59DAMkRdsAxJMswYe-9yK1xFvtFce6ejrMl96P1-UUTjFsdLKyYib6XBPcjIpvyRYPb7YhBrShRRjqn0-kHWIot0nOdKREgqRZ-Yi1ug4CR3zWeB7nuAn1io0nrMfsZllZvIsIRv_2rm0uy7eXL1_7egx51rNyHAg8c2vf47czvlzEdsEsUpWpmhiidJ_SF2z1k9hPCdUH5VCNCXZPog.30Z8Be8SIM5Y5L3yjsa7lXoNWHLhAJsKjtfEyqiYWro&dib_tag=se&keywords=mouse&qid=1705899931&sr=8-3&th=1'
    # Extra Data as Html object from amazon Review page
    def reviewsHtml(product_url, len_page):
        soups = []
        for page_no in range(1, len_page + 1):
            params = {
                'ie': 'UTF8',
                'reviewerType': 'all_reviews',
                'filterByStar': 'critical',
                'pageNumber': page_no,
            }
            response = requests.get(product_url, headers=headers, params=params)
            soup = BeautifulSoup(response.text, 'lxml')
            soups.append(soup)
        return soups

    # Grab Reviews name, description, date, stars, title from HTML
    def getReviews(html_data):
        data_dicts = []
        boxes = html_data.select('div[data-hook="review"]')
        for box in boxes:
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
                datetime_str = box.select_one('[data-hook="review-date"]').text.strip().split(' on ')[-1]
                date = datetime.strptime(datetime_str, '%B %d, %Y').strftime("%d/%m/%Y")
            except Exception as e:
                date = 'N/A'

            try:
                description = box.select_one('[data-hook="review-body"]').text.strip()
            except Exception as e:
                description = 'N/A'

            data_dict = {
                'Name': name,
                'Stars': stars,
                'Title': title,
                'Date': date,
                'Description': description
            }

            data_dicts.append(data_dict)

        return data_dicts

    html_datas = reviewsHtml(product_url, len_page)
    reviews = []

    for html_data in html_datas:
        review = getReviews(html_data)
        reviews += review

    df_reviews = pd.DataFrame(reviews)
    #return df_reviews
    df_reviews.to_csv('reviews.csv', index=False)
    return df_reviews