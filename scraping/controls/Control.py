from bs4 import BeautifulSoup as bs
import requests

import re


def get_results(url:str,tags,*,methods = "or"):
    if url == "" or tags == "":
        if url == "":
            text = "please enter the url.\n"
        if tags == []:
            text_2 = "please enter the tags."    
            text += text_2
        return text
    
    res = requests.get(url)
    soup = bs(res.text,"html.parser")

    all_ = soup.find_all("p")
    all_text = soup.get_text().split("\n")

    itemlist = {}

    if type(tags) == list:
        for tag in tags:
            itemlist[tag] = []
            for text in all_text:
                m = re.search(re.escape(tag),text)
                if m != None:
                    itemlist[tag].append(text)
    elif type(tags) == str:
        itemlist[tags] = []
        for text in all_text:
            print(text)
            m = re.search(re.escape(tags),text)
            if m != None:
                itemlist[tags].append(text)

    return itemlist







