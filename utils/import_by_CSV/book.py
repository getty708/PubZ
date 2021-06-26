import argparse
import json
import os
from logging import INFO, basicConfig, getLogger

import requests
from auth_token import get_auth_token

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
KEYS_CREATE_BOOK = [
    "title",
    "abbr",
    "style",
]


# -----------------------------------------------------------------------
"""
GET
"""


def get_books(url_base, param, logger=getLogger(__name__ + ".get_book")):
    """
    Args.
    -----
    - url_base : str, End point of Base REST API
    - param     : str, book (name_en or name_ja)

    Return.
    -------
    - list
    """
    url_with_param = os.path.join(url_base, "books/?search={}".format(param))
    headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
    }
    r = requests.get(url_with_param, headers=headers, verify=False)
    if r.status_code in [
        200,
    ]:
        data = json.loads(r.text)
        books = data["results"]
    else:
        books = []
    return books


"""
POST
"""


def create_book(
    url_base, token, book_dict, logger=getLogger(__name__ + ".create_book")
):
    """
    Args.
    -----
    - url         : str, API Endpoint
    - token       : str, Authentication Token
    - book_dict : dict object which contains KEYS_POST_BOOK

    Returns.
    --------
    - True/False
    """
    # Check payload
    key_expected, key_actual = set(KEYS_CREATE_BOOK), set(book_dict.keys())
    if not key_expected == key_actual:
        logger.warning(
            "Check book_dict. some keys are missing or it contains unsed keys. [diff={}]".format(
                key_expected - key_actual
            )
        )
        return False

    # Make Post Request
    url_post = os.path.join(url_base, "books/")
    headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
        "Authorization": "Token {}".format(token),
    }
    payload = book_dict
    logger.debug("Make Requests:")
    logger.debug("- url    : {}".format(url_post))
    logger.debug("- headers: {}".format(headers))
    logger.debug("- params : {}".format(payload))
    r = requests.post(url_post, headers=headers, data=json.dumps(payload), verify=False)

    # Check Responce
    data = json.loads(r.text)
    logger.debug("Response: status={}, data={}".format(r.status_code, data))
    if r.status_code == 201:
        logger.info("Success: Create new book.")
        return True, "Created"
    else:
        if (
            str(data)
            == "{'non_field_errors': ['The fields title, style must make a unique set.']}"
        ):
            logger.warning("Failed: Already exists (DB internal error.)\n")
            return True, str(data)
        logger.warning("Failed: Cannot create new book. {}".format(data))
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
    book_dict = {
        "title": "TestBook1",
        "abbr": "test conf.",
        "style": "BOOK",
    }
    create_book(url, token, book_dict)


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
    # Get Token
    def _auth_token():
        url = os.path.join(args.url_base, "api-token-auth/")
        token = get_auth_token(url, args.username)
        logger.debug("Token [{}]: {}".format(args.username, token))
        return token

    def _load_csv():
        # Read and Check CSV
        import pandas as pd

        df = pd.read_csv(args.file).fillna("")
        print(df.head())
        key_expected, key_actual = set(KEYS_CREATE_BOOK), set(df.columns)
        if not key_expected <= key_actual:
            raise ValueError(
                "Check CSV some keys are missing [diff={}]".format(
                    key_expected - key_actual
                )
            )
        return df

    def _create_books(df):
        df["status"] = "None"
        df["msg"] = ""
        if args.debug:
            df = df[:10].reset_index(drop=True)
        for i in range(len(df)):
            row = df.loc[i, :]
            book_dict = {
                "title": row["title"],
                "abbr": row["abbr"],
                "style": row["style"],
            }
            status, msg = create_book(args.url_base, token, book_dict)
            df.loc[i, "status"] = status
            df.loc[i, "msg"] = msg
        return df

    def _print_results(df):
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
            "Errors : {} [{}%]".format(
                len(df_error), len(df_error) / len(df_tried) * 100
            )
        )
        for no, idx in enumerate(df_error.index):
            logger.info(
                "- No.{}: {} {}".format(
                    no,
                    df_error.loc[idx, ["status", "msg"]].values,
                    df_error.loc[
                        idx,
                        [
                            "style",
                            "title",
                            "abbr",
                        ],
                    ].values,
                )
            )
            logger.info("==============")

        # Write Results
        filename = "".join(str(args.file).split(".")[:-1]) + ".results.csv"
        if args.file[0] != "/":
            filename = "." + filename
        df.to_csv(filename)

    # == Main ==
    token = _auth_token()
    df = _load_csv()
    df = _create_books(df)
    _print_results(df)


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
