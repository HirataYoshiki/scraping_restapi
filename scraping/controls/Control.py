from bs4 import BeautifulSoup as bs
import requests

import re

class Scraping:
    @classmethod
    def get_results(cls,url:str,tags,*,methods = "or"):
        if url == "" or tags == "":
            if url == "":
                text = "please enter the url.\n"
            if tags == []:
                text_2 = "please enter the tags."    
                text += text_2
            return text
        
        res = requests.get(url)
        soup = bs(res.text,"html.parser")

        all_ = soup.find_all("li")
        all_text = soup.get_text().split("\n")

        itemlist = {}

        if type(tags) == list:
            for tag in tags:
                itemlist[tag] = cls._match_tag_alltext(tag,all_text)
        elif type(tags) == str:
            itemlist[tags] = cls._match_tag_alltext(tag,all_text)

        return itemlist

    def _get_all_tag(url) ->list:
        res = requests.get(url)
        soup = bs(res.text,"html.parser")
        alltags = soup.findAll(True) 
        tagslist_raw = [tag.name for tag in alltags]
        tagslist = list(dict.fromkeys(tagslist_raw))
        return tagslist

    def _match_tag_alltext(tag,all_text) ->list:
        result = []
        for text in all_text:
            m = re.search(re.escape(tag),text)
            if m != None:
                result.append(text)
        return result









