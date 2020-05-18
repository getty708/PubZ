import os
import json
import requests
from getpass import getpass
import pandas as pd

from logging import getLogger, basicConfig, DEBUG, INFO
logger = getLogger(__name__)
LOG_FMT = "{asctime} | {levelname:<5s} | {name} | {message}"
# basicConfig(level=DEBUG, format=LOG_FMT, style="{")
basicConfig(level=INFO, format=LOG_FMT, style="{")

from auth_token import get_auth_token
from book import get_books
from bibtex import get_bibtexs
from authors import get_authors

# -----------------------------------------------------------------------
import argparse

def make_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='Sub-Commands')

    # single
    single_parser = subparsers.add_parser('SINGLE')
    single_parser.set_defaults(func=main_single) 
    single_parser.add_argument('--url-base', default="http://django:8000/api/rest/",
                                help="URL to get auth token")
    single_parser.add_argument('-u', '--username', required=True,
                                help="User ID (email)")

    
    # CSV
    csv_parser = subparsers.add_parser('CSV')
    csv_parser.set_defaults(func=main_csv)
    csv_parser.add_argument('--url-base', default="http://django:8000/api/rest/",
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
KEYS_CREATE_AUTHOR_ORDER = ["bibtex_id","author_id","order",]


# -----------------------------------------------------------------------
"""
GET
"""
def get_author_orders(url_base, param, logger=getLogger(__name__+'.get_author_order')):
    """
    Args.
    -----
    - url_base : str, End point of Base REST API 
    - param     : str, author_order (name_en or name_ja)

    Return.
    -------
    - list
    """
    url_with_param = url_base + "author_orders/?search={}".format(param)
    headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
    }
    r = requests.get(url_with_param, headers=headers)
    if r.status_code in [200,]:
        data = json.loads(r.text, "utf-8")
        author_orders = data["results"]
    else:
        author_orders = []
    return author_orders


