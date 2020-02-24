from django.db import models
from users.models import User


# --------------------------------------------------
class Bibtex(models.Model):
    """ Bibtex object. All information of your publications are represented as this model.

    Attributes:
        id (int): Defined by django app automatically. AutoField, primary key.
        title_ja (django.db.models.CharField): title of your pubilication (Japanese). 
            Check validation rules. (len=512, blank=True)
        authors (django.db.models.ManyToManyField): authors of this publication.
            The order is stored in ``AuthorOrder`` model.
            (model='Author', through='AuthorOrder').
        book (django.db.models.ForeignKey): book object in which this paper is published 
            (e.g. {International proceedings, journals, newspapers, ...}).
            (model='Book')
        book_title (django.db.models.CharField): book title including details (e.g. year).
            (len=512, null=True, blank=True)
        volume (django.db.models.CharField): volume number (巻). Before published, 
            ignore this column.
            (len=128, blank=True)
        number (django.db.models.CharField): number of the book (号). Before published,
            ignore this column.
            (len=128, blank=True)
        chapter (django.db.models.CharField): chapter number (章).
            Before published, ignore this column. 
            (len=128, blank=True)
        page (django.db.models.CharField): page number (章).
            Before published, ignore this column. Check validation rule.
            (len=32, blank=True)
        edition (django.db.models.CharField): edition (版).
            Before published or no longer needed to the format of the publication, 
            ignore this column. Check validation rule.
            (len=128, blank=True)
        pub_date (django.db.models.DateField): date (year, month, date) on which the book
            is published. If date-info is no needed, set 01 to the date field.
            (default="2000-01-01")
        use_date_info (django.db.models.BooleanField): if set True, the date will be 
            displayed. (default: True)
        url (django.db.models.URLField): An URL to PDF or something. (blank=True)
        fund (django.db.models.CharField): information about research funds
            (e.g. JST CREST JPMJCR15E2).
            (len=512, blank=False)
        abstract (django.db.models.TextField): abstract of the paper.
        tags (models.ManyToManyField): tag for this publication. 
            (model='core.Tag', through='core.TagChain')
        is_published (django.db.models.BooleanField): set True when this paper has 
            already published.
            (default=False)
        created (django.db.models.DateTimeField): date and time which this record is created.
            This column is automatically filled by django app.
            (auto_add_now=True)
        modified (django.db.models.DateTimeField): date and time which this object is updated.
            This column is automatically filled by django app.
            (auto_now=True)
        owner (django.db.models.ForeignKey): user who creates this object.
            This column is automatically filled by django app.
            (model='users.User')
        
        LANGUAGE_CHOICES (tuple): choices for an available langauages.
        BIBSTYLE_CHOICES (tuple): bibtex type.
            
            .. csv-table::
                :header: Var, Type, Description
                :widths: 5, 5, 10

                ``AWARD``, Award, TBA
                ``KEYNOTE``, Keynote (Presentation), TBA
                ``SAMEASBOOK``, Same as the Book, TBA

    """

    # Constants
    LANGUAGE_CHOICES = (
        ('EN', 'English'),
        ('JA', 'Japanese'),
    )
    BIBSTYLE_CHOICES = (
        ('AWARD', 'Award',),
        ('KEYNOTE', 'Keynote',),
        ('SAMEASBOOK','Same as the Book'),
    )
    
    # Fields
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        help_text="Default language setting for this publication. (choise={'EN' or 'JA'}")
    title_en = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        default="",
        help_text=(
            "Title of your pubilication (Japanese). Check validation rules."
            "(len=512, blank=True)"
        ))
    title_ja = models.CharField(
        max_length=512, null=True, blank=True, default="",
        help_text=(
            "title of your pubilication (Japanese). "
            "Check validation rules. (len=512, blank=True)"
        ))
    authors = models.ManyToManyField(
        'core.Author',
        through='AuthorOrder',
        help_text=(
            "authors of this publication. The order is stored in ``AuthorOrder`` model."
            "(model='Author', through='AuthorOrder')."
        ))
    book = models.ForeignKey(
        'core.Book',
        on_delete=models.PROTECT,
        help_text=(
            "book title including details (e.g. year). "
            "(len=512, null=True, blank=True)"
        ))
    bib_type = models.CharField(
        max_length=32,
        choices=BIBSTYLE_CHOICES,
        default="SAMEASBOOK",
        help_text=(
            "If this entry is related to an award or a presentation (not article),"
            "set this field."
            "(choose from ``BIBSTYLE_CHOICES``, see note for available choices.)"
        ))
    book_title = models.CharField(
        max_length=512, null=True, blank=True, default="",
        help_text=(
            "book title including details (e.g. year)."
            "(len=512, null=True, blank=True)"
        ))
    volume = models.CharField(
        max_length=128,null=True,blank=True,
        help_text=(
            "volume number (巻). Before published, ignore this column."
            "(len=128, blank=True)"
        ))
    number = models.CharField(
        max_length=128, null=True,blank=True,
        help_text=(
            "number of the book (号). Before published, ignore this column."
            "(len=128, blank=True)"
        ))
    chapter = models.CharField(
        max_length=128, null=True, blank=True,
        help_text=(
            "chapter number (章). Before published, ignore this column. "
            "(len=128, blank=True)"
        ))
    page = models.CharField(
        max_length=32, null=True, blank=True,
        help_text=(
            "page number. Before published, ignore this column. Check validation rule."
            "(len=32, blank=True)"
        ))
    edition = models.CharField(
        max_length=128, null=True, blank=True,
        help_text=(
            "edition (版). Before published or no longer needed to "
            "the format of the publication, ignore this column. Check validation rule."
            "(len=128, blank=True)"
        ))
    pub_date = models.DateField(
        null=True, blank=True, default="2000-01-01",
        help_text=(
            "date (year, month, date) on which the book is published. "
            "If date-info is no needed, set 01 to the date field."
            "(blank=True) (default: 2000-01-01)"
        ))
    use_date_info = models.BooleanField(
        default=False, blank=True,
        help_text=(
            "if set True, the date will be displayed."
            "(default: False)"
        ))
    url = models.URLField(
        null=True, blank=True,
        help_text=(
            "An URL to PDF or something. (blank=True)"
        ))
    fund = models.CharField(
        max_length=512, null=False, blank=True, default="",
        help_text=(
            "information about research fundings"
            "(e.g. JST CREST JPMJCR15E2)."
        ))
    abstruct = models.TextField(
        null=True, blank=True,
        help_text=(
            "abstract of the paper."
            "(blank=True)"
        ))
    memo = models.CharField(
        max_length=32, null=False, blank=True, default="",
        help_text=(
            "note or comment."
            "(blank=True)"
        ))
    tags = models.ManyToManyField(
        'core.Tag', through='core.TagChain',
        blank=True,
        help_text=(
            "tag for this publication. "
            "(model='core.Tag', through='core.TagChain')"
        ))
    is_published = models.BooleanField(
        default=False, blank=True,
        help_text=(
            "set True when this paper has already published."
            "(default: False)"
        ))
    created = models.DateTimeField(
        auto_now_add=True, blank=False,
        help_text=(
            "date and time which this record is created."
            "This column is automatically filled by django app."
            "(auto_add_now=True)"
        ))
    modified = models.DateTimeField(
        auto_now=True, blank=False,        
        help_text=(
            "date and time which this object is updated."
            "This column is automatically filled by django app."
            "(auto_now=True)"
        ))
    owner = models.ForeignKey(
        'users.User',
        null=True, on_delete=models.SET_NULL,
        help_text=(
            "user who creates this object."
            "This column is automatically filled by django app."
            "(model='users.User')"
        ))
    
    class Meta:
        unique_together = (
            ("title_en", "book", "pub_date", "memo", "page",),
        )
    
    def __str__(self):
        if self.language == 'EN':
            return self.title_en
        elif self.language == 'JA':
            return self.title_ja
        return "Bibtex[{}]".format(self.id)

    @property
    def title(self):
        """ Returns a title of this entry in the default language. """
        if self.language == 'EN':
            return self.title_en
        elif self.language == 'JA':
            return self.title_ja

    @property
    def book_title_display(self):
        """ Returns a book title of this entry.
        
        If this enttry has ``book_title`` itself, return it.
        Otherwise, returns a book title of linked ``book`` entry.

        """
        if self.book_title:
            return self.book_title
        else:
            return self.book.title

    @property
    def book_abbr_display(self):
        """ Returns abbribiation text of a linked book. (e.g. (IMWUT 2020)) """
        if self.book.abbr:
            return "({abbr} {year})".format(abbr=self.book.abbr, year=self.pub_date.year)
        else:
            return None

    @property
    def bib_type_key(self):
        """ Returns bibtex type (key).

        Returns:
            str: ``Bitex.BIBTEXSTYLE_CHOICES`` or ``Book.STYLE_CHOICES``
        
        """
        if self.bib_type == "SAMEASBOOK":
            return self.book.style
        return self.bib_type

    @property
    def bib_type_display(self):
        """ Returns bibtex tyepe (display string) 
        
        """
        if self.bib_type == "SAMEASBOOK":
            return self.book.get_style_display()
        return self.get_bib_type_display()

    @property
    def authors_list(self,):
        """ Returns a list of linked core.Author objects.

        Returns:
            list of ``core.Author``

        """
        author_list = []
        for author in self.authors.all():
            author_dict = author.__dict__
            author_dict["name"] = author.name_ja if self.language == "JA" else author.name_en            
            author_list.append(author_dict)
        return author_list

    @property
    def author_order_list(self):
        """ TBA 


        Todo:
            Check whether this property is used or not. If not, remove this.
        
        """
        return self.authororder_set.all().order_by('order')
    
    @property
    def date_str(self):
        """ Returns date in display format.

        Returns:
            str

        """
        if not self.pub_date:
            return "None"
        elif self.use_date_info:
            if self.language == "EN":
                return self.pub_date.strftime("%B %d, %Y")
            else:
                return self.pub_date.strftime("%Y年%m月%d日")
        else:
            if self.language == "EN":
                return self.pub_date.strftime("%B %Y")
            else:
                return self.pub_date.strftime("%Y年%m月")

    @property
    def date_dict(self):
        """ Returns date infomation as dict.

        This dict contains month sting

        Todo:
            Check whether this property is used or not. If not, remove this.        
        
        """
        dict_ret = {
            "original": self.pub_date,
        }
        if self.pub_date:
            dict_ret["year"]  = self.pub_date.year
            dict_ret["month"] = self.pub_date.month
            dict_ret["month_string"] = self.pub_date.strftime("%B")
        else:
            dict_ret["year"] = "None"
            dict_ret["month"] = "None"
            dict_ret["month_string"] = "None"
        return dict_ret                
    

