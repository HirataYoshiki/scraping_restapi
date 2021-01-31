from bs4 import BeautifulSoup as bs
import requests

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




