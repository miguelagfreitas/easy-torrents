import urllib2, os, sys
from itertools import izip

current_proxy = ''

def clear():
    if os.name == 'nt':
        os.system('cls')
    if os.name == 'posix':
        os.system('clear')

def get_mirrors():
    proxy_list_url = 'https://thepiratebay-proxylist.org/'

    try:
        print 'Connecting to proxy list...'
        req = urllib2.Request(proxy_list_url, headers={'User-Agent' : "Magic Browser"})
        con = urllib2.urlopen( req )
    except(HTTPError):
        print 'Could not connect to proxy list'
    except Exception as e:
        print 'Something went wrong'


    proxy_list_urls = []

    for line in con.readlines():
        if 'https' and 'tr data-probe' in line:
            proxy_list_urls.append('https://'+line.split('\"')[1].split('/')[2])

    return proxy_list_urls

def try_connections(proxy_list_urls):
    for url in proxy_list_urls:
        try:
            print 'Trying to connect to '+ url
            req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
            con = urllib2.urlopen(req)
            global current_proxy
            current_proxy = url
            print 'Connected succssfuly to '+ url
            create_query(url)
            break
        except(urllib2.HTTPError):
            print 'Could not connect to proxy list'


def create_query(url):
    user_input = raw_input('Search query:\n')
    q = user_input.replace(" ", "+")
    query = url + "/s/?q="+q+"&page=0&orderby=99"
    search_magnet(query)

def search_magnet(search_url):
    try:
        print 'Searching...\n'
        req = urllib2.Request(search_url, headers={'User-Agent' : "Magic Browser"})
        con = urllib2.urlopen(req)
        handle_search(con.readlines())
    except(urllib2.HTTPError):
        print 'Could not search on proxy'

def handle_search(html):
    search_urls = []
    search_prints = []
    for line in html:
        if 'td' or 'href' in line:
            if 'detLink' and 'Details' in line:
                search_url = current_proxy + line.split('"')[3]
                search_urls.append(search_url)
                search_prints.append(line.split(">")[2].replace("</a", ""))
            if 'align="right"' in line:
                search_prints.append(line.split(">")[1].replace("</td", ""))

    i = 0
    result_count = 10
    curr_result = 0
    while i < result_count*3:
        name = search_prints[i]
        seeds = search_prints[i+1]
        leechers = search_prints[i+2]
        if i % 3 == 0:
            print u'{0:85}  ({1}:{2})'.format((str)(curr_result+1) + ': ' +name, seeds, leechers)
            curr_result+=1
        i+=1

    user_search(search_urls)

def user_search(url_list):
    user_choice = raw_input("\n\n\nTorrent to download: \n")
    try:
        int(user_choice)
    except ValueError:
        print 'Invalid input'

    try:
        clear()
        print 'Fetching magnet...'
        req = urllib2.Request(url_list[int(user_choice)-1], headers={'User-Agent' : "Magic Browser"})
        con = urllib2.urlopen(req)
        fetch_magnet(con.readlines())
    except(urllib2.HTTPError):
        print 'Could not fetch magnet'

def fetch_magnet(html):
    magnet = ''
    for line in html:
        if 'icon-magnet' in line:
            magnet = line.split("\"")[3]
            break
    open_magnet(magnet)

def open_magnet(magnet):

    if(os.name == 'nt'):
        os.startfile(magnet)
    else:
        f = open("magnet_dump.txt", "wb")
        f.write(magnet+"\n")
        f.close()

if __name__ == '__main__':
    clear()
    try_connections(get_mirrors())
