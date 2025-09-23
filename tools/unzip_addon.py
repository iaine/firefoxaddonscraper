"""
   Classes to unzip FFAdd-On and access the manifest file
"""
from urllib.request import urlretrieve
import zipfile
import json

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Extract():
    '''
       Class functions to extract the files from the XPI archive. 
    '''
    def download_link(xpi_link, dir = "."):
        '''
            Download and unzip a file
            :param xpi_link - the url to the XPI file. 
            :param dir - the directory to extract it all into
        '''
        xpi_filename = xpi_link.split('/')

        urlretrieve(xpi_link, xpi_filename[len(xpi_filename)-1])

        with zipfile.ZipFile(xpi_filename[len(xpi_filename)-1], 'r') as zip_ref:
            zip_ref.extractall(dir)

class Manifest():
    """
        Class to read the Add-On manifest file.
    """

    def __init__(self):
        self.data = ""

    def extract_manifest(self, manifestfile):
        '''
            Return the Manifest as a string
        '''
        data = ""
        with open(manifestfile) as f:
            data = f.read()
        return data
    
    def read_manifest(self, manifestfile):
        '''
            Read the Manifest JSON
        '''
        with open(manifestfile) as f:
            self.data = json.load(f)
    
    def permissions(self):
        '''
            Read the permissions field from read in file
        '''
        if "permissions" in self.data:
            return self.data['permissions']
        
    def name(self):
        '''
            Read the name field from read in file
        '''
        if "name" in self.data:
            return self.data['name']
        
    def addon_version(self):
        '''
            Read the Add-On version field from read in file
        '''
        if "version" in self.data:
            return self.data['version']

    def manifest_version(self):
        '''
            Read the manifest version field from read in file
        '''
        if "manifest_version" in self.data:
            return self.data['manifest_version']  
             
    def default_locale(self):
        '''
            Read the default locale field from read in file
        '''
        if "default_locale" in self.data:
            return self.data['default_locale']
        
    def browser_specific_settings(self):
        '''
            Read the browser specific settings field from read in file
        '''
        if "browser_specific_settings" in self.data:
            return json.dumps(self.data['browser_specific_settings'])
