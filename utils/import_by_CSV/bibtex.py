import argparse
import json
import os
from logging import INFO, basicConfig, getLogger

import requests
from auth_token import get_auth_token
from book import get_books

logger = getLogger(__name__)
LOG_FMT = "{asctime} | {levelname:<5s} | {name} | {message}"
basicConfig(level=INFO, format=LOG_FMT, style="{")

# -----------------------------------------------------------------------


def make_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Sub-Commands")

    # single
    single_parser = subparsers.add_parser("SINGLE")
    single_parser.set_defaults(func=main_single)
    single_parser.add_argument(
        "--url-base",
        default="http://django:8000/api/rest/",
        help="URL to get auth token",
    )
    single_parser.add_argument(
        "-u", "--username", required=True, help="User ID (email)"
    )

    # CSV
    csv_parser = subparsers.add_parser("CSV")
    csv_parser.set_defaults(func=main_csv)
    csv_parser.add_argument(
        "--url-base",
        default="http://django:8000/api/rest/",
        help="URL to get auth token",
    )
    csv_parser.add_argument("-u", "--username", required=True, help="User ID (email)")
    csv_parser.add_argument("-f", "--file", required=True, help="file path")
    csv_parser.add_argument("--debug", action="store_true", help="Debug flag")

    return parser


# -----------------------------------------------------------------------
"""
Constant Params
"""
KEYS_CREATE_BIBTEX = [
    "language",
    "title_en",
    "title_ja",
    "volume",
    "number",
    "chapter",
    "page",
    "edition",
    "bib_type",
    "pub_date",
    "use_date_info",
    "url",
    "fund",
    "memo",
    "book",
    "book_title",
]


# -----------------------------------------------------------------------
"""
GET
"""


def get_bibtexs(url_base, param, logger=None):
    """
    Args.
    -----
    - url_base : str, End point of Base REST API
    - param     : str, bibtex (name_en or name_ja)

    Return.
    -------
    - list
    """
    if logger is None:
        logger = getLogger(__name__ + ".get_bibtex")

    url_with_param = os.path.join(url_base, "bibtexs/?search={}".format(param))
    headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
    }
    r = requests.get(url_with_param, headers=headers)
    if r.status_code in [
        200,
    ]:
        data = json.loads(r.text)
        bibtexs = data["results"]
    else:
        bibtexs = []
    return bibtexs


"""
POST
"""


def create_bibtex(
    url_base,
    token,
    bibtex_dict,
    logger=None,
):
    """

    Args:
        url         (str): API Endpoint
        token       (str): Authentication Token
        bibtex_dict (dict): dict object which contains KEYS_POST_BIBTEX

    Returns.
    --------
    - True/False
    """
    if logger is None:
        logger = getLogger(__name__ + ".create_bibtex")

    def _validate(bibtex_dict):
        # Check payload
        key_expected, key_actual = set(KEYS_CREATE_BIBTEX), set(bibtex_dict.keys())
        if not key_expected == key_actual:
            logger.warning(
                "Check bibtex_dict. some keys are missing or it contains unsed keys."
                + " [diff={}]".format(key_expected - key_actual)
            )
            return False
        return True

    def _get_book_data(bibtex_dict):
        # url_get_book = os.path.join(url_base, "books/")
        books = get_books(url_base, bibtex_dict["book"]["title"])
        books_selected = [
            book for book in books if (book["title"] == bibtex_dict["book"]["title"])
        ]
        if len(books_selected) == 1:
            book = books_selected[0]
            bibtex_dict["book_id"] = book["id"]
            logger.info("Get Book data: {}".format(book))
        else:
            logger.warning(
                "There is some anbiguity to selected book. [got {}]".format(len(books))
            )
            logger.warning("Search [{}] ==> {}".format(bibtex_dict["book"], books))
            return False, "Book is unknow"
        return True, bibtex_dict

    # Setup
    if not _validate(bibtex_dict):
        return False, "Failed: Key missmatch."
    status, bibtex_dict = _get_book_data(bibtex_dict)
    if not status:
        return False, str(bibtex_dict)

    # Make Post Request
    url_post = os.path.join(url_base, "bibtexs/")
    headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
        "Authorization": "Token {}".format(token),
    }
    payload = bibtex_dict
    logger.debug("Make Requests:")
    logger.debug("- url    : {}".format(url_post))
    logger.debug("- headers: {}".format(headers))
    logger.debug("- params : {}".format(payload))
    r = requests.post(url_post, headers=headers, data=json.dumps(payload), verify=False)

    # Check Responce
    data = json.loads(r.text)
    logger.debug("Response: status={}, data={}".format(r.status_code, data))
    print(payload)
    print(r.status_code)
    print(data)
    print()

    if r.status_code == 201:
        logger.info("Success: Create new bibtex. [{}]".format(bibtex_dict["title_en"]))
        return True, "Created"
    else:
        if str(data) == "['DB IntegrityError']":
            return True, str(data)
        logger.warning(
            "Failed: Cannot create new bibtex. {} - {}".format(r.status_code, data)
        )
    logger.info("\n")
    return False, str(data)


