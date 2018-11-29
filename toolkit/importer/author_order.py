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
def create_author_order(url_base, token, author_order_dict, logger=getLogger(__name__+'.create_author_order')):
    """
    Args.
    -----
    - url         : str, API Endpoint
    - token       : str, Authentication Token
    - author_order_dict : dict object which contains ["bibtex_title", "authors",]

    Returns.
    --------
    - True/False
    """
    # Check payload
    key_expected, key_actual = set(["bibtex", "authors"]), set(author_order_dict.keys())
    if not key_expected == key_actual:
        logger.warning("Check author_order_dict. some keys are missing or it contains unsed keys. [diff={}]".format(key_expected - key_actual))
        raise ValueError("Check author_order_dict")

    # Get Bibtex Data
    url_get_bibtex = url_base + "bibtexs/"
    bibtexs = get_bibtexs(url_base, author_order_dict["bibtex"]["title"])
    bibtexs_selected = [bibtex for bibtex in bibtexs if (bibtex["title_en"] == author_order_dict["bibtex"]["title"]) or (bibtex["title_ja"] == author_order_dict["bibtex"]["title"])]
    if len(bibtexs_selected) == 1:
        bibtex = bibtexs_selected[0]
        bibtex["title"] = author_order_dict["bibtex"]["title"]
        bibtex_id = bibtex["id"]
        logger.info("Get Bibtex data: {}".format(bibtex))
    else:
        logger.warning("There is some anbiguity to selected bibtex. [got {}]".format(len(bibtexs)))
        logger.warning("Search [{}] ==> {}".format(author_order_dict["bibtex"], bibtexs))
        df_tmp = pd.DataFrame({
            "bibtex_title": [author_order_dict["bibtex"]["title"]],
            "bibtex_id"   : [-1,],
            "no"          : [0,],
            "author"      : [author_order_dict["authors"],],
            "status"      : [False],
            "msg"         : ["Bibtex not found [Got{}]".format(len(bibtexs)),],
        })
        return df_tmp

    
    # Make Post Request
    url_post = url_base + "author-orders/"
    headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
        "Authorization": "Token {}".format(token),
    }
    logger.debug("Make Requests:")
    logger.debug("- url    : {}".format(url_post))
    logger.debug("- headers: {}".format(headers))
    logger.debug("- params : {}".format(author_order_dict))

    df_ret = []
    authors_list = [a.strip() for a in author_order_dict["authors"].split(",")]
    for no,_author in enumerate(authors_list):
        row = [bibtex["title"],bibtex_id, no, _author,]
        # Get Author Data
        url_get_author = url_base + "authors/"
        _author = _author.strip()
        authors = get_authors(url_base, _author)
        authors_selected = [author for author in authors if (_author == author["name_en"].upper()) or (_author == author["name_ja"].upper())]
        if len(authors_selected) == 1:
            author = authors_selected[0]
            author_id = author["id"]
            logger.info("Get Author data: {}".format(author))
        else:
            logger.warning("There is some anbiguity to selected author. [got {}]".format(len(authors)))
            logger.warning("Search [{}] ==> {}".format(_author, authors))
            row = row + [False, "Author is unknow [Got {}]".format(len(authors))]
            df_ret.append(row)
            continue
            
        # Post
        payload = {
            "bibtex_id": bibtex_id,
            "author_id": author_id,
            "order":     no+1,
        }
        r = requests.post(url_post,  headers=headers, data=json.dumps(payload),)
        ## Check Responce
        logger.info("Response: status={}".format(r.status_code))            
        data = json.loads(r.text)
        logger.debug("Response: status={}, data={}".format(r.status_code, data))
        if r.status_code == 201:
            logger.info("Success: Create new author_order.\n")
            row = row + [True, "Created"]
            df_ret.append(row)
            continue
        else:
            if str(data) == "['DB IntegrityError']":
                row = row + [True, str(data)]
                df_ret.append(row)
                continue            
            logger.warning("Failed: Cannot create new author_order. {} \n".format(data))
            row = row + [False, str(data)]
            df_ret.append(row)
            continue
    return pd.DataFrame(df_ret, columns=["bibtex_titele", "bibtex_id", "no", "author", "status", "msg"])


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
        "bibtex": {"title": "{IoT}環境における処理削減によるストリーミング処理時間短縮手法",},
        "authors": "AI-Sakib Khan Pathan,Akihito Hiromori,Akiko Yamazoe-Umemoto",
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
    url = args.url_base + "api-token-auth/"
    token = get_auth_token(url, args.username)
    logger.debug("Token [{}]: {}".format(args.username, token))
    
    # Read and Check CSV
    import pandas as pd
    df = pd.read_csv(args.file).fillna("")
    print(df.head())
    key_expected, key_actual = set(["bib_title","keys_author",]), set(list(df.columns))
    if not key_expected <= key_actual:
        raise ValueError("Check CSV some keys are missing [diff={}]".format(key_expected - key_actual))

    # Create New Author_Orders
    df["status"] = "None"
    df["msg"] = ""
    df_results = pd.DataFrame()
    if args.debug:
        df = df[1130:1140].reset_index(drop=True)
    for i in range(len(df)):
        row = df.loc[i, :]
        author_order_dict = {
            "bibtex" : {"title": row["bib_title"]},
            "authors": row["keys_author"],
        }
        df_tmp = create_author_order(args.url_base, token, author_order_dict)
        df_results = pd.concat([df_results, df_tmp], axis=0)
    df_results = df_results.reset_index(drop=False)
    print(df_results)

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
            df_error.loc[idx, ["status", "msg", "bibtex_id", "author"]].values,))
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
