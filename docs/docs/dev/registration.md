# Appication Registration

This application provides registration form and support function (ex. autocompetion, update, tagging)

## Basic URL Structure
Root URL = `^dashboard/`

| URL | Action |
|-----|-------------|
| `^list/` | View the papers as a list|
| `^tab/` | View the papers as a table |
| `^latex/` | View the papers in Latex form |
| `^bib/` | View the papers's reference as bib |
| `^<int:pk>/` | View the detail of paper #int |
| `^bib/<int:pk>/` | View the detail of paper #int |
| `^book/` | View the list of books |
| `^book/<int:pk>/` | View the detail of book #int |
| `^author/` | View the list of authors |
| `^author/<int:pk>/` | View the detail of author #int |
| `^notification/alert/` | View the notification/alert |
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
