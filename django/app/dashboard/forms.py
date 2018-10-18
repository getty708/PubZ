from django import forms
from dal import autocomplete

from core import models
from dashboard import validators



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


    def clean_base(self, key):
        validator_dict = validators.validation_callback_author_form
        val = self.cleaned_data[key]
        if key in validator_dict.keys():
            callback_funcs = validator_dict[key]
            for func in callback_funcs:
                val = func(val)
        return val
        
    def clean_name_en(self):
        return self.clean_base('name_en')

    def clean_name_ja(self):
        return self.clean_base('name_ja')

    def clean_dep_en(self):
        return self.clean_base('name_en')

    def clean_dep_ja(self):
        return self.clean_base('name_en')     
           
    def clean(self):
        cleaned_data = super().clean()        
        return cleaned_data        

        
class AuthorOrderForm(forms.ModelForm):
    class Meta:
        model = models.AuthorOrder
        fields = [
            'bibtex','author','order',
        ]
        widgets = {
            'author': autocomplete.ListSelect2(
                url='api:autocomplete_author',),
        }

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


    def clean_base(self, key):
        validator_dict = validators.validation_callback_book_form
        val = self.cleaned_data[key]        
        if key in validator_dict.keys():
            callback_funcs = validator_dict[key]
            for func in callback_funcs:
                val = func(val)
        return val
        
    def clean_title(self):
        return self.clean_base('title')

    def clean_abbr(self):
        return self.clean_base('abbr')
    
    def clean_institution(self):
        return self.clean_base('institution')
    
            
    def clean(self):
        cleaned_data = super().clean()        
        return cleaned_data        
        
        

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
        for key in self.Meta.fields:
            self.fields[key].widget.attrs.update({
                'class': 'form-control form-control-sm',
            })

    # Validation
    def clean_base(self, key):
        validator_dict = validators.validation_callback_bibtex_form
        val = self.cleaned_data[key]        
        if key in validator_dict.keys():
            callback_funcs = validator_dict[key]
            for func in callback_funcs:
                val = func(val)
        return val
    

    def clean_title_en(self):
        return self.clean_base('title_en')

    def clean_title_ja(self):
        return self.clean_base('title_ja')
    
    def clean_page(self):
        return self.clean_base('page')
    
            
    def clean(self):
        cleaned_data = super().clean()        
        return cleaned_data
            
    
        

        
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


    def clean_base(self, key):
        validator_dict = validators.validation_callback_bibtex_form_step1
        val = self.cleaned_data[key]        
        if key in validator_dict.keys():
            callback_funcs = validator_dict[key]
            for func in callback_funcs:
                val = func(val)
        return val


    def clean_lang(self):
        return self.clean_base('lang')
        
    def clean_title(self):
        return self.clean_base('title')

    def clean_book(self):
        return self.clean_base('book')
    
    def clean(self):
        cleaned_data = super().clean()        
        return cleaned_data

    
