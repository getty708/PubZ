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
        widgets = {
            'dep_en': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
            'dep_ja': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        for key in self.Meta.fields:
            self.fields[key].widget.attrs.update({
                'class': 'form-control form-control-sm',
            })
        for key in ["name", "dep"]:
            for lang in [("en","English",), ("ja","日本語",)]:
                self.fields["{}_{}".format(key, lang[0])].widget.attrs.update({
                    'class': 'form-control form-control-sm',
                    'placeholder': lang[1],
                })

        self.fields["date_join"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': "Date of Join",
        })                
        self.fields["date_leave"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': "Date of Leave",
        })

        
class AuthorOrderForm(forms.ModelForm):
    class Meta:
        model = models.AuthorOrder
        fields = [
            'bibtex','author','order',
        ]

    def __init__(self, *args, **kwargs):
        super(AuthorOrderForm, self).__init__(*args, **kwargs)
        for key in self.Meta.fields:
            self.fields[key].widget.attrs.update({
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
        for key in self.Meta.fields:
            self.fields[key].widget.attrs.update({
                'class': 'form-control form-control-sm',
            })

        # Cutomize
        self.fields["abbr"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': 'abbr',
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
        for key in self.Meta.fields:
            self.fields[key].widget.attrs.update({
                'class': 'form-control form-control-sm',
            })
              
        

        
"""
Registration Form
"""
class BibtexFormStep1(forms.Form):
    # language
    lang = forms.ChoiceField(choices=models.Bibtex.LANGUAGE_CHOICES)
    lang.widget.attrs.update({
            'class': 'form-control form-control-sm',
    })
    # Title
    title = forms.CharField(
        max_length=256,
    )
    title.widget.attrs.update({
        'class': 'form-control form-control-sm',
        'placeholder': "Engilsh / 日本語",
    })
    # Book
    book = forms.ModelChoiceField(
        queryset=models.Book.objects.order_by('style', 'title',),
        empty_label='---')
    book.widget.attrs.update({
            'class': 'form-control form-control-sm',
    })    
    
