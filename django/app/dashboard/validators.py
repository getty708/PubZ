from django import forms



# ===============
# Model: Author
# ===============
def val_author_name_en_replace_keywords(name_en):
    if "　" in name_en:
        return name_en.replace("　", " ")
    else:
        return name_en


def val_author_name_ja_replace_keywords(name_ja):
    if name_ja is not None:
        if "　" in name_ja:
            return name_ja.replace("　", " ")
        else:
            return name_ja
            

def val_author_name_en_lab_rule(name_en):
    validated_name_en = ""
    separated_list = name_en.split()
    for i in range(len(separated_list)-1):
        validated_name_en = validated_name_en + separated_list[i][0:1] + "."

    validated_name_en = validated_name_en + "~" + separated_list[-1]
    return validated_name_en


def val_author_name_ja_lab_rule(name_ja):
    if len(name_ja) <= 4:
        return name_ja.replace(" ", "~")
    else:
        return name_ja.replace(" ", "")



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
        # preposition
        'to', 'for', 'from', 'up', 'down', 'in', 'on', 'at', 'off', 'into', 'around',
        'among', 'between', 'of', 'over', 'above', 'below', 'under', 'through', 'across',
        'along', 'near', 'by', 'beside',
        # article
        'a', 'an', 'the',
        # conjunction

    ]

    validated_title  = ''

    if ':' in title_en:
        colon_separated_list = title_en.split(':')
        space_separated_list_front = colon_separated_list[0].split()
        space_separated_list_back = colon_separated_list[1].split()

        need_capitalize_front =True
        for word in space_separated_list_front:
            if need_capitalize_front or word not in CHECK_LIST:
                need_capitalize_front = False
                if '{' in word:
                    validated_title = validated_title + word + ' '
                elif '-' in word:
                    front = word.split('-')[0].capitalize()
                    back = word.split('-')[1].capitalize()
                    validated_title = validated_title + front + '-' + back + ' '
                else:
                    validated_title = validated_title + word.capitalize() + ' '
            else:
                validated_title = validated_title + word + ' '

        validated_title = validated_title[:-1] + ': '

        need_capitalize_back =True
        for word in space_separated_list_back:
            if need_capitalize_back or word not in CHECK_LIST:
                need_capitalize_back = False
                if '{' in word:
                    validated_title = validated_title + word + ' '
                elif '-' in word:
                    front = word.split('-')[0].capitalize()
                    back = word.split('-')[1].capitalize()
                    validated_title = validated_title + front + '-' + back + ' '
                else:
                    validated_title = validated_title + word.capitalize() + ' '
            else:
                validated_title = validated_title + word + ' '
    else:
        space_separated_list = title_en.split()
        need_capitalize = True

        for word in space_separated_list:
            if need_capitalize or word not in CHECK_LIST:
                need_capitalize = False
                if '{' in word:
                    validated_title = validated_title + word + ' '
                elif '-' in word:
                    front = word.split('-')[0].capitalize()
                    back = word.split('-')[1].capitalize()
                else:
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
    "name_en": [val_author_name_en_replace_keywords],
    "name_ja": [val_author_name_ja_replace_keywords],
}
