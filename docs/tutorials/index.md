## Tutorials

This goes through how you might approach questions using this tool. 

### Localisation

Localisation is one of the basic digital methods and it can be used for search engines, app stores, and the Firefox Add-On. 

The tool provides access to the language option. This uses a particular style, like en-GB for British English or en-US for American English.

These can be put into a simple list with the same keyword to find different responses from different locales. 

```python

search_term = "privacy"
languages = ['en-GB', 'fr-FR', 'cn-ZH']

for language in languages:
    search_term = "banana"
    addons = scraper.find_software_by_search(search_term, language)
    print(addons)
    addondets = scraper.get_links_details(addons)
    scraper.write_file(addondets, f"{search_term}_{language}_search.csv")
```

The resulting data files, stored where you run the script, can then be analysed to look at the ordering and presence of add-ons. 