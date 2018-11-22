import json
import requests
from getpass import getpass

from logging import getLogger, basicConfig, DEBUG, INFO
logger = getLogger(__name__)
LOG_FMT = "{asctime} | {levelname:<5s} | {name} | {message}"
# basicConfig(level=DEBUG, format=LOG_FMT, style="{")
basicConfig(level=INFO, format=LOG_FMT, style="{")

from auth_token import get_auth_token


# -----------------------------------------------------------------------
import argparse

def make_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='Sub-Commands')

    # single
    single_parser = subparsers.add_parser('SINGLE')
    single_parser.set_defaults(func=main_single) 
    single_parser.add_argument('--url-base', default="http://localhost:7000/api/rest/",
                                help="URL to get auth token")
    single_parser.add_argument('-u', '--username', required=True,
                                help="User ID (email)")

    
    # CSV
    csv_parser = subparsers.add_parser('CSV')
    csv_parser.set_defaults(func=main_csv)
    csv_parser.add_argument('--url-base', default="http://localhost:7000/api/rest/",
                                help="URL to get auth token")
    csv_parser.add_argument('-u', '--username', required=True,
                                help="User ID (email)")
    csv_parser.add_argument('-f', '--file', required=True,
                                help="file path")
    csv_parser.add_argument('--debug', action='store_true',
                                help="Debug flag")

    
    
    return parser


# -----------------------------------------------------------------------
"""
Constant Params
"""
KEYS_CREATE_AUTHOR = ["name_en", "name_ja", "dep_en", "dep_ja", "mail",]


# -----------------------------------------------------------------------
"""
GET
"""
def get_authors(url_base, param, logger=getLogger(__name__+'.get_authot')):
    """
    Args.
    -----
    - url_base : str, End point of Base REST API 
    - param     : str, author (name_en or name_ja)

    Return.
    -------
    - list
    """
    url_with_param = url_base + "authors/?search={}".format(param)
    headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
        # "Authorization": "Token {}".format(token),
    }
    r = requests.get(url_with_param, headers=headers)
    logger.debug(r.status_code)
    if r.status_code in [200,]:
        data = json.loads(r.text, "utf-8")
        authors = data["results"]
    else:
        authors = []
    return authors


"""
POST
"""
def create_author(url_base, token, author_dict, logger=getLogger(__name__+'.create_author')):
    """
    Args.
    -----
    - url         : str, API Endpoint
    - token       : str, Authentication Token
    - author_dict : dict object which contains KEYS_POST_AUTHOR

    Returns.
    --------
    - True/False
    """
    # Check payload
    key_expected, key_actual = set(KEYS_CREATE_AUTHOR), set(author_dict.keys())
    if not key_expected == key_actual:
        logger.warning("Check author_dict. some keys are missing or it contains unsed keys. [diff={}]".format(key_expected - key_actual))
        return False
    
    # Make Post Request
    url_post = url_base + "authors/"
    headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
        "Authorization": "Token {}".format(token),
    }
    payload = author_dict
    logger.debug("Make Requests:")
    logger.debug("- url    : {}".format(url_post))
    logger.debug("- headers: {}".format(headers))
    logger.debug("- params : {}".format(payload))
    r = requests.post(url_post,  headers=headers, data=json.dumps(payload),)

    # Check Responce
    data = json.loads(r.text)
    logger.debug("Response: status={}, data={}".format(r.status_code, data))
    if r.status_code == 201:
        logger.info("Success: Create new author.\n")
        return True, "Created"
    else:
        # if str(data) == "{'non_field_errors': ['The fields name_en, mail must make a unique set.']}":
        if "non_field_errors" in data.keys():
            logger.warning("Failed: Already exists (DB internal error.)\n")
            return True, str(data)
        logger.warning("Failed: Cannot create new book. {}\n".format(data))
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
    url = args.url_base + "authors/"
    author_dict = {
        "name_en": "TestAuthor2",
        "name_ja": "テスト2",
        "dep_en":  "Osaka University",
        "dep_ja":  "Osaka University",
        "mail":    "test2@test.com",
    }
    create_author(url, token, author_dict)


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
    url = args.url_base + "api-token-auth/"
    token = get_auth_token(url, args.username)
    logger.debug("Token [{}]: {}".format(args.username, token))
    
    # Read and Check CSV
    import pandas as pd
    df = pd.read_csv(args.file).fillna("")
    print(df.head())
    key_expected, key_actual = set(KEYS_CREATE_AUTHOR), set(df.columns)
    if not key_expected <= key_actual:
        raise ValueError("Check CSV some keys are missing [diff={}]".format(key_expected - key_actual))


    # Create New Authors
    df["status"] = "None"
    df["msg"] = ""
    if args.debug:
        df = df[:10].reset_index(drop=True)
    for i in range(len(df)):
        row = df.loc[i, :]
        author_dict = {
            "name_en": row["name_en"],
            "name_ja": row["name_ja"],
            "dep_en":  row["dep_en"],
            "dep_ja":  row["dep_ja"],
            "mail":    row["mail"],
        }
        status, msg = create_author(args.url_base, token, author_dict)
        df.loc[i, "status"] = status
        df.loc[i, "msg"] = msg
        

    # Results
    logger.info("=== Results ===")
    df_tried = df[df["status"].isin([True, False])]
    df_success, df_error = df[df["status"] == True], df[df["status"] == False]
    logger.info("Total  : {}".format(len(df_tried)))
    logger.info("Success: {} [{}%]".format(
        len(df_success), len(df_success)/len(df_tried)*100))
    logger.info("Errors : {} [{}%]".format(
        len(df_error), len(df_error)/len(df_tried)*100))
    for no,idx in enumerate(df_error.index):
        logger.info("- No.{}: {} {}".format(
            no,
            df_error.loc[idx, ["status", "msg"]].values,
            df_error.loc[idx, ["name_en", "name_ja", "mail",]].values))
    logger.info("==============")

    # Write Results
    filename = "".join(str(args.file).split(".")[:-1]) + ".results.csv"
    df.to_csv(filename)
    
    
# -----------------------------------------------------------------------    
if __name__=='__main__':
    parser = make_parser()
    args = parser.parse_args()
    args_dict = vars(args)
    logger.info(" Args:")
    for key in args_dict.keys():
        logger.info(" - {:<15s}= {}".format(key, args_dict[key]))
    print()
    args.func(args)    
