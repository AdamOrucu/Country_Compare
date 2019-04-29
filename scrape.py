import requests
import urllib.request
from bs4 import BeautifulSoup

# Gets html of wanted country from Wikipedia
def get_html(country):
    try:
        url = "https://en.wikipedia.org/wiki/" + country
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")
    except:
        return False

# Gets demonym(s) used
def get_demonyms(soup):
    dens = []
    infobox = soup.find('table', {'class': "infobox"})
    for row in infobox.find_all('tr'):
        if(row.find('th') != None):
            if 'Demonym' in row.find('th').getText():
                for den in row.find('td').find_all('a'):
                    dens.append(den.string)
                if dens == []:
                    for den in row.find('td').find_all('li'):
                        print('entered')
                        dens.append(den.string)
    print(dens)
    return dens

# Gets the country flag
def get_flag(soup):
    infobox = soup.find('table', {'class': "infobox"})
    for img in infobox.find_all('img'):
        if 'Flag' in img.get('src'):
            return (infobox.find('img').get('src'))

# Returns all the paragaraphs where the keywords were used
def check_word_in_soup(keywords, soup):
    res = []
    for keyword in keywords:
        for par in soup.find_all('p'):
            if par.getText() != None:
                if keyword.lower() in par.getText().lower():
                    res.append(par)
    return res

# Gets some important information about a country
def get_info_table(soup):
    no_nos = ['[1]', '[2]', '[3]', '[4]', '[5]', '[6]', '[7]', '[a]', '[b]', '[c]', '[d]', '[N 2]']
    res_rows = []
    infobox = soup.find('table', {'class': "infobox"})
    for row in infobox.find_all('tr'):
        if(row.find('th') != None):
            if 'Capital' in row.find('th').getText():
                caps = []
                for cap in row.td.find('a'):
                    if cap not in no_nos:
                        caps.append(cap.string)
                res_rows.append(('capital', caps))
            elif 'language' in row.find('th').getText():
                langs = []
                for lang in row.td.findChildren('a'):
                    if lang.string not in no_nos:
                        langs.append(lang.string)
                res_rows.append((row.find('th').getText(), langs))
            elif 'groups' in row.find('th').getText().lower():
                groups = []
                for group in row.td.find_all('li'):
                    if group not in no_nos:
                        groups.append(group.getText())
                if groups == []:
                    for group in row.td.find_all('a'):
                        if group not in no_nos:
                            groups.append(group.getText())
                res_rows.append(('Ethnic Groups', groups))
            elif 'religion' in row.find('th').getText().lower():
                rels = []
                for rel in row.td.find_all('li'):
                    if rel not in no_nos:
                        rels.append(rel.getText())
                if rels == []:
                    for rel in row.td.find_all('a'):
                        if rel not in no_nos:
                            rels.append(rel.getText())
                res_rows.append(('Religion', rels))
    return res_rows