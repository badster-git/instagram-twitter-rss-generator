from bs4 import BeautifulSoup
from urllib.parse import urlencode
import clipboard
import argparse
import requests

def getUsernameResult(username):
    instagramUrl = "https://instagram.com/{}".format(username)

    response = requests.get(instagramUrl)
    soup = BeautifulSoup(response.text, 'html.parser')
    keyValue = '"logging_page_id"'

    try:
        for i in range(10):
            if keyValue in str(soup.find_all('script')[i])[:300]:
                val = str(soup.find_all('script')[i])[:300]
                return val
    except IndexError:
        val = ""

def getId(text):
    if (text is not None):
        keyValue = '"logging_page_id"'
        start = text.find(keyValue)

        cnt = 0
        pos = 0
        for x in text[start:]:
            if '"' == x:
               cnt += 1
            elif cnt == 4:
                end = start + pos
                break
            pos += 1
        userId = text[start:end].rsplit('_',1)[1].rstrip('"')
        return userId
    else:
        return False


def getRSSBridgeLink(userId):
    param = urlencode({'u': userId})
    rssBridgeUrl = ("https://rss-bridge.snopyta.org"
                    "/?action=display&bridge=Instagram"
                    "&context=Username&%s&media_type=all&format=Atom" % param
                    )
    return rssBridgeUrl


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('user', nargs='+', help='user to find id for')
    args = parser.parse_args()
    user_term = ' '.join(args.user)

    userId = getId(getUsernameResult(user_term))
    if (userId):
        rssLink = getRSSBridgeLink(userId)
        clipboard.copy(rssLink)
        print("Link copied to clipboard.")
    else:
        print("No id found.\nCheck spelling or try a different username.")
