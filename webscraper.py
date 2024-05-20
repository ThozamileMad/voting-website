from bs4 import BeautifulSoup
import requests
from pprint import pprint


class SabcNewsScraper:
    def __init__(self):
        response = requests.get(url="https://www.sabcnews.com/sabcnews/")
        sabc_html_text = response.text
        self.soup = BeautifulSoup(sabc_html_text, "html.parser")
        self.selectors = [".elementor-section.elementor-inner-section.elementor-element.elementor-element-5cbecfd.elementor-section-full_width.elementor-section-height-default.elementor-section-height-default", ".elementor-section.elementor-top-section.elementor-element.elementor-element-85e4325.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default", ".elementor-section.elementor-top-section.elementor-element.elementor-element-62fbc394.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default", ".elementor-element.elementor-element-53ee0ee.elementor-widget.elementor-widget-shortcode", ".elementor-element.elementor-element-01a6303.elementor-widget.elementor-widget-shortcode", ".elementor-section.elementor-inner-section.elementor-element.elementor-element-1651432c.elementor-section-full_width.elementor-section-height-default.elementor-section-height-default"]

    # Scraps image sources.
    def scraped_imgs(self):
        all_img_links = [[tag.get("src") for tag in self.soup.select(f"{selector} img")] for selector in self.selectors]
        return all_img_links

    # Scraps article text (description and date).
    def scraped_article_link_and_date(self):
        descriptions = [[tag.text for tag in self.soup.select(f"{selector} a")] for selector in self.selectors]
        date_and_time_lst = [[tag.text for tag in self.soup.select(f"{selector} time")] for selector in self.selectors]
        return [descriptions, date_and_time_lst]


    # Combines all scraped data except data from other_data function
    def mixology(self):
        mix_it_up = [
            {"first_image": {
                "img_url": self.scraped_imgs()[0][0],
                "description": self.scraped_article_link_and_date()[0][0][1],
                "time": self.scraped_article_link_and_date()[0][0][1]
                            },
            }
        ]

SabcNewsScraper().scraped_imgs()
SabcNewsScraper().scraped_article_link_and_date()
