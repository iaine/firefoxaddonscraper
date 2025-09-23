## Extracting from the archive

There is a function to extract all files from the archive. 

```python
extract = Extract()

xpi_link = "https://addons.mozilla.org/firefox/downloads/file/4532473/adaptive_tab_bar_colour-3.0.xpi"

extract.download_link(xpi_link)
```
You can also set the ```dir``` parameter to a directory of your choice. By default, the function will extract into the directory where you are running your script. 