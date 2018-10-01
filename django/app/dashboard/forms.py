from django import forms


from core import models


"""
Author
"""
class AuthorForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = [
            'name_en','name_ja','dep_en','dep_ja','mail','date_join','date_leave',
        ]

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self.fields["name_en"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["name_ja"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["dep_en"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["dep_ja"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["mail"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["date_join"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["date_leave"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })

        
class AuthorOrderForm(forms.ModelForm):
    class Meta:
        model = models.AuthorOrder
        fields = [
            'bibtex','author','order',
        ]

    def __init__(self, *args, **kwargs):
        super(AuthorOrderForm, self).__init__(*args, **kwargs)
        self.fields["bibtex"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["author"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["order"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        

        
"""
Book
"""
class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = [
            'title','abbr','style','institution','organizer','publisher','address',
        ]


    def __init__(self,*args,**kwargs):
        super(BookForm,self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["abbr"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': 'abbr',
        })
        self.fields["institution"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["organizer"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["publisher"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["address"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })

        

"""
Bibtex
"""
class BibtexForm(forms.ModelForm):
    class Meta:
        model = models.Bibtex
        fields = [
            'language','title_en','title_ja',
            'book','volume','number','chapter','page','edition','pub_date','use_date_info',
            'acceptance_rate','impact_factor','url','note',
            'abstruct','image','is_published',
        ]

    def __init__(self,*args,**kwargs):
        super(BibtexForm,self).__init__(*args,**kwargs)
        print(self.Meta.fields)
        
        self.fields["language"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["title_en"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["title_ja"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["book"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["volume"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["number"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["chapter"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["page"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["edition"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["pub_date"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["use_date_info"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["acceptance_rate"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["impact_factor"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["url"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["note"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["abstruct"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["image"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["is_published"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })        
        

        
