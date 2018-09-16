## datamuse with caching

import requests
import json

# on startup, try to load the cache from file
CACHE_FNAME = 'cache_file_name.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

# function that accepts 2 parameters and returns a string that uniquely represents the request (url + params)
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

# main cache function: first look to see if have already cached the result and return it; if haven't, get a new one and cache it
def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)
    if unique_ident in CACHE_DICTION:     # look in the cache to see if we already have this data
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:   # if not, fetch the data afresh, add it to the cache
        print("Making a request for new data...")
        resp = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

# get data from the datamuse API, using the cache
def get_rhymes_from_datamuse_caching(rhymes_with):
    baseurl = "https://api.datamuse.com/words"
    params_diction = {}
    params_diction["rel_rhy"] = rhymes_with
    return make_request_using_cache(baseurl, params_diction)

# extract just the words from the data structures returned by datamuse
def get_word_list(data_muse_word_list):
    words = []
    for word_dict in data_muse_word_list:
        words.append(word_dict['word'])
    return words

# print up to 'max_rhymes' words that rhyme with 'word'
def print_rhymes(word, max_rhymes=10):
    rhymes = get_word_list(get_rhymes_from_datamuse_caching(word))
    print('Words that rhyme with', word)
    max2print = min(max_rhymes, len(rhymes))
    for i in range(max2print):
        print('\t', rhymes[i])

print_rhymes('blue')
print_rhymes('green')
print_rhymes('purple')
