from django.db import models
from django.contrib.auth.models import User


# --------------------------------------------------
class Bibtex(models.Model):
    """ Constants
    """
    LANGUAGE_CHOICES = (
        ('EN', 'English'),
        ('JA', 'Japanese'),
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
    volume = models.CharField(max_length=128,null=True,blank=True)
    number = models.CharField(max_length=128, null=True,blank=True)
    chapter = models.IntegerField(null=True,blank=True)
    page = models.CharField(max_length=32, null=True,blank=True)
    edition = models.TextField(max_length=16,null=True,blank=True)
    pub_date = models.DateField(null=True,blank=True)
    use_date_info = models.BooleanField(default=False, blank=True)
    acceptance_rate = models.FloatField(null=True,blank=True)
    impact_factor = models.FloatField(null=True,blank=True)
    url = models.URLField(null=True,blank=True)
    note = models.TextField(null=True,blank=True)
    memo = models.CharField(max_length=32, null=True,blank=True)
    abstruct = models.TextField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True, upload_to="api")
    tags = models.ManyToManyField(
        'core.Tag',
        through='core.TagChain',
        blank=True,
    )
    is_published = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=False)    
    owner = models.ForeignKey(
        'auth.User',
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        unique_together = (
            ("title_en", "book", "pub_date","memo",),
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
    def authors_list(self,):
        author_list = []
        
        for author in self.authors.all():
            author_dict = author.__dict__
            author_dict["name"] = author.name_ja if self.language == "JA" else author.name_en            
            author_list.append(author_dict)
        return author_list
    
        
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
        'auth.User',
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
        ('INTPROC', 'International Proceedings',),
        ('JOURNAL', 'Journal Paper',),
        ('CONF_DOMESTIC', 'Domestic Conference',),
        ('CONF_DOMESTIC_NO_REVIEW', 'Domestic Conference (No Review)',),
        ('CONF_NATIONAL', 'National Conference'),
        ('BOOK', 'Book/Review/Editor/Translation',),
        ('KEYNOTE', 'Keynote/Panel Discution/Seminer'),
        ('NEWS', 'New Paper article',),
        ('OTHERS', 'others',),
        ('AWARD', 'Award',),
    )
    
    title = models.CharField(max_length=256)
    abbr  = models.CharField(max_length=256, null=True,blank=True)    
    style = models.CharField(
        max_length=32,
        choices=STYLE_CHOICES,
    )
    institution = models.CharField(max_length=256,null=True,blank=True)
    organizer = models.CharField(max_length=256, null=True,blank=True)
    publisher = models.CharField(max_length=256,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=False)    
    owner = models.ForeignKey(
        'auth.User',
        null=True,
        on_delete=models.SET_NULL
    )

    
    class Meta:
        unique_together = (
            ("title", "style",),
        )

    def __str__(self):
        if self.abbr is not None:
            return self.abbr
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
        'auth.User',
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
        'auth.User',
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
        'auth.User',
        null=True,
        on_delete=models.SET_NULL
    )

    
    class Meta:
        unique_together = (
            ("bibtex", "tag",),
        )
    
