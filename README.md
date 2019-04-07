# IFB-Tools
Collection of Python CLI Tools for iFormBuilder.

## Tools
- **add-built-in-functions:** Adds 9 built-in functions to a given form (server name, profile id, page id, app name, app version, os type, os version, device model, device language)
- **create-users:** Create iFormBuilder users from a JSON file
- **delete-orphaned-option-lists:** Delete all Option Lists with no assignment in a given profile
- **download-all-records:** Download all records as a JSON file in a given page

## Installation
TO BE ADDED

## Using Existing Tools
TO BE ADDED

## Building New Tools
TO BE ADDED

## iFormBuilder API Calls

### Token Resource
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| POST | Token | requestAccessToken() |

### Profile
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| GET | Profile | getProfile |
| GET | Profiles | getProfiles |
| GET |   | getAllProfiles |
| GET | Company Info | getCompanyInfo |
| POST | Profile | postProfile |

### User
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| POST | Users | postUsers |

### Page
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| GET | Page | getPage |
| GET | Pages | getPages |
| GET |   | getAllPages |

### Option List
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| GET | Option List | getOptionList |
| GET | Option Lists | getOptionLists |
| GET |  | getAllOptionLists |
| DELETE | Option List | deleteOptionList |
| Option List Dependencies | GET | ✓ |

### Option
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| GET | Option | getOption |
| GET | Options | getOptions |
| GET |  | getAllOptions |

### Element
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| GET | Element | getElement |
| GET | Elements | getElements |
| GET |   | getAllElements |
| POST | Elements | postElements |

### Record
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| GET | Record | getRecord |
| GET | Records | getRecords |
| GET |   | getAllRecords |