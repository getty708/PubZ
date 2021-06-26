import datetime

from django.db import models


# --------------------------------------------------
class Bibtex(models.Model):
    """Bibtex object. All information of your publications are represented as this
    model.

    Possible choices for ``bib_style`` filed are follows.

    .. csv-table::
        :header: Var, Type, Description
        :widths: 5, 5, 10

        ``AWARD``, Award, 受賞
        ``KEYNOTE``, Keynote (Presentation), 基調講演/セミナー・パネル討論等
        ``SAMEASBOOK``, Same as the Book,

    """

    # Constants
    LANGUAGE_CHOICES = (
        ("EN", "English"),
        ("JA", "Japanese"),
    )
    BIBSTYLE_CHOICES = (
        (
            "AWARD",
            "Award",
        ),
        (
            "KEYNOTE",
            "Keynote",
        ),
        (
            "MISC",
            "Others",
        ),
        ("SAMEASBOOK", "Same as the Book"),
    )

    # Fields
    # Todo: change this filed to title/title_secondary and language/langage_secondary
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        help_text="Default language setting for this publication. (choise=EN/JA",
    )
    title = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        default="",
        help_text=(
            "Title of this pubilication (Primary Language). Check validation rules."
            "(len=512, blank=True)"
        ),
    )
    title_2nd_lang = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        default="",
        help_text=(
            "Title of this pubilication (Primary Language). Check validation rules."
            "(len=512, blank=True)"
        ),
    )
    authors = models.ManyToManyField(
        "core.Author",
        through="AuthorOrder",
        help_text=(
            "Authors of this publication. "
            "The order is stored based on ``AuthorOrder.order`` model."
            "(model='Author', through='AuthorOrder')."
        ),
    )
    book = models.ForeignKey(
        "core.Book",
        on_delete=models.PROTECT,
        help_text=("Book object of this entry." "(model=Book)"),
    )
    bib_type = models.CharField(
        max_length=32,
        choices=BIBSTYLE_CHOICES,
        default="SAMEASBOOK",
        help_text=(
            "If this entry is related to an award or a presentation (not article),"
            "set this field. Otherwise, set SAMEASBOOK."
            "(choose from ``BIBSTYLE_CHOICES``, see note for available choices.)"
        ),
    )
    book_title = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        default="",
        help_text=(
            "The title of the book, if only part of it is being cited. "
            "This field include more detail information like year."
            "For example, the title of book object is 'ICLR', set 'the 20th ICML'."
            "(len=512, blank=True)"
        ),
    )
    volume = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text=(
            "The volume of a journal or multi-volume book."
            "Before published, ignore this field."
            "(len=128, blank=True)"
        ),
    )
    number = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text=(
            "The '(issue) number' of a journal, magazine, or tech-report,"
            "if applicable. Note that this is not the 'article number' assigned"
            "by some journals. Before published, ignore this field."
            "(len=128, blank=True)"
        ),
    )
    chapter = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text=(
            "The chapter number of a jounral. Before published, ignore this field."
            "(len=128, blank=True)"
        ),
    )
    page = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        help_text=(
            "page number. Before published, ignore this field. Check validation rule."
            "(len=32, blank=True)"
        ),
    )
    edition = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text=(
            "The edition name. Before published, ignore this field. Check validation rule."
            "(len=128, blank=True)"
        ),
    )
    pub_date = models.DateField(
        null=True,
        blank=True,
        default=datetime.date.today,
        help_text=(
            "The date (year, month, date) on which the book is published. "
            "If date-info is no needed, set 01 to the date field."
            "(blank=True) (default: 2000-01-01)"
        ),
    )
    use_date_info = models.BooleanField(
        default=False,
        blank=True,
        help_text=("If set True, the date will be displayed." "(default: False)"),
    )
    url = models.URLField(
        null=True, blank=True, help_text=("An URL to PDF or something. (blank=True)")
    )
    fund = models.CharField(
        max_length=512,
        null=False,
        blank=True,
        default="",
        help_text=(
            "Information about research fundings" "(e.g. JST CREST JPMJCR15E2)."
        ),
    )
    doi = models.CharField(
        max_length=128,
        null=False,
        blank=True,
        default="",
        help_text=("The Digital Object Identifier." "(len=128, optional)"),
    )
    abstract = models.TextField(
        null=True, blank=True, help_text=("Abstract of the paper." "(blank=True)")
    )
    memo = models.CharField(
        max_length=32,
        null=False,
        blank=True,
        default="",
        help_text=(
            "[Deprecated] Short Note to distinguish similar entries." "(blank=True)"
        ),
    )
    note = models.TextField(
        null=False,
        blank=True,
        default="",
        help_text=("Note or comment." "(blank=True)"),
    )
    related_entry = models.URLField(
        null=True, blank=True, help_text=("URL to a related PubZ entry. (blank=True)")
    )
    tags = models.ManyToManyField(
        "core.Tag",
        through="core.TagChain",
        blank=True,
        help_text=(
            "Tags linked to this publication. "
            "(model='core.Tag', through='core.TagChain')"
        ),
    )
    is_published = models.BooleanField(
        default=False,
        blank=True,
        help_text=(
            "Set True when this paper has already published." "(default: False)"
        ),
    )
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=False)
    owner = models.ForeignKey("users.User", null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = (
            (
                "title",
                "book",
                "pub_date",
                # "memo",
                "page",
            ),
        )

    def __str__(self):
        if self.title is not None:
            return str(self.title)
        return "Bibtex[{}]".format(self.id)

    @property
    def book_title_display(self):
        """Returns a book title of this entry.

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
            return "({abbr} {year})".format(
                abbr=self.book.abbr, year=self.pub_date.year
            )
        else:
            return None

    @property
    def bib_type_key(self):
        """Returns bibtex type (key).

        Returns:
            str (``Bitex.BIBTEXSTYLE_CHOICES`` or ``Book.STYLE_CHOICES``)

        """
        if self.bib_type == "SAMEASBOOK":
            return self.book.style
        return self.bib_type

    @property
    def bib_type_display(self):
        """Returns bibtex tyepe (display string)"""
        if self.bib_type == "SAMEASBOOK":
            return self.book.get_style_display()
        return self.get_bib_type_display()

    @property
    def authors_list(
        self,
    ):
        """Returns a list of linked core.Author objects.

        Returns:
            list of ``core.Author``

        """
        author_list = []
        for author in self.authors.all():
            author_dict = author.__dict__
            if self.language == "JA":
                author_dict["name"] = author.name_ja
            else:
                author_dict["name"] = author.name_en
            author_list.append(author_dict)
        return author_list

    @property
    def author_order_list(self):
        """TBA


        Todo:
            Check whether this property is used or not. If not, remove this.

        """
        return self.authororder_set.all().order_by("order")

    @property
    def date_str(self):
        """Returns date in display format.

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
        """Returns date infomation as dict.

        This dict contains month sting

        Todo:
            Check whether this property is used or not. If not, remove this.

        """
        dict_ret = {
            "original": self.pub_date,
        }
        if self.pub_date:
            dict_ret["year"] = self.pub_date.year
            dict_ret["month"] = self.pub_date.month
            dict_ret["month_string"] = self.pub_date.strftime("%B")
        else:
            dict_ret["year"] = "None"
            dict_ret["month"] = "None"
            dict_ret["month_string"] = "None"
        return dict_ret


class Author(models.Model):
    name_en = models.CharField(
        max_length=128,
        help_text=(
            "The auhtor's full name in English. First name and family name should be "
            "split by space. See validation rules. (len=128)."
        ),
    )
    name_ja = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text=(
            "The author's full Name (Japanese). First name and family name should be "
            "split by space. See validation rules.  (len=128, null=True, blank=True)"
        ),
    )
    affiliation_en = models.TextField(
        null=True,
        blank=True,
        help_text=("Affiliation (in English)" "(null=True, blank=True)"),
    )
    affiliation_ja = models.TextField(
        null=True,
        blank=True,
        help_text=("Affiliation (in Japanese)" "(null=True, blank=True)"),
    )
    mail = models.EmailField(
        null=True, blank=True, help_text=("E-mail." "(null=True, blank=True)")
    )
    date_join = models.DateField(
        null=True,
        blank=True,
        help_text=(
            "The date which this author joinded to this department."
            "(null=True, blank=True)"
        ),
    )
    date_leave = models.DateField(
        null=True,
        blank=True,
        help_text=(
            "The date which this author leave this department."
            "(null=True, blank=True)"
        ),
    )
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=False)
    owner = models.ForeignKey(
        "users.User", null=True, blank=False, on_delete=models.SET_NULL
    )

    class Meta:
        unique_together = (
            (
                "name_en",
                "mail",
            ),
        )

    def __str__(self):
        return str(self.name_en)

    @property
    def name(self, lang="EN"):
        """ Returns the name of the author in a selected language. """
        if lang == "EN":
            return self.name_en
        else:
            return self.name_ja

    @property
    def dep(self, lang="EN"):
        """ Returns department name in a selected language. """
        if lang == "EN":
            return self.dep_en
        else:
            return self.dep_ja


