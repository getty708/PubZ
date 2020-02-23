from django import forms
from dal import autocomplete
import re

from core import models
from dashboard import validators

from bootstrap_datepicker_plus import DatePickerInput

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
        self.fields["name_en"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': "English",
        })
        self.fields["name_ja"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': "日本語",
        })
        self.fields["dep_en"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': "English",
        })
        self.fields["dep_ja"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': "日本語",
        })
        self.fields["mail"].widget.attrs.update({
            'class': 'form-control form-control-sm',
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
        name_en = self.clean_base('name_en')
        if ' ' not in name_en:
            raise forms.ValidationError('Please separate your first and last name with a space.')
        return name_en

    def clean_name_ja(self):
        name_ja = self.clean_base('name_ja')
        if name_ja is not None and ' ' not in name_ja:
            raise forms.ValidationError('Please separate your first and last name with a space.')
        return name_ja

    def clean_dep_en(self):
        return self.clean_base('dep_en')

    def clean_dep_ja(self):
        return self.clean_base('dep_ja')

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
            'title','abbr','style','institution','organizer','publisher','address','note',
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
        abbr = self.cleaned_data['abbr']
        if abbr is not None and re.search('[0-9]', abbr):
            raise forms.ValidationError('Do not include year')
        return abbr

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
            'book','book_title','bib_type',
            'volume','number','chapter','page','edition',
            'pub_date','use_date_info', 'is_published',
            'url', 'fund',
            'memo','abstruct',
        ]
        widgets = {
            'book': autocomplete.ListSelect2(
                url='api:autocomplete_book',),
            'pub_date': DatePickerInput(),
        }

    def __init__(self,*args,**kwargs):
        super(BibtexForm,self).__init__(*args,**kwargs)
        for key in self.Meta.fields:
            self.fields[key].widget.attrs.update({
                'class': 'form-control form-control-sm',
            })
        self.fields["book_title"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'disabled': True,
        })            
        self.fields["is_published"].widget.attrs.update({
            'class': 'form-check-input',
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
        empty_label='---',
        widget=autocomplete.ListSelect2(url='api:autocomplete_book')
        )
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



"""
Tag
"""
class TagForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = [
            'name', 'description', 'parent',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        for key in self.Meta.fields:
            self.fields[key].widget.attrs.update({
                'class': 'form-control form-control-sm',
            })


class TagChainForm(forms.ModelForm):
    class Meta:
        model = models.TagChain
        fields = [
            'bibtex', 'tag',
        ]
        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super(TagChainForm, self).__init__(*args, **kwargs)
        for key in self.Meta.fields:
            self.fields[key].widget.attrs.update({
                'class': 'form-control form-control-sm',
            })