# -----------------------------------------------------------------------
"""
Main
"""


def main_single(args):
    # Get Token
    url = args.url_base + "api-token-auth/"
    token = get_auth_token(url, args.username)
    logger.debug("Token [{}]: {}".format(args.username, token))

    # POST
    url = args.url_base
    bibtex_dict = {
        "language": "EN",
        "title_en": "bibtex entry 2",
        "title_ja": "",
        "volume": "0",
        "number": "1",
        "chapter": "2",
        "page": "123-124",
        "edition": "",
        "pub_date": "2018-01-02",
        "use_date_info": False,
        "url": "",
        "fund": "",
        "memo": "",
        "bib_type": "AWARD",
        "book": {"title": "TestBook1", "style": "BOOK"},
        "book_title": "Test Book title",
    }
    create_bibtex(url, token, bibtex_dict)


def main_csv(args):
    """
    Args.
    -----
    - url       : str, API Endpoint
    - token     : str, Authentication Token
    - file_path : str, path to CSV file

    Returns.
    --------
    - pd.DataFrame
    """

    def _auth_token():
        url = os.path.join(args.url_base, "api-token-auth/")
        token = get_auth_token(url, args.username)
        logger.debug("Token [{}]: {}".format(args.username, token))
        return token

    def _load_csv():
        import pandas as pd

        df = pd.read_csv(args.file).fillna("")
        df = df.rename(
            columns={"bib_{}".format(c): c for c in KEYS_CREATE_BIBTEX + ["title"]}
        )
        # df["book"] = df["key_book"]
        df["language"] = df["language"].str.replace("en", "EN")
        df["language"] = df["language"].str.replace("ja", "JA")
        print(df.head())
        key_expected, key_actual = set(KEYS_CREATE_BIBTEX), set(
            list(df.columns) + ["title_en", "title_ja"]
        )
        if not key_expected <= key_actual:
            raise ValueError(
                "Check CSV some keys are missing [diff={}]".format(
                    key_expected - key_actual
                )
            )
        return df

    def _create_bibtexs(df):
        df["status"] = "None"
        df["msg"] = ""
        if args.debug:
            df = df[200:210].reset_index(drop=True)
        for i in range(len(df)):
            row = df.loc[i, :]
            bibtex_dict = {
                "language": row["language"],
                "title_en": row["title"] if row["language"] == "EN" else "",
                "title_ja": row["title"] if row["language"] == "JA" else "",
                "volume": row["volume"],
                "number": row["number"],
                "chapter": row["chapter"],
                "page": row["page"],
                "edition": row["edition"],
                "pub_date": row["pub_date"],
                "use_date_info": False if row["use_date_info"] == 0 else True,
                "url": row["url"],
                "fund": row["fund"],
                "memo": row["memo"],
                "book": {"title": row["book"], "style": row["bib_type"]},
                "book_title": row["book_title"],
                "bib_type": row["bib_type"],
            }
            # raise NotImplementedError("OK!")
            status, msg = create_bibtex(args.url_base, token, bibtex_dict)
            df.loc[i, "status"] = status
            df.loc[i, "msg"] = msg
        return df

    # == Main ==
    token = _auth_token()
    df = _load_csv()[:]
    df = _create_bibtexs(df)

    # Results
    logger.info("=== Results ===")
    df_tried = df[df["status"].isin([True, False])]
    df_success, df_error = df[df["status"] == True], df[df["status"] == False]
    logger.info("Total  : {}".format(len(df_tried)))
    logger.info(
        "Success: {} [{}%]".format(
            len(df_success), len(df_success) / len(df_tried) * 100
        )
    )
    logger.info(
        "Errors : {} [{}%]".format(len(df_error), len(df_error) / len(df_tried) * 100)
    )
    for no, idx in enumerate(df_error.index):
        logger.info(
            "- No.{}: {} {}".format(
                no,
                df_error.loc[idx, ["status", "msg"]].values,
                df_error.loc[
                    idx,
                    [
                        "key_book_style_old",
                        "title",
                        "book_title",
                    ],
                ].values,
            )
        )
    logger.info("==============")

    # Write Results
    filename = str(args.file) + ".results.csv"
    df.to_csv(filename)


# -----------------------------------------------------------------------
if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()
    args_dict = vars(args)
    logger.info(" Args:")
    for key in args_dict.keys():
        logger.info(" - {:<15s}= {}".format(key, args_dict[key]))
    print()
    args.func(args)
