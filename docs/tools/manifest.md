# Manifest Files

Each XPI file has a manifest file. This class provides functions to read it.

## Extracting the Manifest

Each XPI archive has a manifest file that is written in JSON. This file returns the whole file for processing with your code. 

```python
manifest = Manifest()

manifest.extract_manifest('manifest.json')
```

## Reading the Manifest

Each XPI archive has a manifest file that is written in JSON. This file reads the JSON to allows other functions to get particular data.

```python
manifest = Manifest()

manifest.read_manifest('manifest.json')
```

## Permissions

This code extracts the permissions from field from the read manifest.

```python
manifest = Manifest()

manifest.read_manifest('manifest.json')
permissions = manfest.permissions()
```

## Name

This code extracts the name of the Add-On field from the read manifest.

```python
manifest = Manifest()

manifest.read_manifest('manifest.json')
name = manfest.name()
```

## Add-On version

This code extracts the Add-On version field from the read manifest.

```python
manifest = Manifest()

manifest.read_manifest('manifest.json')
name = manfest.addon_version()
```
This code extracts the name of the Add-On field from the read manifest.

## Manifest 

This code extracts the Manifest version field from the read manifest.
```python
manifest = Manifest()

manifest.read_manifest('manifest.json')
name = manfest.manifest_version()
```

## Default Locale

This code extracts the default locale field from the read manifest.
```python
manifest = Manifest()

manifest.read_manifest('manifest.json')
name = manfest.default_locale()
```

## Browser Specific Settings

This code extracts the browser specific settings field from the read manifest.
```python
manifest = Manifest()

manifest.read_manifest('manifest.json')
name = manfest.browser_specific_settings()
```