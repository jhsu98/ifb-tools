# IFB-Tools
Collection of Python CLI Tools for iFormBuilder.

## Tools
- **add-built-in-functions:** Adds 9 built-in functions to a given form (server name, profile id, page id, app name, app version, os type, os version, device model, device language)
- **create-users:** Create iFormBuilder users from a JSON file
- **delete-orphaned-option-lists:** Delete all Option Lists with no assignment in a given profile
- **download-all-records:** Download all records as a JSON file in a given page
- **form-search:** Multi-profile search for forms matching a fuzzy search

## Installation
To install the IFB Tools, first make sure Python3+ is [installed](https://realpython.com/installing-python/)

Once Python3 has been installed, use PIP to install the [ifb-wrapper](https://github.com/jhsu98/ifb-wrapper)

```pip install ifb-wrapper```
or
```pip3 install ifb-wrapper```

Lastly, clone the [repository](https://github.com/jhsu98/ifb-tools) or download the [zip file](https://github.com/jhsu98/ifb-tools/archive/master.zip)