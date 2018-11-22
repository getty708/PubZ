from django import forms



# ===============
# Model: Author
# ===============
def val_author_title_en_replace_keywords(author):
    if "　" in author:
        return authort.replace("　", " ")

    elif " " not in author:
        return error

    else:
        return author


validation_callback_bibtex ={
    "tmp": [],
}



# ----------------------------------------------------------
# ===============
# Model: Bibtex
# ===============
def val_bibtex_title_en_replace_keywords(title_en):
    """
    Return.
    -------
    - Title string, some keywords are replaced with registerd format
    (e.g. Conference => Conf., International => Int'l.)
    """
    CHECK_LIST = [
        # <Target>: [ <Source1>, <Source2>, ...],
        'for', 'on',
    ]

    validated_title  = ''

    if ':' in title_en:
        validated_title = title_en


    else:
        space_separated_list = title_en.split()

        need_capitalize = True
        for word in space_separated_list:
            if need_capitalize or word not in CHECK_LIST:
                need_capitalize = False
                validated_title = validated_title + word.capitalize() + ' '
            else:
                validated_title = validated_title + word + ' '

        validated_title = validated_title[:-1]

    return validated_title




# ----------------------------------------------------------
# ===============
# Medel: Book
# ===============
def val_book_title_replace_keywords(title):
    """
    Return.
    -------
    - Title string, some keywords are replaced with registerd format
    (e.g. Conference => Conf., International => Int'l.)
    """
    CHECK_DICT ={
        "Conference": ["Conf.",],
        "Transactions on": ["Trans.",],
        "in Proceedings of": ["Proc.",],
        "International": ["Int'l",],
    }

    for key, value in CHECK_DICT.items():
        for v in value:
            title = title.replace(v, key)

    return title



# ----------------------------------------------------------
# ===============
# Connection to form
# ===============


# BibtexFormStep1 (Step.1)
# - url: `dashboard:bibtex_add_step1`
validation_callback_bibtex_form_step1 = {
    "title": [val_bibtex_title_en_replace_keywords],
}


# BibtexForm (Detail)
# - url: `dashboard:bibtex_edit`
validation_callback_bibtex_form = {
    "title_en": [val_bibtex_title_en_replace_keywords],
}


# BookForm
# - url: `dashboard:bool_edit`
validation_callback_book_form = {
    "title": [val_book_title_replace_keywords],
}


# AuthorForm
# - url: `dashboard:bool_edit`
validation_callback_author_form = {

}
