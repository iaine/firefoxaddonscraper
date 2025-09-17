## Scraper

### Install

Please use

```bash
pip install git
```

### Methods

The main methods available from the scraper can be accessed by importing the library. 

```python
from firefox import FFScraper

scraper = FFScraper()
```

The Firefox URL has a language option: ```python language = "en-GB" ```

This option is included with the various calls. 

#### Search

Searches can be run using keywords in the interface. 
```python
search_term = "banana"
addons = scraper.find_software_by_search(search_term, language)
print(addons)
addondets = scraper.get_links_details(addons)
scraper.write_file(addondets, "search.csv")
```
This will print a list of URLs that can be expanded by using the link detail calls and then write the details to a file called search. It would be advisable to create a more meaningful name for your own data management. 

#### Categories

The Add-On market has two main areas: extensions and themes. Both of these have categories that collect similar add-ons together. 

The categories can be found using:
```python
category = scraper.find_categories("themes", language)
print(category)
```
Themese can be changed for extensions. 

The categories can then be searched using:
```python
categories = "alerts-updates"
addons = scraper.find_software_by_category(language, "alerts-updates")
print(addons)
addondets = scraper.get_links_details(addons)
scraper.write_file(addondets, "category.csv")
```
This will print a list of URLs that can be expanded by using the link detail calls and then write the details to a file called category. It would be advisable to create a more meaningful name for your own data management.

#### Developers

Sometimes you may want to see what a developer has created. 

```python
devs = scraper.find_developer(language, 1224)
print(devs)
devsdets = scraper.get_links_details(addons)
scraper.write_file(devsdets, "apps_by_developer.csv")
```
This will print a list of URLs that can be expanded by using the link detail calls and then write the details to a file called apps_by_developer. It would be advisable to create a more meaningful name for your own data management.

#### Version History

Add-Ons may have earlier versions posted that can be used to explore the history of any app(s) and to get their details like package size and release dates.

```python
history = scraper.get_version_data("https://addons.mozilla.org/en-GB/firefox/addon/epubreader")
scraper.write_file(history, "version_history.csv")
```
This will print a list of details that is written to a file called version_history. It would be advisable to create a more meaningful name for your own data management.