"""
POST
"""
def create_author_order(url_base, token, data, logger=getLogger(__name__+'.create_author_order')):
    """
    Args.
    -----
    - url         : str, API Endpoint
    - token       : str, Authentication Token
    - data : dict object which contains ["bibtex_title", "authors",]

    Returns.
    --------
    - True/False
    """
    # Make Post Request
    URL_POST = os.path.join(url_base, "author-orders/")
    HEADERS = {
        "Accept": "application/json",
        "Content-type": "application/json",
        "Authorization": "Token {}".format(token),
    }
    
    def _validate():
        key_expected, key_actual = set(["bibtex","book","pub_date","page","authors"]), set(data.keys())
        if not key_expected == key_actual:
            logger.warning("Check `data`. some keys are missing or it contains unsed keys. [diff={}]".format(
                key_expected - key_actual))
            raise ValueError("Check author_order_dict")

    # Get Bibtex Data
    def _get_bibtex(bib_title, book, pub_date, page,):
        def _check(bibtexs):
            ret = []
            for bib in bibtexs:
                if (bib["title_en"] == bib_title) or (bib["title_ja"] == bib_title):
                    if (bib["book"]["title"] == book) and (bib["pub_date"] == pub_date) and (bib["page"] == page):
                        return bib
            raise ValueError("No bibtex entry was found. [Search Results={}]".format(len(bibtexs)))
        
        bibtexs = get_bibtexs(url_base, bib_title)
        bibtex = _check(bibtexs)
        logger.info("Get Bibtex data: {}".format(bibtex))
        return bibtex

    def _get_author(author_name):
        def _check_name(author_name, author_db):
            name_en = author_db["name_en"].upper()
            if author_db['name_ja'] ==  None:
                name_ja = ""
            else:
                name_ja = "".join(author_db["name_ja"].split())
            #print(author_name, "=>", name_en, name_ja)
            if author_name.upper() == name_en:
                return True
            elif len(name_ja) > 0 and (name_ja == "".join(author_name.split())):
                # Japanene Version
                return True
            elif len(name_en.split(",")) == 2 and len(author_name.split()) == 2:
                _name1 = [s.upper() for s in author_name.split()]
                _name2 = [s.strip() for s in name_en.split(",")]
                #print(_name1, _name2, _name1[0] == _name2[0], _name1[1] == _name2[1], _name1[0] == _name2[1], _name1[1] == _name2[0],)
                if (_name1[0] == _name2[0]) and (_name1[1] == _name2[1]):   # FamilyName + FirstName
                    return True
                elif (_name1[0] == _name2[1]) and (_name1[1] == _name2[0]): # FirstName + FamilyName
                    return True
            return False
                
        for _author in [s.strip() for s in author_name.split()]:
            for author_db in get_authors(url_base, _author):
                if _check_name(author_name, author_db):
                    return author_db
        return None

    # == Main ==
    _validate()
    bibtex = _get_bibtex(
        data["bibtex"],
        data["book"],
        data["pub_date"],
        data["page"],
    )

    
    authors_list = [a.strip() for a in data["authors"].split(",")]
    authors_success, authors_fail = [], []
    for no, author_name in enumerate(authors_list):
        #print(author_name)
        # Get Author Data
        author = _get_author(author_name)
        if author == None:
            authors_fail.append("{}[AuthorNotFound]".format(author_name))
            continue
        
        # Post
        payload = {
            "bibtex_id": bibtex["id"],
            "author_id": author["id"],
            "order":     no+1,
        }
        r = requests.post(URL_POST,  headers=HEADERS, data=json.dumps(payload),)
        ## Check Responce
        logger.info("Response: status={} [{}]".format(r.status_code,author_name))
        _data = json.loads(r.text)
        print(r.status_code)
        print(_data)
        if r.status_code == 201:
            logger.info("Success: Create new author_order. [Bib{} - {} ({})]".format(bibtex["id"],author_name,no+1))
            authors_success.append(author_name)
            continue
        else:
            if str(_data) == "['DB IntegrityError']":
                authors_success.append("{}[{}]".format(author_name,"DB IntegrityError"))
                continue
            logger.warning("Failed: Cannot create new author_order. {} \n".format(_data))
            authors_fail.append("{}[{}]".format(author_name, _data))

    # Summry
    ret = {
        "bib_title": data["bibtex"],
        "bib_id": bibtex["id"],
        "pub_date": data["pub_date"],
        "book": data["book"],
        "author_success": authors_success,
        "author_fail": authors_fail,
        "status": True,
    }
    return ret

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
    author_order_dict = {
        "bibtex": "bibtex entry 1",
        "book": "TestBook1",
        "pub_date": "2018-01-02",
        "page": "123-124",
        "authors": "Test Author4, Test Author, Test Abc",    
    }
    df = create_author_order(url, token, author_order_dict)
    print(df)

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
    def _get_auth_token():
        url = os.path.join(args.url_base, "api-token-auth/")
        token = get_auth_token(url, args.username)
        logger.debug("Token [{}]: {}".format(args.username, token))
        return token
    
    def _load_csv():
        import pandas as pd
        df = pd.read_csv(args.file).fillna("")
        print(df.head())
        key_expected, key_actual = set(["bib_title","keys_author",]), set(list(df.columns))
        if not key_expected <= key_actual:
            raise ValueError("Check CSV some keys are missing [diff={}]".format(key_expected - key_actual))
        return df

    def _create_author_orders(df):
        df["status"] = "None"
        df["msg"] = ""
        df_ret = []
        if args.debug:
            df = df[:10].reset_index(drop=True)
        for i in range(len(df)):
            row = df.loc[i, :]
            author_order_dict = {
                "bibtex"  : row["bib_title"],
                "book"    : row["book"],
                "pub_date": row["bib_pub_date"],
                "page"    : row["bib_page"],
                "authors" : row["keys_author"],
            }
            try:                
                status = create_author_order(args.url_base, token, author_order_dict)
                df_ret.append(status)                
            except ValueError as e:
                logger.warning("ValueError: {}".format(e))
                status = {
                    "bib_title":row["bib_title"],
                    "bib_id": -1,
                    "book": row["book"],
                    "pub_date": row["bib_pub_date"],
                    "author_success": None,
                    "author_fail": row["keys_author"],
                    "status": False,
                    "Error": e,
                }
                df_ret.append(status)
            #raise NotImplementedError("OK!")
        df_ret = pd.DataFrame(df_ret)
        return df_ret

    # == Main ==
    token = _get_auth_token()
    df = _load_csv()[:]
    df_results = _create_author_orders(df)
    
    # Results
    logger.info("=== Results ===")
    df_tried = df_results[df_results["status"].isin([True, False])]
    df_success, df_error = df_results[df_results["status"] == True], df_results[df_results["status"] == False]
    logger.info("Total  : {}".format(len(df_tried)))
    logger.info("Success: {} [{}%]".format(
        len(df_success), len(df_success)/len(df_tried)*100))
    logger.info("Errors : {} [{}%]".format(
        len(df_error), len(df_error)/len(df_tried)*100))
    for no,idx in enumerate(df_error.index):
        logger.info("- No.{}: {}".format(
            no,
            df_error.loc[idx, ["status", "Error", "bib_id", "author_fail"]].values,))
    logger.info("==============")

    # Write Results
    filename = "/".join(str(args.file).split("/")[:-1]) + "/author_order.results.csv"
    logger.info("Write results to {}".format(filename))
    df_results.to_csv(filename)
    
    
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
