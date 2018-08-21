from django.db import models


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
    language = model.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,)
    title_en = model.CharField(max_length=512)
    title_ja = model.CharField(max_length=512)
    authors = model.ManyToManyField()
    book = model.ManyToManyField()
    volume = model.IntergerField(null=True)
    number = model.IntergerField(null=True)
    chapter = model.IntergerField(null=True)
    page = model.TextField(max_length=16)
    edition = model.TextField(max_length=16)
    pub_date = model.DateField()
    is_date = model.BooleanField()
    acceptance_rate = model.FloatField(null=True)
    inpact_factor = model.FloatField(null=True)
    url = model.UrlField(null=True)
    note = model.TextField(null=True)
    abstruct = model.TextField(null=True)
    image = model.ImageField(null=True)
    tags = model.ManyToManyField()    
    is_published = model.BooleanField()
    
    


# --------------------------------------------------
class Author(models.Model):
    name_en = models.CharField(max_length=128)
    name_ja = models.CharField(max_length=128)
    dep_en = models.TextField(null=True)
    dep_ja = models.TextField(null=True)
    mail = models.EmailFiled()
    date_join = models.DateField()
    date_leave = models.DataField()    



# --------------------------------------------------
class Book(models.Model):
    title = models.CharField(max_length=256)
    style = models.CharField(max_length=8)
    institution = models.CharField(max_length=256)
    publisher = models.CharField(max_length=256)
    adderss = models.TextField()
    




# --------------------------------------------------
class Tag(models.Model):
    name = models.CharFeild(max_length=32)
    description = models.TextField()
