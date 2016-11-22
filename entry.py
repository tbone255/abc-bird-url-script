from bs4 import BeautifulSoup
import requests
from linker import Linker
import re
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from unidecode import unidecode


link = Linker()

def format_url():
    base_url = "https://web.archive.org/web/"
    date = "20001017050155/"
    return base_url + date + link.getNextLink()


def get_parsed_title(url): #gets title and parses it
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    result = soup.find('span', class_='H1')

    if result == None:
        result = soup.find('h1', {"align":"center"})
        if result == None:
            return "no-wayback"

    a = result.text
    b = _removeNonAscii(a)
    c = re.sub('\s+', ' ', b).strip()
    d = c.replace(" ", "-")
    return d.replace(" ", "")

def _removeNonAscii(s):
    return "".join(i for i in s if (ord(i) == 32 or ord(i) >= 65 and ord(i) <= 90 or ord(i) >= 97 and ord(i) <= 122 or 48 <= ord(i) <= 57 or ord(i) == 45 ))

def return_working_title(url):
    hdr = {'User-agent': 'Mozilla/5.0'}
    req = Request(url, headers=hdr)

    try:
        page = urlopen(req).read
        ppage = requests.get(url)

        soup = BeautifulSoup(ppage.text, 'html.parser')

        if "404 " in soup.text:
            return "not in new site"
    except HTTPError:
        return "NOT ON NEW SITE"

    return url

def add_all_links(a, b): #will add the link or note to the sheet
    link.rowNum = a
    for i in range(a, b):
        a = get_parsed_title(format_url())
        current_link = return_working_title("https://abcbirds.org/" + a)
        print(str(i) + " " + a + "  \n  " + "https://abcbirds.org/" + a)

        if a == 'no-wayback' or a is 'no-wayback':
            link.addNote("no-wayback-machine")
            print('WAYBACK')
        else:
            link.addNote(current_link)

    link.save()



try:
    add_all_links(30, 35)
except:
    link.save()
    print("FAILED")
    raise