class Book(models.Model):
    """

    Publication object
    Available Book stype.

    .. csv-table::
        :header: Key, Type, Memo
        :widths: 5, 5, 10

        ``ARTICLE``, Journal, Journal Paper
        ``INPROCEEDINGS_INTERNATIONAL``, Proceedings of International Conference
        ``INPROCEEDINGS_DOMESTIC``, Domestic Conference, (国内会議 (査読付き), 国内研究会, 全国大会)
        ``BOOK``, Book, 出版社が刊行した書籍。(著書／監修／編集／訳書)
        ``NEWS``, News Paper, 新聞記事
        ``MISC``, Others, その他該当種別が無いもの。

    """

    STYLE_CHOICES = (
        (
            "Paper",
            (
                ("ARTICLE", "Journal"),
                ("INPROCEEDINGS_INTERNATIONAL", "International Conference"),
                (
                    "INPROCEEDINGS_DOMESTIC",
                    "Domestic Conference",
                ),
            ),
        ),
        (
            "Article",
            (
                (
                    "BOOK",
                    "Book",
                ),
                (
                    "NEWS",
                    "News Paper",
                ),
                ("MISC", "Others"),
            ),
        ),
    )

    title = models.CharField(
        max_length=256,
        help_text=(
            "Book title (full). Some words should be replaced based on the local "
            "rules. See validation rules. (len=256, blank=False)"
        ),
    )
    abbr = models.CharField(
        max_length=256,
        blank=True,
        null=False,
        default="",
        help_text=(
            "The book title (Abbreviation)."
            "See validation. (len=256, null=True, blank=True)"
        ),
    )
    style = models.CharField(
        max_length=32,
        choices=STYLE_CHOICES,
        help_text=(
            "Publication Type. See validation/type for the avaiable choises."
            "(len=32, choice=``core.Book.STYLE_CHOICES``)"
        ),
    )
    publisher = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text=("The publisher's name." "(len=256, blank=True)"),
    )
    note = models.TextField(
        null=True,
        blank=True,
        help_text=("Miscellaneous extra information." "(blank=True)"),
    )
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=False)
    owner = models.ForeignKey("users.User", null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = (
            (
                "title",
                "style",
            ),
        )

    def __str__(self):
        if self.abbr != "":
            return "{title} ({abbr})".format(title=self.title, abbr=self.abbr)
        return str(self.title)


class Tag(models.Model):
    """

    Via objects, you can make links among related bibtex entries.
    For example, make a tag for a working group (e.g. Ubiquitous),
    you can pick up all bibtex of this team through the tag.

    """

    name = models.CharField(
        max_length=32, help_text=("A name of this tag." "(len=32, required)")
    )
    description = models.TextField(help_text=("Discription of this tag."))
    parent = models.ForeignKey(
        "core.Tag",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=("A parent tag of this tag entry." "(model=Tag, blank=True)"),
    )
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=False)
    owner = models.ForeignKey(
        "users.User",
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        unique_together = (
            (
                "name",
                "parent",
            ),
        )

    def __str__(self):
        return str(self.name)


class AuthorOrder(models.Model):
    """This is an intermidiate model to link bibtex and author objects."""

    bibtex = models.ForeignKey(
        "core.Bibtex",
        on_delete=models.PROTECT,
    )
    author = models.ForeignKey(
        "core.Author",
        on_delete=models.PROTECT,
    )
    order = models.PositiveSmallIntegerField(
        help_text=(
            "a order of this author within the bibtex."
            "For example, this author is a first author, set 1."
            "(Only positive integer is acceptable)"
        )
    )
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=False)
    owner = models.ForeignKey("users.User", null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = (
            (
                "bibtex",
                "order",
            ),
        )

    def __str__(self):
        if self.order == 1:
            order = "1st"
        elif self.order == 2:
            order = "2nd"
        elif self.order == 3:
            order = "3rd"
        else:
            order = "{}th".format(self.order if self.order else "")
        bib_id = self.bibtex.id if self.bibtex.id else 0
        s = "Bibtex[{}] {}".format(bib_id, order)
        return s


class TagChain(models.Model):
    """This is an intermidiate model to link bibtex and tag objects."""

    bibtex = models.ForeignKey(
        "core.Bibtex",
        on_delete=models.PROTECT,
    )
    tag = models.ForeignKey(
        "core.Tag",
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True, blank=False)
    modified = models.DateTimeField(auto_now=True, blank=False)
    owner = models.ForeignKey("users.User", null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = (
            (
                "bibtex",
                "tag",
            ),
        )
