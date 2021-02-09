#スクレイピングに関するファイル
from bs4 import BeautifulSoup as bs
import requests

import re

class Scraping:
    # Scraping.get_result(url,tags) is the entry point for scraping.
    # the flow is below...(it is written like example)
    # example description : [func.__name__]

    # [Flow]
    # 1. Ckeck if url and tags are not "". [_check_tag_url(url,tags)]
    #       bool:True  -> continue
    #       bool:False -> exit
    # 2. make request and get html. [requests.get(url)]
    # 3. make valid encoding. [res.encoding = res.apparent_encoding]
    # 4. make soup.[BeautifulSoup(body,parser)]
    # 5. get target tag if that exists in the html. [_get_html_tags(soup)]
    #       the target tag is hard coded -> extractlist = ["p"]
    # 6. get result(dict). [_match_tag_alltext(soup,tags,htmltags)]     
    #       result = {"tag":{"htmltag.name":[text1,text2,...]}} 

    @classmethod
    def get_results(cls,url:str,tags:list):     

        if not cls._check_tag_url(url,tags):  
            return "url or tag is invalid."

        res = requests.get(url)
        res.encoding = res.apparent_encoding
        soup = bs(res.text,'html.parser')
        htmltags = cls._get_html_tags(soup)
        itemlist = cls._match_tag_alltext(soup,tags,htmltags)
        return itemlist


    def _check_tag_url(url,tags) -> bool:
        Number = 1

        if url == "" or tags == "":
            return False
        else:
            return True

    def _get_html_tags(soup) -> list:
        Number = 2

        extractlist = ["p","a","li"]

        alltags = soup.findAll(True) 
        tagslist_raw = [tag.name for tag in alltags if tag.name in extractlist]
        tagslist = list(dict.fromkeys(tagslist_raw))
        return tagslist

    def _match_tag_alltext(soup,SearchTags:list,HtmlTags:list) -> dict:
        Number = 3

        result = {}
        for htmltag in HtmlTags:
            minisoup = soup.findAll(htmltag)
            for minimumsoup in minisoup:
                try:
                    for searchtag in SearchTags:
                        text = minimumsoup.text
                        m = re.search(searchtag,text)
                        if m !=None:
                            if result.get(searchtag,False):
                                if result[searchtag].get(htmltag,False):
                                    result[searchtag][htmltag].append(text)
                                else:
                                    result[searchtag][htmltag] = [text]
                            else:
                                result[searchtag] = {htmltag:[text]}
                except:
                    continue

        return result








