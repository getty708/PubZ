import argparse
import json
from getpass import getpass
from logging import INFO, basicConfig, getLogger

import requests

logger = getLogger(__name__)
LOG_FMT = "{asctime} | {levelname:<5s} | {name} | {message}"
basicConfig(level=INFO, format=LOG_FMT, style="{")


# -----------------------------------------------------------------------


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        default="http://django:8000/api/rest/api-token-auth/",
        help="URL to get auth token",
    )
    parser.add_argument("-u", "--username", required=True, help="User ID (email)")
    return parser


# -----------------------------------------------------------------------
def get_auth_token(url, user, logger=None):
    if logger is None:
        logger = getLogger(__name__ + ".get_auth_token")

    pw = getpass("Password for [{}]: ".format(user))

    # Make Post Request
    headers = {
        "Accept": "application/json",
        "Content-type": "application/json",
    }
    payload = {
        "username": user,
        "password": pw,
    }
    logger.debug("Make Requests:")
    logger.debug("- url    : {}".format(url))
    logger.debug("- headers: {}".format(headers))
    logger.debug("- params : {}".format(payload))
    r = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)

    # Check Responce
    data = json.loads(r.text)
    logger.debug("Response: status={}\n{}".format(r.status_code, data))
    token = data["token"]
    if (r.status_code == 200) and token:
        logger.info("Success: Token was obtained.")
    else:
        raise ValueError("Filed to get token for user {}".format(user))
    return token


# -----------------------------------------------------------------------
if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()
    print()

    args_dict = vars(args)
    logger.info(" Args:")
    for key in args_dict.keys():
        logger.info(" - {:<15s}= {}".format(key, args_dict[key]))
    print()

    token = get_auth_token(args.url, args.username)
    logger.debug("Token [{}]: {}".format(args.username, token))
