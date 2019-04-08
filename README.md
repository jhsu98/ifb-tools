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
| POST | Profile | createProfile |
| GET | Profile | readProfile |
| GET | Profiles | readProfiles |
| GET | * | readAllProfiles |
| PUT | Profile | updateProfile |
| DELETE | Profile | deleteProfile |
| DELETE | Profiles | deleteProfiles |

| Method | Resource | Function |
|:------:|:--------:|:--------:|
| GET | Company Info | readCompanyInfo |

### User
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| POST | Users | createUsers |
| GET | User | readUser |
| GET | Users | readUsers |
| GET | * | readAllUsers |
| PUT | User | updateUser |
| PUT | Users | updateUsers |
| DELETE | User | deleteUser |
| DELETE | Users | deleteUsers |

### Page
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| POST | Page | createPage |
| GET | Page | readPage |
| GET | Pages | readPages |
| GET | * | readAllPages |
| PUT | Page | updatePage |
| PUT | Pages | updatePages |
| DELETE | Page | deletePage |
| DELETE | Pages | deletePages |

### Element
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| POST | Elements | createElements |
| GET | Element | readElement |
| GET | Elements | readElements |
| GET | * | readAllElements |
| PUT | Element | updateElement |
| PUT | Elements | updateElements |
| DELETE | Element | deleteElement |
| DELETE | Elements | deleteElements |

### Option List
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| POST | Option List | createOptionList |
| GET | Option List | readOptionList |
| GET | Option Lists | readOptionLists |
| GET |  | readAllOptionLists |
| PUT | Option List | updateOptionList |
| PUT | Option Lists | updateOptionLists |
| DELETE | Option List | deleteOptionList |
| DELETE | Option Lists | deleteOptionLists |

| Method | Resource | Function |
|:------:|:--------:|:--------:|
| GET | Option List Dependencies | readOptionListDependencies |

### Option
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| POST | Options | createOptions |
| GET | Option | readOption |
| GET | Options | readOptions |
| GET | * | readAllOptions |
| PUT | Option | updateOption |
| PUT | Options | updateOptions |
| DELETE | Option | deleteOption |
| DELETE | Options | deleteOptions |

### Record
| Method | Resource | Function |
|:------:|:--------:|:--------:|
| POST | Records | createRecords |
| GET | Record | readRecord |
| GET | Records | readRecords |
| GET | * | readAllRecords |
| PUT | Record | updateRecord |
| PUT | Records | updateRecords |
| DELETE | Record | deleteRecord |
| DELETE | Records | deleteRecords |