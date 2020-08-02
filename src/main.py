from bs4 import BeautifulSoup
from urllib.parse import urlencode
import clipboard
import argparse
import requests

def getUsernameResult(username, column):
    if column == 'twitter':
        baseUrl = "https://nitter.net/{}/rss".format(username)
        response = requests.get(baseUrl)
        soup = BeautifulSoup(response.text, 'html.parser')
        if (soup.find('title').text) == 'Error | nitter':
            print("User doesn't exits")
            return
        else:
            return baseUrl
    else:
        baseUrl = "https://instagram.com/{}".format(username)

    response = requests.get(baseUrl)
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
    column = parser.add_mutually_exclusive_group()
    parser.add_argument('search', nargs='+', help='user to find id for')
    column.add_argument('-i', '--instagram', action='store_true',
                                            help='get Instagram url')
    column.add_argument('-t', '--twitter', action='store_true',
                                            help='get Twitter url')

    args = parser.parse_args()
    user_term = ' '.join(args.search)
    search_args = [(args.instagram, 'instagram'),
                    (args.twitter, 'twitter')]
    selColumn = 'def'
    for arg in search_args:
        if arg[0]:
            selColumn = arg[1]

    userId = getUsernameResult(user_term, selColumn)

    if (userId):
        if selColumn == 'twitter':
            clipboard.copy(userId)
        else:
            rssLink = getRSSBridgeLink(getId(userId))
            clipboard.copy(rssLink)
        print("Link copied to clipboard.")
    else:
        print("No id found.\nCheck spelling or try a different username.")
