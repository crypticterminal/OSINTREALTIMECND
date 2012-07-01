#!/usr/local/bin/python

import sys, datetime, json, twitter, re, glob

# Generic function to create CSV full paste url and full path to the paste
def globof_files(path, filter_name):
    files = glob.glob(path)
    for filename in files:
        suffix = filter_name
        if filename.endswith(suffix) == True:
            yield(filename)
            
# WatchList string list convert to list datastructure generator object
def username_watchlist(watchlist_username):
    for line in open(watchlist_username, 'r'):
        yield line.strip('\n')
        


# WatchList string list convert to list datastructure generator object
def search_watchlist(watchlist_search):
    for line in open(watchlist_search, 'r'):
        yield line.strip('\n')

# Search Twitter Function
def search_twitter(search_usernames, search_list, int_one, int_two, output_file_name):
    MAX_PAGES = int_one
    RESULTS_PER_PAGE = int_two
    twitter_search = twitter.Twitter(domain="search.twitter.com")
    search_results = []
    for page in range(1,MAX_PAGES+1):
        for search_string in search_usernames:
            search_results += twitter_search.search(q=search_string, rpp=RESULTS_PER_PAGE, page=page)['results']
            for result in search_results:
                if search_string.split('@')[1] in result['from_user_name']:
                    for search_element in search_list:
                        ipsrch = re.compile(r'\b%s\b' %search_element, re.IGNORECASE)
                        if ipsrch.findall(result['text']):
                            with open(output_file_name, "a") as f:
                                f.write(json.dumps(result, indent=0))

# Global Variables
path = "/Users/alienone/Downloads/alienone-PASTEBIN-9fd9c83/twitter/*.txt"
filter_name = ".txt"
watchlist_username = "watchlist/twitter_usernames.txt"
watchlist_search = "watchlist/twitter_watchlist.txt"
search_usernames = [i for i in username_watchlist(watchlist_username)]
search_list = [i for i in search_watchlist(watchlist_search)]
int_one = 2
int_two = 50
date_time_one = (str(datetime.datetime.now()).split(' ')[0])
date_time_two = (str(datetime.datetime.now())).split(' ')[1].replace(':','-').split('.')[0]
output_file_name = 'culled_twit_files/' + "Twitter_Hits-" + date_time_one + "-" + date_time_two + '.txt'


# Main Execution
if __name__ == '__main__':
    search_twitter(search_usernames, search_list, int_one, int_two, output_file_name)
    