# Application Dashboard

This application provides all usrs to view and seatch function.


## Basic URL Structures

| URI | Usage |
|-----|-------------|
| `^dashboard/$`              |  Root URI of this application |
| `^/dashboard/view/$`        | List view |
| `^/dashboard/view/list/$`   | List view |
| `^/dashboard/view/bibtex/$` | Bibtex style view |
| `^/dashboard/view/table/$`  | Table style view  |
| `^/dashboard/view/tile/$`   | Tile style view   |


## How to Edit Display Style
To change display style {List, Table, Bibtex, Latex}, plsease edit the function in `dashboard/templatetags/utils_bib_fomrat.py`. We provide call back function (implemented as Class Object) for several display formats. When you want to change the style, just overwrite  the `get_template_{TEMPLATE STYLE}` functions.

```python
# Example of Template tag function.
# ---------------------------------

class BibtexFormatListDefault(BibtexFormatBase):
    
    def get_template_INTPROC(self):
        html = (
            '{authors}; '
            '<a href="{url_bib}">"{title}"</a>, '
            '2017'
        )
        return html    

    def get_template_JOURNAL(self):
        html = (
            '{authors}; '
            '<a href="{url_bib}">"{title}"</a>, '
            '2017 '
            '(JOURNAL)'
        )
        return html
```

### Default Style Examples
#### List Style
```
dashboard.templatetags.utils_bib_format.BibtexFormatListDefault
```

##### International Proceedings
```
TBA
```

##### Journal
```
TBA
```

.....





## Search Function
Use search form. 



### memo (東出)
クエリをPOSTするのか，get prameterを使うのかは要検討.