# --------------------------------------------------
class Author(models.Model):
    name_en = models.CharField(max_length=128)
    name_ja = models.CharField(max_length=128, null=True, blank=True)
    dep_en = models.TextField(null=True,blank=True,)
    dep_ja = models.TextField(null=True, blank=True,)
    mail = models.EmailField(null=True, blank=True)
    date_join = models.DateField(null=True, blank=True)
    date_leave = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=False)    
    owner = models.ForeignKey(
        'users.User',
        null=True,blank=False,
        on_delete=models.SET_NULL
    )

    class Meta:
        unique_together = (
            ("name_en", "mail",),
        )
        
    def __str__(self):
        return self.name_en


    @property
    def name(self, lang="EN"):
        if lang == "EN":
            return self.name_en
        else:
            return self.name_ja

    @property
    def dep(self, lang="EN"):
        if lang == "EN":
            return self.dep_en
        else:
            return self.dep_ja
        
        

# --------------------------------------------------
class Book(models.Model):
    STYLE_CHOICES = (
        ('Paper',(
            ('JOURNAL', 'Journal'),
            ('INPROCEEDINGS', 'International Conference'),            
            ('CONF_DOMESTIC', 'Domestic Conference',),            
        ),),
        ('Article', (
            ('BOOK', 'Book',),
            ('NEWS', 'News Paper',),            
            ('MISC', 'Others'),
            ('ARTICLE', "Article"),
        ),),
    )
    
    title = models.CharField(max_length=256)
    abbr  = models.CharField(max_length=256, blank=True, null=False, default="")  
    style = models.CharField(
        max_length=32,
        choices=STYLE_CHOICES,
    )
    institution = models.CharField(max_length=256,null=True,blank=True)
    organizer = models.CharField(max_length=256, null=True,blank=True)
    publisher = models.CharField(max_length=256,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    note = models.TextField(null=True,blank=True)    
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=False)    
    owner = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL
    )

    
    class Meta:
        unique_together = (
            ("title", "style",),
        )

    def __str__(self):
        if self.abbr != "":
            return "{title} ({abbr})".format(title=self.title, abbr=self.abbr)
        return self.title

            
        
        



