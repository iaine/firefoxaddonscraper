'''
   Firefox Add-On Market

   Does history, search, category, & add-on version history
'''
import re
import ssl 
from urllib.request import urlopen

from bs4 import BeautifulSoup

import pandas as pd

import ScraperException

ssl._create_default_https_context = ssl._create_unverified_context

class FFScraper():

    def find_developer(self, language, userid):
        """
        Find extensions by FF addon developer
        """
        if language == "":
            raise ScraperException("No language given. Please use a code like en-GB or cn-ZH")
        if userid == "":
            raise ScraperException("No user given.")
        
        base = f"https://addons.mozilla.org/{language}/firefox/user/{userid}/"
        data = urlopen(base)
        #print(base)

        # parsing the html file
        htmlParse = BeautifulSoup(data, 'html.parser')
        print(htmlParse)
        links = []
        for link in htmlParse.find_all('ul', {'class': 'AddonsCard-list'}):
            for li in link.find_all('a', href=True):
                links.append(li)
        return links

    def find_categories(self, language=""):
        '''
            Get Categories
        '''
        categories = []
        if language == "":
            raise ScraperException("No language given. Please use a code like en-GB or cn-ZH")
        
        base = f"https://addons.mozilla.org/{language}/firefox/extensions/"
        data = urlopen(base)

        # parsing the html file
        htmlParse = BeautifulSoup(data, 'html.parser')

        # getting all the paragraphs
        for para in htmlParse.find_all("section", {'class':"Card"}):
            p = para.get_text()
            
            if p.startswith("Categories"):
                children = para.findChildren("li")
                for child in children:
                    anchors = child.find('a')
                    categories.append({child.get_text(): anchors.get('href')})

        return categories

    def find_software_by_category(self, language, category):
        ''' find add on by category'''

        categories = []

        if language == "":
            raise ScraperException("No language given. Please use a code like en-GB or cn-ZH")
        
        if '&' in category or ',' in category: 
            category.replace('&', '-').replace(',','-')

        base = f"https://addons.mozilla.org/{language}/firefox/extensions/category/{category}"
        data = urlopen(base)

        htmlParse = BeautifulSoup(data, 'html.parser')
        links = []
        for link in htmlParse.find_all('li', {'class': 'SearchResult'}):
            for li in link.find_all('a', href=True):
                d = li.get('href')
                if d.startswith(f"/{language}/firefox"): links.append(d)
        return links

    def find_software_by_search(self, searchterm, language, extension="", badging=""):
        ''' find add on by category'''

        categories = []
        if searchterm == "":
            raise ScraperException("No language given. Please use a code linke en-GB or cn-ZH")
        
        base = f"https://addons.mozilla.org/{language}/firefox/search/?q={searchterm}"

        if extension in ['theme', 'extension']:
            base += f"&type={extension}"

        if badging in ['recommended', 'line', 'badged']:
            base += f"&promoted={extension}"

        data = urlopen(base)

        htmlParse = BeautifulSoup(data, 'html.parser')
        links = []
        for link in htmlParse('li', {'class': 'SearchResult'}):
            for li in link.find_all('a', href=True):
                links.append(li.get('href'))
        return links

    def get_links(self, url):
        links = []

        data = urlopen(url, timeout=10)

        # parsing the html file
        htmlParse = BeautifulSoup(data, 'html.parser')

        # getting all the paragraphs
        for para in htmlParse.find_all("a"):
            ah = para.get('href')
            if "/firefox/addon/" in ah:
                links.append(para.get('href'))
        return links

    def get_version_data(self, url):
        '''
        Get version history links
        '''
        links = []

        data = urlopen(url + '/version', timeout=10)

        htmlParse = BeautifulSoup(data, 'html.parser')
        history = {}
        for lnk in htmlParse.find_all("li", {'class': 'AddonVersionCard'}):
            history['version'] = lnk.find('div', {'class': 'AddonVersionCard-version'})
            release = lnk.find('div', {'class': 'AddonVersionCard-fileInfo'}).get_text().split(' - ')
            history['releaseDate'] = release[0]
            history['releaseSize'] = release[1]
            history['platform'] = lnk.find('div', {'class': 'AddonVersionCard-compatability'})
            note = lnk.find('div', {'class': 'AddonVersionCard-releaseNotes'})
            history['notes'] = note.get_text()
            history['noteslink'] = note.find('a')['href']
            history['license'] = lnk.find('div', {'class': 'AddonVersionCard-license'}).get_text()
            history['download'] = lnk.find('div', {'class': 'InstallButtonWrapper-download'}).find('a')['href']
            
            links.append(history)

        return links

    def get_link_details(self, url):
        '''
        Get individual link and data
        '''
        details = {}

        base = f"https://addons.mozilla.org{url}"

        data = urlopen(base, timeout=10)

        # parsing the html file
        htmlParser = BeautifulSoup(data, 'html.parser')
        details['url'] = base
        # getting all the paragraphs
        details['title'] = htmlParser.find('h1',{'class':'AddonTitle'}).get_text()
        auth = htmlParser.find('span',{'class':'AddonTitle-author'})
        details['authorlink'] = auth.find('a').get('href')
        details['author'] = auth.find('a').get_text().replace('by', '').strip()
        desc = htmlParser.find('div',{'class':'AddonDescription-contents'})
        if desc is not None:
            details['description'] = htmlParser.find('div',{'class':'AddonDescription-contents'}).get_text()
        else:
            details['description'] = ""
        
        #details['badges'] = htmlParser.find('span',{'class':'AddonTitle-author'})
        if htmlParser.find('h4',{'class':'PermissionsCard-subhead--required'}) != None:
            reqs = []
            for req in htmlParser.find_all('li',{'class':'Permission'}): reqs.append(req.get_text())
            details['requiredpermissions'] = ";".join(reqs)
        else:
            details['requiredpermissions'] = ""
        #lnks = htmlParser.find('dd',{'class':'AddonMoreInfo-links'})
        #print(lnks)
        #ls = [l['href'] for l in lnks.find_all('a')]
        #details['links'] = ";".join(ls)
        details['version'] = htmlParser.find('dd',{'class':'AddonMoreInfo-version'}).get_text()
        details['size'] = htmlParser.find('dd',{'class':'AddonMoreInfo-filesize'}).get_text()
        details['last'] = htmlParser.find('dd',{'class':'AddonMoreInfo-last-updated'}).get_text()
        related = htmlParser.find('dd',{'class':'AddonMoreInfo-related-categories'})
        if related is not None:
            details['related'] = related.get_text()
        else:
            details['related'] = ""
        
        details['licence'] = htmlParser.find('dd',{'class':'AddonMoreInfo-license'}).get_text()
        priv = htmlParser.find('dd',{'class':'AddonMoreInfo-privacy-policy'})
        if priv is not None: 
            details['privacy'] = priv.find('a').get('href')
        else:
            details['privacy'] = ""
        #details['tags'] = htmlParser.find('dd',{'class':'AddonMoreInfo-tag_links'}).get_text()

        return details

    def get_links_details(self, linksarray):
        '''
        Get the detail pages from a links array
        '''
        details = []
        for l in linksarray:
            print(l)
            details.append(self.get_link_details(l))
        return details

    def write_file(self, data, filename):
        ''' Write to CSV '''
        df = pd.DataFrame(data)

        df.to_csv(filename, index=False)
    
class ScraperException(Exception):
    pass