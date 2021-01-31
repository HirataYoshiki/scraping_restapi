from bs4 import BeautifulSoup as bs
import requests

import re


def get_results(url:str,*tags,methods = "or"):
    if url = "" or tags = "":
        if url = "":
            text = "please enter the url.\n"
        if tag = "":
            text_2 = "please enter the tags."    
            text += text_2
        return text
    
    res = requests.get(url)
    soup = bs(res.text,"html.parser")

    all_text = soup.get_text().split(" ")

    itemlist = {}

    for text in all_text:
        for tag in tags:
            m = re.match(tag,text)
            item = m.groups()
            if not len(item)==0:
                itemlist[text]= item

    return itemlist







