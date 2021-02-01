from bs4 import BeautifulSoup as bs
import requests

import re

URL = "https://tdoc.info/beautifulsoup/#iterating-over-a-tag"
TAG = ["Python","キーワード","時間"]

class Test_scraping:
    @classmethod
    def get_results(cls,url:str,tags:list,*,methods = "or"):     

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

        extractlist = ["p"]

        alltags = soup.findAll(True) 
        tagslist_raw = [tag.name for tag in alltags if tag.name in extractlist]
        tagslist = list(dict.fromkeys(tagslist_raw))
        return tagslist

    def _match_tag_alltext(soup,SearchTags:list,HtmlTags:list) -> dict:
        Number = 3

        itemlist = {}
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

        return itemlist



        
    

if __name__ == "__main__":
    Test_scraping.get_results(URL,TAG)