from bs4 import BeautifulSoup as bs
import requests

import re

URL = "https://tdoc.info/beautifulsoup/#navigating-the-parse-tree"
TAG = ["タグ","要素"]

class Test_scraping:
    @classmethod
    def get_results(cls,url:str,tags:list,*,methods = "or"):     
        itemlist = {}

        if not cls._check_tag_url(url,tags):  
            return "url or tag is invalid."

        res = requests.get(url)
        soup = bs(res.text,"html.parser")
        htmltags = cls._get_html_tags(soup)



        return itemlist

    def _check_tag_url(url,tag) -> bool:
        Number = 1

        if url == "" or tags == "":
            return False
        else:
            return True

    def _get_html_tags(soup) -> list:
        Number = 2

        alltags = soup.findAll(True) 
        tagslist_raw = [tag.name for tag in alltags]
        tagslist = list(dict.fromkeys(tagslist_raw))
        return tagslist

    def _match_tag_alltext(soup,SearchTags:list,HtmlTags:list) -> dict:
        Number = 3

        result = {}
        for search in SearchTags:
            for 


        
    

if __name__ == "__main__":
    print(Test_scraping.get_results(URL,TAG))