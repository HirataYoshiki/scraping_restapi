from bs4 import BeautifulSoup as bs
import requests

import re

URL = "https://tdoc.info/beautifulsoup/#navigating-the-parse-tree"
TAG = ["タグ","要素"]

class Test_scraping:
    @classmethod
    def get_results(cls,url:str,tags,*,methods = "or"):     
        if not cls._check_tag_url(url,tags):  
            return "url or tag is invalid."

        res = requests.get(url)
        soup = bs(res.text,"html.parser")

        all_text = soup.get_text().split("\n")

        itemlist = {}

        if type(tags) == list:
            for tag in tags:
                itemlist[tag] = cls._match_tag_alltext(tag,all_text)
        elif type(tags) == str:
            itemlist[tags] = cls._match_tag_alltext(tag,all_text)
            
        return itemlist

    def _check_tag_url(url,tag) -> bool:
        if url == "" or tags == "":
            return False
        else:
            return True

    def _get_all_tag(soup) -> list:
        alltags = soup.findAll(True) 
        tagslist_raw = [tag.name for tag in alltags]
        tagslist = list(dict.fromkeys(tagslist_raw))
        return tagslist

    def _match_tag_alltext(tag,all_text) -> list:
        result = []
        for text in all_text:
            m = re.search(re.escape(tag),text)
            if m != None:
                result.append(text)
        return result
    

if __name__ == "__main__":
    print(Test_scraping.get_results(URL,TAG))