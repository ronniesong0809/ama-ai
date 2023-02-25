import requests
from bs4 import BeautifulSoup


def fetch_data1(url):
    r = requests.get(url)
    print(r.status_code)
    soup = BeautifulSoup(r.text, "html.parser")
    if r.status_code == 200:
        strs = []
        for node in soup.findAll("p"):
            strs.append(node.findAll(string=True))
        page = "".join(str(s) for s in strs)
        return page
    else:
        return ""


def fetch_data(url):
    r = requests.get(url)
    print(r.status_code)
    soup = BeautifulSoup(r.text, "html.parser")
    if r.status_code == 200:
        strs = []
        for node in soup.findAll(string=True):
            strs.append(node)
        page = "".join(str(s) for s in strs)
        return page
    else:
        return ""
