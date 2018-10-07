from django import forms



# ===============
# Model: Author
# ===============
def val_author_title_en_replace_keywords(author):
    pass


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
    CHECK_DICT ={
        # <Target>: [ <Source1>, <Source2>, ...],
        "Conf.": ["Conference",],        
    }
    
    return "CHECKED[{}]".format(title_en)




# ----------------------------------------------------------
# ===============
# Medel: Book
# ===============




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

}


# AuthorForm
# - url: `dashboard:bool_edit`
validation_callback_author_form = {

}





