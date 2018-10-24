# Appication Registration

This application provides registration form and support function (ex. autocompetion, update, tagging)

## Basic URL Structure
Root URL = `^dashboard/`

| URL | Action |
|-----|-------------|
| `^add/` | Add new bibtex object |
| `^add/step1/` | Start to add new bibtex object (this function will be integrated with `^add/`) |
| `^edit/<int:bibtex_id>/` | Edit bibtex object |
| `^author/add` | Add new author object |
| `^author/edit/<int:book_id>` | Edit the author object |
| `^book/add` | Add new book object |
| `^book/edit/<int:book_id>` | Edit the book object |


## Bibtex Registration Flow
### Step.1 Register Title and Book (and Number of Authors)
Just provide `language, title, book`. In the next page, our app returns you a form with some guides (e.g. Requrired or Not)
(Validation and user check)


### Step2. Register Book Infomation if needed.
TBA


### Step.3 Edit detail of Bibtex
Register detail information of the bib object. Validation is performed afeter click send button.
(Validation and user check)





## Validation 
In this section, we are going to describe how to edit and apply validation rules in this application.
Validation rules for each field are described in [Model](./models.md). Please check it.


### Where should you write validation rules?
Pleas edit `dashboard/validators.py` to implement validation rules. The rules are expressed as function. For clarity, function names shall obey the following setting.

```python
def val_<field name of model/form field >_<short discription>(val):
	"""
	Returns.
	--------
	- <Detail discritption about values to be returned >
	"""
	# Rules here!
	return val_checked
	

# ----------------
def val_bibtex_title_en_replace_keywords(val):
	""" 
	Return.
	------
    - Title string, some keywords are replaced with registerd format
    (e.g. Conference => Conf., International => Int'l.)
	
	"""
	# Write Validation Rule
	return title_checked
```

!!! Info
	Each rule funtion shall check a single rule, not multiple. If you want to apply severel validation rules, you should devide the funtion and register them.
	
	
