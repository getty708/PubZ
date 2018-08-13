# Models

-----------
## class **Bibtex**
```
TBA
```

Bibtex object. All information of your publications are represented as this model.

### Properties
+ **id**: Defined by djnago app automatically. `AutoField`, primary key.
+ **type**: Publication Type. See [Validation/type](#type) for the avaiable choises. `CharField(64) with choices`.
+ **title**: A title of your pubilication. `CharField(512)`, unique, required. [Check validation rules](#title)
+ **title_e**: A title (English ver.). This column should be filled whether it is same as `title`. `varchar(512)`.

!!! Warning
	If there are more English displays than Japanese, "title" is fixed to write in English.
	
+ **authors**: Auhtors of this pubilcation. This columns shall be selected from `Author` model. `ManyToManyField`, foreign-key-ristriction(`Author`), required.

!!! Warning
	We should discuss how to store the order of authors.

+ **book**: A book which this work is published. e.g. {International proceedings, journals, news papers, ...}.`ForeignKey`, foreign-key-ristriction(`Book`), required.

+ **volume**: A volume number (巻). Before published, ingnore this columns. `IntegerField`.
+ **number**: A number of the book (号). Before published, ignore this columns. `IntegerField`, null=True.
+ **chapter**: A chapter number (章). Before published, ignore this columns. `IntegerField`, null=True.
+ **page**: A cpage number (章). Before published, ignore this columns. `TextField`, null=True. [Check validation rule](#page).
+ **edition**: An Edition (版).  Before published or no longer needed to the format of the publication, ignore this columns. `TextField`, null=True. Check validation rule.
+ **pub_date**: A set of {year,month,date} which the book is published. If date-info is no needed, set 01 to the date.
+ **is_date**: Whether use date-info or not in the `pub_date` column. `BooleanField`, default=`False`.
+ **acceptance_rate**: If acceptance rate of the book of this time. Set this columns when it is available. `FloatField`, default=null.
+ **impact_factor**: Inpact factor (IF). Set the value only when it is available. `FloatField`, default=null.
+ **url**: An URL to PDF or something. `URLField`.
+ **note**: Note. If you need, you can add some text. `TextField`.
+ **abstruct**: Abstruct of the paper. `TextField`. 

!!! Info
	This abstuct is used in tile-style display.

+ **is_published**: Whether it is published or not. `BooleanField`, default=`False`, required.




### Validaion Rules
#### type
Select form followings.

| Var       | Type | Description |
|-----------|------|-------------|
| `INTPROC` | International Proceedings | 国際会議 |
| `JOURNAL` | Journal Paper | 論文誌 |
| `CONF_DOMESTIC` | Domestic Conference  |国内会議 (査読付き) |
| `CONF_DOMESTIC_NO_REVIEW` | Domestic Conference |国内研究会 |
| `CONF_NATIONAL` | National Conference | 全国大会 |
| `BOOK`    | Book/Review/Editor/Translation | 著書／監修／編集／訳書|
| `KEYNOTE` | Presentaion/Panel Discution/Seminer | 基調講演/セミナー・パネル討論等 |
| `NEWS`    | New Paper article | 新聞報道記事 |
| `OTHERS`  | others | その他（一般記事等）|
| `AWARD`   | Award | 受賞 |

#### title
TBA

!!! Warning
	**Dev**: How to store infomation about capital letters.


#### page
TBA

Just a number, or double hyphen notation style (e.g. `100--120`).





-----------
## class **Author**
```
TBA
```


-----------
## class **Book**
```
TBA
```


-----------
## class **Meta**
```
TBA
```

-----------
## class **Tag**
```
TBA
```
