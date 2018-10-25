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
### Step 1. Register Title and Book <!-- (and Number of Authors) -->
<!--
Just provide `language, title, book`. In the next page, our app returns you a form with some guides (e.g. Requrired or Not)
(Validation and user check)
-->

1. Press __`Add New Bib`__ to register a new Bibtext into our system.  
2. For the first step, you need to choose the __`Language`__, input the __`Title`__ and choose the __`Book`__.  
3. If the __`Book`__ is not included in our system, please press __`Add New Book`__, and refer __[Step 2]__. 
4. Press __`Add New`__ button and continue the registration.  


### Step 2. Register Book Infomation (if necessary).
1. Please fill in the form with the book's information.
2. After press the 'Register' button, you can see the list of all the registered book.
3. Go back to the Bib registration page, and choose the new-registered book from the list.  


### Step 3. Edit detail of Bibtex
<!--Register detail information of the bib object. Validation is performed afeter click send button.
(Validation and user check)
-->

1. The __`Language`__, __`Title`__ and __`Book`__ will be filled in automatically.
2. Please fill in the table with other informatin of the Bibtex.
3. Press __`Update`__ button to finish the registration, and then you can see the list of all the regisgered Bibtex.



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


