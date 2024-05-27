from bs4 import BeautifulSoup
import requests
from pprint import pprint
from datetime import datetime



class SabcNewsScraper:
    def __init__(self):
        response = requests.get(url="https://www.sabcnews.com/sabcnews/")
        sabc_html_text = response.text
        self.soup = BeautifulSoup(sabc_html_text, "html.parser")
        self.selectors = [".elementor-section.elementor-inner-section.elementor-element.elementor-element-5cbecfd.elementor-section-full_width.elementor-section-height-default.elementor-section-height-default", ".elementor-section.elementor-top-section.elementor-element.elementor-element-85e4325.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default", ".elementor-section.elementor-top-section.elementor-element.elementor-element-62fbc394.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default", ".elementor-element.elementor-element-53ee0ee.elementor-widget.elementor-widget-shortcode", ".elementor-element.elementor-element-01a6303.elementor-widget.elementor-widget-shortcode", ".elementor-section.elementor-inner-section.elementor-element.elementor-element-1651432c.elementor-section-full_width.elementor-section-height-default.elementor-section-height-default"]

    # Scraps image sources.
    def scraped_imgs(self):
        all_img_links = [[tag.get("src") for tag in self.soup.select(f"{selector} img")] for selector in self.selectors]
        pprint(all_img_links)
        return all_img_links

    # Scraps article text (description and date).
    def scraped_article_link_and_date(self):
        descriptions = [[tag.text for tag in self.soup.select(f"{selector} a")] for selector in self.selectors]
        date_and_time_lst = [[tag.text for tag in self.soup.select(f"{selector} time")] for selector in self.selectors]
        span_text = self.soup.select_one(f".elementor-section.elementor-inner-section.elementor-element.elementor-element-5cbecfd.elementor-section-full_width.elementor-section-height-default.elementor-section-height-default span").text

        return [descriptions, date_and_time_lst, span_text]


    # Combines all scraped data except data from other_data function
    def mixology(self):
        img_data = self.scraped_imgs()
        art_link_data = self.scraped_article_link_and_date()

        second_art_lst = art_link_data[0][0][3].split("\n")
        third_art_lst = art_link_data[0][0][4].split("\n")

        second_art_des = second_art_lst[3]
        second_art_date = second_art_lst[4]

        third_art_des = third_art_lst[3]
        third_art_date = third_art_lst[4]

        mix_it_up = [

            {"art_1": {
                "img_url": img_data[0][0],
                "description": art_link_data[0][0][1],
                "date_time": art_link_data[-1]
                },
            },
            {"art_2": {
                    "img_url": img_data[0][1],
                    "description": second_art_des,
                    "date_time": second_art_date,
                },
            },
            {"art_3": {
                    "img_url": img_data[0][2],
                    "description": third_art_des,
                    "date_time": third_art_date,
                },
            },
        ]

        for num in range(3, 27):
            mix_it_up.append({f"art_{num}": {
                                "img_url": img_data[0][3],
                                "description": None,
                                "date_time": None,
                                },
                             })

        pprint(mix_it_up)

SabcNewsScraper().scraped_imgs()