# --------------------------------------------------
class Tag(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    parent = models.ForeignKey(
        'core.Tag',
        null=True,blank=True,
        on_delete=models.SET_NULL,
    )
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=False)    
    owner = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL,
    )

    
    class Meta:
        unique_together = (
            ("name", "parent",),
        )

    def __str__(self):
        return self.name

  

# --------------------------------------------------
# Intermidiate Models
# 

class AuthorOrder(models.Model):
    bibtex = models.ForeignKey(
        'core.Bibtex',
        on_delete=models.PROTECT,
    )
    author = models.ForeignKey(
        'core.Author',
        on_delete=models.PROTECT,
    )
    order = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=False)    
    owner = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL
    )


    class Meta:
        unique_together = (
            ("bibtex", "order",),
        )

    def __str__(self):
        if self.order == 1:            
            order = "1st"
        elif self.order == 2:
            order = "2nd"
        elif self.order == 3:
            order = "3rd"
        else:
            order = "{}th".format(self.order)
        return "Bibtex[{}] {}".format(self.bibtex.id, order)



# --------------------------------------------------

class TagChain(models.Model):
    bibtex = models.ForeignKey(
        'core.Bibtex',
        on_delete=models.PROTECT,
    )
    tag = models.ForeignKey(
        'core.Tag',
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=False)    
    owner = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL
    )

    
    class Meta:
        unique_together = (
            ("bibtex", "tag",),
        )
    
