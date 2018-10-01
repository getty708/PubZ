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


## Display Style
To change display style {List, Table, Bibtex}, plsease edit the function in `~/templatetags/display_style.py`. We are provide call back function for some display formats. When you want to change the style, just change the callback function that you 
want.

```
Example of Template tag function.
---------------------------------

TBA
```

###  Callback funtion
#### Requrements




### memo (東出)
List, Bibetex, Tableの基本的なviewは吉村が整備．東出はtemplatetagを作成する.



## Search Function
Use search form. 



### memo (東出)
クエリをPOSTするのか，get prameterを使うのかは要検討.

