from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os


def try_getting_pb(tries):
    table = driver.find_elements_by_class_name('proxies')[0]
    tr = table.find_elements_by_tag_name('tr')[tries+1]
    return tr.find_elements_by_tag_name('td')[0].text

def valid_page():
    valid_title = "Download music, movies, games, software! The Pirate Bay - The galaxy's most resilient BitTorrent site"
    return driver.title == valid_title

def query_string(query):
    q = query.replace(" ", "+")
    return "/s/?q="+q+"&page=0&orderby=99"

driver = webdriver.Remote(
   command_executor='http://127.0.0.1:4444/wd/hub',
   desired_capabilities={'browserName': 'htmlunit',
                         'version': '2',
                        'javascriptEnabled': True})


proxy_list = "https://thepiratebay-proxylist.org/"
driver.get(proxy_list)

tries = 30

for counter in range(0, tries):

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    domain = try_getting_pb(counter)
    link = "https://" + domain
    print "Trying "+link+"..."
    driver.get(link)
    if valid_page():
        break

print "\nSuccessfuly got Pirate Bay proxy: "+link

query = raw_input("\nSearch query:\n")


driver.get(link + query_string(query))
print("\n\n\n")

results = driver.find_elements_by_id('searchResult')[0].find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

result_count = 19
i = 0

os.system('cls')

magnets = []

for result in results:
    row = result.find_elements_by_tag_name('td')[1].find_elements_by_tag_name('a')[0]
    magnets.append(result.find_elements_by_tag_name('td')[1].find_elements_by_tag_name('a')[1])
    seeds = result.find_elements_by_tag_name('td')[2].text
    leechers = result.find_elements_by_tag_name('td')[3].text

    try:
        print u'{0:85}  ({1}:{1})'.format((str)(i+1) + ': ' +row.text, seeds, leechers)
    except Exception as e:
        print "[Decode Error]"
        i-=1

    if i == result_count:
        break
    i+=1

user_choice = raw_input("\nChoose torrent to download\n")

driver.get(magnets[int(user_choice)-1].get_attribute('href'))

dl_button = driver.find_elements_by_class_name('download')[0].find_elements_by_tag_name('a')[0]

if os.name == 'nt':
    os.startfile(dl_button.get_attribute('href'))
else:
    pass
