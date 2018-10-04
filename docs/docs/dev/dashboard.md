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
[ex.]

Original Bibtex
---------------------------------
@inproceedings{id2741,
         title = {Privacy-Preserving Recognition of Object-based Activities Using Near-Infrared Reflective Markers},
        author = {Joseph Korpela and Takuya Maekawa},
       journal = {ACM/Springer Personal and Ubiquitous Computing (ACM/Springer PUC)},
        volume = {22},
        number = {2},
         pages = {365-377},
         month = {4},
          year = {2018},
}
---------------------------------


List View
---------------------------------
[1] Joseph Korpela and Takuya Maekawa, "Privacy-Preserving Recognition of Object-Based Activities Using Near-Infrared Reflective Markers," ACM/Springer Personal and Ubiquitous Computing (ACM/Springer PUC), volume 22, number 2, pages 365-377 April 2018.
---------------------------------


Bibtex View
---------------------------------
@inproceedings{id2741,
         title = {Privacy-Preserving Recognition of Object-based Activities Using Near-Infrared Reflective Markers},
        author = {Joseph Korpela and Takuya Maekawa},
       journal = {ACM/Springer Personal and Ubiquitous Computing (ACM/Springer PUC)},
        volume = {22},
        number = {2},
         pages = {365-377},
         month = {4},
          year = {2018},
}
---------------------------------


Table View
---------------------------------

|/|著者名(author)|表題(title)|論文誌/会議名|巻号|ページ範囲(pages)|出版年月|JCR/採択率|File|
|----|----|----|----|----|----|----|----|----|
|論文誌|Joseph Korpela, Takuya Maekawa|Privacy-Preserving Recognition of Object-Based Activities Using Near-Infrared Reflective Markers|ACM/Springer Personal and Ubiquitous Computing (ACM/Springer PUC)|22(2)|365-377|2018年4月|||
---------------------------------

```

###  Callback funtion
#### Requrements




### memo (東出)
List, Bibetex, Tableの基本的なviewは吉村が整備．東出はtemplatetagを作成する.



## Search Function
Use search form. 



### memo (東出)
クエリをPOSTするのか，get prameterを使うのかは要検討.

