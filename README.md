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
| POST | Profile | postProfile |
| GET | Profile | getProfile |
| GET | Profiles | getProfiles |
| GET | * | getAllProfiles |
| GET | Company Info | getCompanyInfo |
| DELETE | Profile | deleteProfile |
| DELETE | Profiles | deleteProfiles |

### User
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| POST | Users | postUsers |
| GET | User | getUser |
| GET | Users | getUsers |
| GET | * | getAllUsers |

### Page
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| POST | Page | postPage |
| GET | Page | getPage |
| GET | Pages | getPages |
| GET | * | getAllPages |
| DELETE | Page | deletePage |
| DELETE | Pages | deletePages |

### Element
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| POST | Elements | postElements |
| GET | Element | getElement |
| GET | Elements | getElements |
| GET | * | getAllElements |
| DELETE | Element | deleteElement |
| DELETE | Elements | deleteElements |

### Option List
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| POST | Option List | postOptionList |
| GET | Option List | getOptionList |
| GET | Option Lists | getOptionLists |
| GET |  | getAllOptionLists |
| DELETE | Option List | deleteOptionList |
| DELETE | Option Lists | deleteOptionLists |
| GET | Option List Dependencies | getOptionListDependencies |

### Option
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| POST | Options | postOptions |
| GET | Option | getOption |
| GET | Options | getOptions |
| GET | * | getAllOptions |
| DELETE | Option | deleteOption |
| DELETE | Options | deleteOptions |

### Record
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| POST | Records | postRecords |
| GET | Record | getRecord |
| GET | Records | getRecords |
| GET |   | getAllRecords |
| DELETE | Record | deleteRecord |
| DELETE | Records | deleteRecords |