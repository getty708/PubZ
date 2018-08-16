# Models

-----------
## class **Bibtex**
```
TBA
```

Bibtex object. All information of your publications are represented as this model.

### Properties
+ **id**: Defined by djnago app automatically. `AutoField`, primary key.
+ (**type**: Publication Type. See [Validation/type](#type) for the avaiable choises. `CharField(64) with choices`.)

!!! Warning
	Double inputs. Select where to place this columns, Bibtex or Book

+ **lang**: A default language setting for this publication.
+ **title_en**: A title of your pubilication (English). `CharField(512)`, unique, required. [Check validation rules](#title)
+ **title_ja**: A title of your pubilication (Japanese). `CharField(512)`, unique, required. [Check validation rules](#title)

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
+ **Image**: A signle thumbnail iamge to represent this publication. This information are used in the [`TyleDisplayStyle`](#). `ImageField`.
+ **tags**: Tag for this publication. `ManyToManyField`, foreign-key-ristriction(`Tag`), required.

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
This model manages infomation about authors.

### Properties
+ **id**: Defined by djnago app automatically. `AutoField`, primary key.
+ **name_en**: Full Name (English). First name and family name should be split by space ([See validation](#name)). `CharField(128)`.
+ **name_ja**: Full Name (Japanese). First name and family name should be split by space ([See validation](#name)). `CharField(128)`.
+ **dep_en**: Depertment Infomation (English). `TextField`, required.
+ **dep_ja**: Depertment Infomation (Japanese). `TextField`, null=True.
+ **mail**: E-mail address. `EmailFiled`.
+ **join**: Date which this poerson joinded this department. `DataField`, null=True.
+ **leave**: Date which this poerson leave this department. `DateField`, null=True.


### Validation Rule
#### name
TBA


-----------
## class **Book**
```
TBA
```
This model stores information about publications.


### Properties
+ **id**: Defined by djnago app automatically. `AutoField`, primary key.
+ **title**: Book tiltle (full). Some words should be replaced based on the local rules. [See validation](#title). `CharField`, required.
+ **type**: Publication Type. See [Validation/type](#type) for the avaiable choises. `CharField(64) with choices`.

!!! Warning
	Double inputs. Select where to place this columns, Bibtex or Book
+ **institution**: Institution (). `CharField(256)`
+ **organizer**: An ornaizer of this Book. `CharField(256)`
+ **publisher**: A publisher of this Book. `CharField(256)`
+ **address**: An address of this publisher. `CharField(512)`

!!! Warning
	Do we really need this column? Check it to Prof.



### Validation Rule
#### title
TBA

If you want to chage these rule, check [TBA page](#)

!!! Warning
	We should select whether the information about year etc.. should be placed. If we palce them in `Bibtex` model, `Book` model shall not have such infomation. Otherwise if we place them in the `Book` object, we shall make copy function to make new `Book` obeject from previous year's one with ease.



-----------
## class **Tag**
```
TBA
```

Add tags to bibtex's. This model is used in search, web emedding API.

### Properties
+ **id**: Defined by djnago app automatically. `AutoField`, primary key.
+ **name**: A tag name. `CharField(128)`
+ **description**: A description for this tag.
+ (**bib**: Specify a publication. `ForeignKey`, foreign-key-ristriction(`Bibtex`), required.)

### Validation Rules
TBA


-----------
## class **Meta**
```
TBA
```

TBA



