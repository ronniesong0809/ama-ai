import requests
from bs4 import BeautifulSoup


def fetch_data(url, all, tag):
    r = requests.get(url)
    print(r.status_code)
    soup = BeautifulSoup(r.text, "html.parser")
    if r.status_code == 200:
        if all:
            context = soup.get_text().replace('\n', '#')
            return list(filter(None, context.split('#')))
        else:
            strs = []
            for node in soup.findAll(tag):
                strs.append(node.findAll(string=True))
            context = ["".join(s) for s in strs]
            return context
    else:
        return ""
