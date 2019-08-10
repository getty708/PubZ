from django.db import models
# from django.contrib.auth.models import User
from users.models import User


# --------------------------------------------------
class Bibtex(models.Model):
    """ Constants
    """
    LANGUAGE_CHOICES = (
        ('EN', 'English'),
        ('JA', 'Japanese'),
    )
    PRIORITY_CHOICES = (
        ('0', 'Default',),        
        ('5', 'High',),
        ('9', 'Super High',),
    )
    BIBSTYLE_CHOICES = (
        ('AWARD', 'Award',),
        ('KEYNOTE', 'Keynote',),
        ('SAMEASBOOK','Same as the Book'),
    )
    
    """ Fields
    """
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,)
    title_en = models.CharField(max_length=512,null=True,blank=True, default="")
    title_ja = models.CharField(max_length=512,null=True,blank=True, default="")
    authors = models.ManyToManyField(
        'core.Author',
        through='AuthorOrder',
    )
    book = models.ForeignKey(
        'core.Book',
        on_delete=models.PROTECT,
    )
    bib_type = models.CharField(
        max_length=32,
        choices=BIBSTYLE_CHOICES,
        default="SAMEASBOOK",
    )
    book_title = models.CharField(max_length=512,null=True,blank=True, default="")
    volume = models.CharField(max_length=128,null=True,blank=True)
    number = models.CharField(max_length=128, null=True,blank=True)
    chapter = models.IntegerField(null=True,blank=True)
    page = models.CharField(max_length=32, null=True,blank=True)
    edition = models.TextField(max_length=16,null=True,blank=True)
    pub_date = models.DateField(null=True,blank=True,default="2010-01-01")
    use_date_info = models.BooleanField(default=False, blank=True)
    url = models.URLField(null=True,blank=True)
    note = models.TextField(null=True,blank=False)
    memo = models.CharField(max_length=32, null=False,blank=True, default="")
    priority =  models.CharField(
        max_length=1,
        default='0',
        choices=PRIORITY_CHOICES,)
    abstruct = models.TextField(null=True,blank=True)
    tags = models.ManyToManyField(
        'core.Tag',
        through='core.TagChain',
        blank=True,
    )
    is_published = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=False)    
    owner = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL
    )
    
    class Meta:
        unique_together = (
            ("title_en", "book", "pub_date","memo", "page",),
        )
    
    def __str__(self):
        if self.language == 'EN':
            return self.title_en
        elif self.language == 'JA':
            return self.title_ja
        return "Bibtex[{}]".format(self.id)

    @property
    def title(self,):
        if self.language == 'EN':
            return self.title_en
        elif self.language == 'JA':
            return self.title_ja

    @property
    def book_title_display(self):
        if self.book_title:
            return self.book_title
        else:
            return self.book.title

    @property
    def book_abbr_display(self):
        if self.book.abbr:
            return "({abbr} {year})".format(abbr=self.book.abbr, year=self.pub_date.year)
        else:
            return None

    @property
    def bib_type_key(self,):
        if self.bib_type == "SAMEASBOOK":
            return self.book.style
        return self.bib_type

    @property
    def bib_type_display(self,):
        if self.bib_type == "SAMEASBOOK":
            return self.book.get_style_display()
        return self.get_bib_type_display()

    @property
    def authors_list(self,):
        author_list = []
        for author in self.authors.all():
            author_dict = author.__dict__
            author_dict["name"] = author.name_ja if self.language == "JA" else author.name_en            
            author_list.append(author_dict)
        return author_list

    @property
    def author_order_list(self,):
        return self.authororder_set.all().order_by('order')
    
    @property
    def date_str(self):
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
        # These options are removed in the feature
        #('INTPROC', "Int'l Proc.",),  # Alias of `in Proceedings`
        #('JOURNAL', 'Journal',), # Alias of `Article`
        # ('CONF_DOMESTIC', '国内会議',),
        # ('CONF_DOMESTIC_NO_REVIEW', '国内研究会',),
        # ('CONF_NATIONAL', '全国大会'),
        # ('BOOK', 'Book',),        
        #('KEYNOTE', 'Keynote'),  # Alias of `Misc`
        # ('NEWS', 'News Paper',), # Alias of `in Book`
        #('OTHERS', 'Others',),   # Alias of `Misc`
        #('AWARD', 'Award',),     # This will be remobed in the future.
        
        # Official bibtex entries (New)
        #('ARTICLE','Article'),
        ('ARTICLE',(
            ('JOURNAL', 'Journal'),
        ),),
        ('INPROCEEDINGS', (
            ('INPROCEEDINGS', 'International Conference'),
            ('CONF_DOMESTIC', 'Domestic Conference',),
            ('CONF_DOMESTIC_NO_REVIEW', '[Warning!! Change to `Domestic Conference`]国内研究会',),
            ('CONF_NATIONAL', '[Warning!! Change to `Domestic Conference`]全国大会'),
        ),),
        ('BOOK',(
            ('BOOK', 'Book',),
            ('NEWS', 'News Paper',),
        ),),
        ('Removed in the future', (
            ('INTPROC', "[Warning!! Change to `International Conference.`]Int'l Proc.",),
            ('KEYNOTE', '[Warning!]Keynote'),            
            ('AWARD', '[Warning!]Award',),
        ),),
        ('Othres', (
            ('MISC', 'Others'),
            ('ARTICLE', "Article"),            
            ('INBOOK', 'in Book'),            
            ('BOOKLET','Booklet'),
            ('INCOLLECTION', 'in Collection'),
            ('MANUAL', 'Manual'),
            ('MASTERTHESIS','Master Thesis'),
            ('PHDTHESIS','Ph.D Thesis'),
            ('PROCEEDINGS','Proceedings'),
            ('UNPUBLISHED','Unpublished'),
            ('TECHREPORT', 'Tech Report'),            
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
    
