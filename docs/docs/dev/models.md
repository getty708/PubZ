# Models

-----------
## class **Bibtex**
```
core.models.Bibtex
```

Bibtex object. All information of your publications are represented as this model.

### Properties
+ **id**: Defined by django app automatically. `AutoField`, primary key.
+ **lang**: A default language setting for this publication.
+ **title_en**: A title of your pubilication (English). `CharField(512)`, unique, required. [Check validation rules](#title), blank=True.
+ **title_ja**: A title of your pubilication (Japanese). `CharField(512)`, unique, required. [Check validation rules](#title), blank=True.

!!! Warning
	We have to check whether `title_en` or `title_ja` is provided.
	
+ **authors**: Authors of this publication. This column shall be selected from `Author` model. The order is stored in `AuthorOrder` model, which is an intermediate model for `Bibtex` and `Author`. `ManyToManyField (through='AuthorOrder')`, foreign-key-restriction(`Author`), required.
+ **book**: A book which this work is published. e.g. {International proceedings, journals, newspapers, ...}.`ForeignKey`, foreign-key-restriction(`Book`), required.

+ **volume**: A volume number (巻). Before published, ignore this column. `CharField (max_length=128)`.
+ **number**: A number of the book (号). Before published, ignore this column. `IntegerField`, null=True,blank=True.
+ **chapter**: A chapter number (章). Before published, ignore this column. `IntegerField`, null=True,blank=True.
+ **page**: A cpage number (章). Before published, ignore this column. `TextField`, null=True,blank=True. [Check validation rule](#page).
+ **edition**: An Edition (版).  Before published or no longer needed to the format of the publication, ignore this column. `TextField`, null=True,blank=True. Check validation rule.
+ **pub_date**: A set of {year,month,date} which the book is published. If date-info is no needed, set 01 to the date.
+ **use_date_info**: Whether use date-info or not in the `pub_date` column. `BooleanField`, default=`False`.
+ **acceptance_rate**: If acceptance rate of the book of this time. Set this column when it is available. `FloatField`, default=null.
+ **impact_factor**: Inpact factor (IF). Set the value only when it is available. `FloatField`, default=null.
+ **url**: An URL to PDF or something. `URLField`.
+ **note**: Note. If you need, you can add some text. `TextField`.
+ **abstract**: Abstract of the paper. `TextField`.

!!! Info
	This abstract is used in tile-style display.

+ **image**: A single thumbnail image to represent this publication. This information are used in the [`TileDisplayStyle`](#). `ImageField`.
+ **tags**: Tag for this publication. `ManyToManyField`, foreign-key-restriction(`Tag`), required.
+ **is_published**: Whether it is published or not. `BooleanField`, default=`False`, required.
+ **created**: Datetime which this object is created. This column is automatically filled by django app. `DateTimeField`.
+ **modified**: Datetime which this object is edited last time. This column is automatically filled by django app. `DateTimeField`.
+ **owner**: User who creates this object. This column is automatically filled by django app. `DateTimeField`.



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
| `KEYNOTE` | Presentation/Panel Discution/Seminer | 基調講演/セミナー・パネル討論等 |
| `NEWS`    | New Paper article | 新聞報道記事 |
| `OTHERS`  | others | その他（一般記事等）|
| `AWARD`   | Award | 受賞 |

#### title
TBA

!!! Warning
	**Dev**: How to store information about capital letters.


#### page
TBA

Just a number, or double hyphen notation style (e.g. `100--120`).

#### DB: Unique Restriction
The following set of field shall be unique.  If some of us are accepted in the same domestic conference. please use memo feild to avoid unique restriction.

```
("title_en", "book", "pub_date","memo")
```

!!! Info
	If you regist `Award`, please fill note with your presentation title. Is is neseccary if there are some members who get the same awards.



-----------
## class **Author**
```
core.models.Author
```
This model manages information about authors.

### Properties
+ **id**: Defined by django app automatically. `AutoField`, primary key.
+ **name_en**: Full Name (English). First name and family name should be split by space ([See validation](#name)). `CharField(128)`.
+ **name_ja**: Full Name (Japanese). First name and family name should be split by space ([See validation](#name)). `CharField(128)`, null=True,blank=True.
+ **dep_en**: Depertment Information (English). `TextField`, null=True,blank=True.
+ **dep_ja**: Depertment Information (Japanese). `TextField`, null=True,blank=True.
+ **mail**: E-mail address. `EmailFiled`, null=True,blank=True.
+ **join**: Date which this poerson joinded this department. `DataField`, null=True,blank=True.
+ **leave**: Date which this poerson leave this department. `DateField`, null=True,blank=True.
+ **created**: Datetime which this object is created. This column is automatically filled by django app. `DateTimeField`.
+ **modified**: Datetime which this object is edited last time. This column is automatically filled by django app. `DateTimeField`.
+ **owner**: User who creates this object. This column is automatically filled by django app. `DateTimeField`.

### Validation Rule
#### name
TBA


### DB: Unique Restriction
The following set of field shall be unique. 

```
("name_en", "deb_en", "mail",)
```

-----------
## class **AuthorOrder**
```
core.models.AuthorOder
```

### Properties
+ **id**: Defined by django app automatically. `AutoField`, primary key.
+ **bibtex**: Bibtex id. `ForeignKey()`, foreign-key-restriction(`Bibtex`), required.
+ **author**: Author id. `ForeignKey()`, foreign-key-restriction(`Author`), required.
+ **order**: Order of Author. `PositiveSmallIntegerFeild`.
+ **created**: Datetime which this object is created. This column is automatically filled by django app. `DateTimeField`.
+ **modified**: Datetime which this object is edited last time. This column is automatically filled by django app. `DateTimeField`.
+ **owner**: User who creates this object. This column is automatically filled by django app. `DateTimeField`.

### Validation Rule
### DB: Unique Resturiction
The following set of field shall be unique. 

```
("bibtex", "author",),
```


-----------
## class **Book**
```
core.models.Book
```
This model stores information about publications.


### Properties
+ **id**: Defined by django app automatically. `AutoField`, primary key.
+ **title**: Book title (full). Some words should be replaced based on the local rules. [See validation](#title). `CharField`, required.
+ **abbr**: Book title (Abbreviation). Some words should be replaced based on the local rules. [See validation](#title). `CharField`, null=True,blank=True.
+ **style**: Publication Type. See [Validation/type](#type) for the avaiable choises. `CharField(64) with choices`.

!!! Warning
	Double inputs. Select where to place this column, Bibtex or Book
+ **institution**: Institution (). `CharField(256)`, null=True,blank=True.
+ **organizer**: An ornaizer of this Book. `CharField(256)`, null=True,blank=True.
+ **publisher**: A publisher of this Book. `CharField(256)`, null=True,blank=True
+ **address**: An address of this publisher. `CharField(512)`, null=True,blank=True.

!!! Warning
	Do we really need this column? Check it to Prof.



### Validation Rule
#### title
TBA

If you want to chage these rule, check [TBA page](#)

!!! Warning
	We should select whether the information about year etc.. should be placed. If we palce them in `Bibtex` model, `Book` model shall not have such information. Otherwise if we place them in the `Book` object, we shall make copy function to make new `Book` obeject from previous year's one with ease.

#### abbr
TBA

#### institude
TBA


### DB: Unique Resturiction
The following set of field shall be unique. 


```
("name", "parent",),
```



-----------
## class **Tag**
```
core.models.Tag
```

Add tags to bibtex. This model is used in search, web embedding API.

### Properties
+ **id**: Defined by django app automatically. `AutoField`, primary key.
+ **name**: A tag name. `CharField(128)`
+ **description**: A description for this tag.
+ **parent**: Parent Tag of this. `ForeignKey`, foreign-key-restriction(`Tag`), required.
+ **created**: Datetime which this object is created. This column is automatically filled by django app. `DateTimeField`.
+ **modified**: Datetime which this object is edited last time. This column is automatically filled by django app. `DateTimeField`.
+ **owner**: User who creates this object. This column is automatically filled by django app. `DateTimeField`.

### Validation Rules
### DB: Unique Resturiction
The following set of field shall be unique. 

```
("name", "parent",),
```



----------
## class **TagChain**

```
core.models.TagChain
```

This is a relation schema between Bibtex and Tag.

### Properties
+ **id**: Defined by django app automatically. `AutoField`, primary key.
+ **bibtex**: Bibtex id. `ForeignKey()`, foreign-key-restriction(`Bibtex`), required.
+ **tag**: Bibtex id. `ForeignKey()`, foreign-key-restriction(`Tag`), required.
+ **created**: Datetime which this object is created. This column is automatically filled by django app. `DateTimeField`.
+ **modified**: Datetime which this object is edited last time. This column is automatically filled by django app. `DateTimeField`.
+ **owner**: User who creates this object. This column is automatically filled by django app. `DateTimeField`.


### Validation
### DB: Unique Resturiction
The following set of field shall be unique. 

```
("name", "parent",),
```


