
from bs4 import BeautifulSoup
import urllib.request as req
import re
url = "https://finance.naver.com/marketindex/exchangeDegreeCountQuote.naver?marketindexCd=FX_USDKRW_SHB&page=1"
def read_fx():
    res = req.urlopen(url)
    soup = BeautifulSoup(res, "html.parser")
    slist=soup.find("tbody").find_all("tr")
    td=[]
    for a in slist:
        td.append(a.text)
    table = str.maketrans('\t', ' ') 
    fx=td[0].split("\n");
    #print(fx[2]);
    val=float(fx[2].replace(",",""))
    return val

def read_sim(base,range):
    r=random.randrange(-range,range);
    fx=base+r;
    return fx;
    
