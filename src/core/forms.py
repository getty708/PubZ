import re
from django import forms

from dal import autocomplete
from bootstrap_datepicker_plus import DatePickerInput

from core import models
# from core import validators


"""
Author
"""


class AuthorForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = [
            'name_en', 'name_ja',
            'affiliation_en', 'affiliation_ja',
            'mail', 'date_join', 'date_leave',
        ]
        widgets = {
            'affiliation_en': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
            'affiliation_ja': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self.fields["name_en"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': "FamilyName, FirstName (MiddleName)",
        })
        self.fields["name_ja"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': "姓 名",
        })
        self.fields["affiliation_en"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': "English",
        })
        self.fields["affiliation_ja"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': "日本語",
        })
        self.fields["mail"].widget.attrs.update({
            'class': 'form-control form-control-sm',
        })
        self.fields["date_join"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': "e.g. 2020-01-01",
        })
        self.fields["date_leave"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': "e.g. 2020-01-01",
        })

    def clean_name_en(self):
        """ Validate an author name (English).

        Remove full-witdh space. 

        """
        print('clean_name_en is called.')
        name_en = self.cleaned_data['name_en']
        # Replace full-with space with normal space.
        name_en = name_en.replace("　", " ")

        # Check space
        if ' ' not in name_en:
            raise forms.ValidationError(
                'Please separate your first and last name with a space.')

        # Auto cleaning
        name_en = [s.strip().title() for s in name_en.split()]
        name_en = " ".join(name_en)
        return name_en

    def clean_name_ja(self):
        """ Validate au author name (Japanese) """
        name_ja = self.cleaned_data['name_ja']
        if name_ja is None:
            return None
        # Replace full-with space with normal space.
        name_ja = name_ja.replace("　", " ")

        # check space
        if ' ' not in name_ja:
            raise forms.ValidationError(
                'Please separate your first and last name with a space.')
        # remove comma from Japanese name.
        if name_ja:
            name_ja = [s.strip().replace(",", "").title()
                       for s in name_ja.split()]
            name_ja = " ".join(name_ja)
        return name_ja

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class AuthorOrderForm(forms.ModelForm):
    class Meta:
        model = models.AuthorOrder
        fields = [
            'bibtex', 'author', 'order',
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
            'title', 'abbr', 'style',
            'publisher', 'note',
        ]

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for key in self.Meta.fields:
            self.fields[key].widget.attrs.update({
                'class': 'form-control form-control-sm',
            })

        # Cutomize
        self.fields["abbr"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': 'e.g. CVPR',
        })

    def clean_title(self):
        """ Validate book title. 


        Note:
            Replace following word with the complete form.

            * To ``Conference`` : conference, Conf., conf.
            * To ``Transactions on`` : Trans. on, trans. on, Trans., trans., Transaction on, transaction on
            * To ``Proceedings of`` : in Proceeding of, in proceeding of, in Proc. of, in proc. of, Proc. of, proc. of, Proc., proc.,
            * To ``International`` : international, Int'l, int'l, Intl, intl       

        """
        # Replace some words.
        title = self.cleaned_data['title']
        CHECK_DICT = {
            "Conference": [
                "conference", "Conf.", "conf.",
            ],
            "Transactions on": [
                "Trans. on", "trans. on", "Trans.", "trans.",
                "Transaction on", "transaction on",
            ],
            "Proceedings of": [
                "in Proceeding of", "in proceeding of",
                "in Proc. of", "in proc. of", "Proc. of", "proc. of",
                "Proc.", "proc.",
            ],
            "International": [
                "international", "Int'l", "int'l", "Intl", "intl",
            ],
        }
        for key, value in CHECK_DICT.items():
            for v in value:
                title = title.replace(v, key)

        # Convert to Title case.
        return title.strip()

    def clean_abbr(self):
        """ Vlidate abbr.

        Raise:
            form.validationError: If the abbr string contains 0-9.

        """
        abbr = self.cleaned_data['abbr']
        if abbr is not None and re.search('[0-9]', abbr):
            raise forms.ValidationError('Do not include year.')
        return abbr

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


"""
Bibtex
"""


class BibtexForm(forms.ModelForm):
    """

    Todo:
        Implement ``self.clean_title_en()``

    """

    class Meta:
        model = models.Bibtex
        fields = [
            'language', 'title_en', 'title_ja',
            'book', 'book_title', 'bib_type',
            'volume', 'number', 'chapter', 'page', 'edition',
            'pub_date', 'use_date_info', 'is_published',
            'url', 'fund', 'doi',
            'memo', 'abstract',
        ]
        widgets = {
            'book': autocomplete.ListSelect2(
                url='api:autocomplete_book',),
        }

    def __init__(self, *args, **kwargs):
        super(BibtexForm, self).__init__(*args, **kwargs)
        for key in self.Meta.fields:
            self.fields[key].widget.attrs.update({
                'class': 'form-control form-control-sm',
            })
        self.fields["title_en"].widget.attrs.update({
            'placeholder': '(If this entry has no English title, leave this as blank.)',
        })
        self.fields["title_ja"].widget.attrs.update({
            'placeholder': '(日本語のタイトルがない場合は空欄)',
        })
        self.fields["book_title"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'disabled': True,
        })
        self.fields["volume"].widget.attrs.update({
            'placeholder': 'Volume',
        })
        self.fields["number"].widget.attrs.update({
            'placeholder': 'Number',
        })
        self.fields["chapter"].widget.attrs.update({
            'placeholder': 'Chapter',
        })
        self.fields["pub_date"].widget.attrs.update({
            'class': 'form-check-input',
            'placeholder': 'YYYY-mm-dd',
        })
        self.fields["is_published"].widget.attrs.update({
            'class': 'form-check-input',
        })

    # TODO: Implement title validator.
    def clean_title_en(self):
        title_en = self.cleaned_data['title_en']
        return title_en

    def clean_page(self):
        """

        Example:
            >>> page = "1--4"
            Ok
            >>> page = "1-4"
            returns 1--4

        """
        page = self.cleaned_data['page']
        if page is None:
            return None
        if '-' in page and not '--' in page:
            page = page.replace('-', '--')
        return page

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
