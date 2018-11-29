# Data Importer via REST API
You can add athor, book, bibtex, author-order info from CSV. This code use REST API. I implemeted this with no spleep time because these codes are expected internal use. Please do not use for production server.
 

## Usage
**Important** Please execte as superuser!

**Important** Please execte these command in this order!

### Add Author
#### CSV Format
First you should prepare CSV which contains following columns.

+ name\_en
+ name\_ja
+ dep\_en
+ dep\_ja
+ mail

#### Execution

```
$ python authors.py CSV -u < user name> -f <path to the CSV> 
```

you can check help text by `python authors.py -h`.


### Add Book Info
#### CSV Format

+ title
+ abbr
+ style


#### Execution

```
$ python book.py CSV -u < user name> -f <path to the CSV>
```

you can check help text by `python authors.py -h`.


### Add Bibtex Info
#### CSV Format

+ bib\_language
+ bib\_title
+ bib\_volume
+ bib\_number
+ bib\_chapter
+ bib\_page
+ bib\_edition
+ bib\_pub\_date
+ bib\_use\_data\_info
+ bib\_url
+ bib\_note
+ bib\_memo
+ book\_title
+ keys\_author
+ key\_tag
+ series
+ key\_book\_style

#### Execution

```
$ python bibtex.py CSV -u < user name> -f <path to the CSV>
```

you can check help text by `python bibtex.py -h`.


### Add Bibtex Info
#### CSV Format

+ book\_title
+ keys\_author
+ series


#### Execution

```
$ python author_order.py CSV -u < user name> -f <path to the CSV>
```

you can check help text by `python bibtex.py -h`.
