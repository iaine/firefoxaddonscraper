'''
   Firefox Add-On Market

   Does history, search, category, & add-on version history
'''

import ssl 
from urllib.request import urlopen
import json
from bs4 import BeautifulSoup

import pandas as pd


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
        
        base = f"https://addons.mozilla.org/api/v5/addons/search/?app=firefox&author={userid}&page=1&page_size=10&sort=users&type=extension&lang={language}"
        data = urlopen(base, timeout=10)
        results = json.loads(data.read().decode('utf-8'))

        appresults = []
        for result in results['results']:
            app = {}
            authornames = []
            authorurls = []
            for author in result['authors']:
                authornames.append(author['name'])
                authorurls.append(author['url'])
            app['authornames'] = ";".join(authornames)
            app['authorurls'] = ";".join(authorurls)
            app['categories'] = ";".join(result['categories'])
            app['url'] = result['current_version']['file']['url']
            app['permissions'] = ";".join(result['current_version']['file']['permissions'])
            app['optpermissions'] = ";".join(result['current_version']['file']['optional_permissions'])
            app['hostpermissions'] = ";".join(result['current_version']['file']['host_permissions'])
            app['datapermissions'] = ";".join(result['current_version']['file']['data_collection_permissions'])
            app['licenseurl'] = result['current_version']['license']['url']
            app['releasenotes'] = result['current_version']['release_notes']
            app['privacy'] = result['has_privacy_policy']
            keys = list(result['description'].keys())
            app['description'] = result['description'][keys[0]]
            keys = list(result['homepage']['url'].keys())
            app['home'] = result['homepage']['url'][keys[0]]
            keys = list(result['name'].keys())
            app['name'] = result['name'][keys[0]]
            app['last'] = result['last_updated']
            app['ratingscount'] = result['ratings']['average']
            app['ratingsnumber'] = result['ratings']['count']
            app['ratingstext'] = result['ratings']['text_count']
            keys = list(result['summary'].keys())
            app['summary'] = result['summary'][keys[0]]
            app['tags'] = ";".join(result['tags'])
            app['versions'] = result['versions_url']
            app['downloads'] = result['weekly_downloads']

            appresults.append(app)
            
        return appresults

    def find_categories(self, addontype, language=""):
        '''
            Get Categories
        '''
        categories = []
        if language == "":
            raise ScraperException("No language given. Please use a code like en-GB or cn-ZH")
        
        base = f"https://addons.mozilla.org/{language}/firefox/{addontype}/"
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

        data = urlopen(url + '/versions', timeout=10)

        htmlParse = BeautifulSoup(data, 'html.parser')
        
        for lnk in htmlParse.find_all("li", {'class': 'AddonVersionCard'}):
            history = {}
            history['version'] = lnk.find('h2', {'class': 'AddonVersionCard-version'}).get_text()
            release = lnk.find('div', {'class': 'AddonVersionCard-fileInfo'}).get_text().split(' - ')
            history['releaseDate'] = release[0]
            history['releaseSize'] = release[1]
            history['platform'] = lnk.find('div', {'class': 'AddonVersionCard-compatibility'}).get_text()
            note = lnk.find('div', {'class': 'AddonVersionCard-releaseNotes'})
            if note is not None:
                history['notes'] = note.get_text()
            else:
                history['notes'] = ""
            if note.find('a') is not None:
                history['noteslink'] = note.find('a').get('href')
            else:
                history['noteslink'] = ""
            
            license = lnk.find('div', {'class': 'AddonVersionCard-license'})
            if license is not None:
                history['license'] = license.get_text()
            else:
                history['license'] = ""
            history['download'] = lnk.find('div', {'class': 'InstallButtonWrapper-download'}).find('a').get('href')
            
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
        
        if htmlParser.find('h4',{'class':'PermissionsCard-subhead--required'}) != None:
            reqs = []
            for req in htmlParser.find_all('li',{'class':'Permission'}): reqs.append(req.get_text())
            details['requiredpermissions'] = ";".join(reqs)
        else:
            details['requiredpermissions'] = ""
        
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
            
        history = htmlParser.find('dd',{'class':'AddonMoreInfo-version-history'})
        if history is not None:
            details['history'] = history.find('a').get('href')
        else:
            details['history'] = ""
        return details

    def get_links_details(self, linksarray):
        '''
        Get the detail pages from a links array
        '''
        details = []
        for l in linksarray:
            details.append(self.get_link_details(l))
        return details

    def write_file(self, data, filename):
        ''' Write to CSV '''
        df = pd.DataFrame(data)

        df.to_csv(filename, index=False)
    
class ScraperException(Exception):
    pass