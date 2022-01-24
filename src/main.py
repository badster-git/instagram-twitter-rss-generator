from bs4 import BeautifulSoup
from urllib.parse import urlencode
import clipboard
import argparse
import requests

def getUsernameResult(username, column):
    if column == 'instagram':
        return getRSSBridgeLink(username)
    else:
        baseUrl = "https://nitter.pussthecat.org/{}/rss".format(username)
        response = requests.get(baseUrl, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        if (soup.find('title').text) == 'Error | nitter':
            print("User doesn't exist")
            return
        else:
            return baseUrl

def getRSSBridgeLink(username):
    param = urlencode({'u': username})
    rssBridgeUrl = ("https://feed.eugenemolotov.ru/"
                    "/?action=display&bridge=Instagram"
                    "&context=Username&%s&media_type=all&format=Atom" % param
                    )
    response = requests.get(rssBridgeUrl, verify=False)
    if response.status_code != 500:
        return rssBridgeUrl
    else:
        return False


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

    rssLink = getUsernameResult(user_term, selColumn)

    if (rssLink):
        if selColumn == 'twitter':
            clipboard.copy(rssLink)
        else:
            clipboard.copy(rssLink)
        print("Link copied to clipboard.")
    else:
        print("No id found.\nCheck spelling or try a different username.")
