#/spotifize.py
import pycurl #/requires pycurl + curl
import cStringIO
import urllib
import sys
import argparse

class searcher(object):
    '''this object will do your searching for you.'''
    def __init__(self):
        '''this method is the init for the object'''
        self.search_string = ''
        self.results_string_io = cStringIO.StringIO()
        self.results_str = ''
        self.curl_obj = pycurl.Curl()
        self.saved_results = []

    def search(self, search_string, save_results=False, search_field='album'):
        '''this method will search a given search string'''

        #this block resets the cStringIO obj
        try:
            self.results_string_io.reset()
        except:
            pass

        #this line url-ifies the search string w/ %20 escapes, etc.
        http_string = urllib.quote(search_string)

        #here is the pycurl stuff for the lookup
        self.curl_obj.setopt(self.curl_obj.URL,
            "http://ws.spotify.com/search/1/{0}?q={1}".format(search_field, http_string))
        self.curl_obj.setopt(self.curl_obj.WRITEFUNCTION, self.results_string_io.write)
        self.curl_obj.perform()

        #gets the value from the string buffer
        self.results_str = self.results_string_io.getvalue()

        #save the results if appropriate
        if save_results:
            self.saved_results.append(results_str)

        return self.results_str

if __name__ == "__main__":
    '''the main method for this script'''
    parser = argparse.ArgumentParser("seach spotify with python")
    parser.add_argument('-f', dest="to_file", action="store", default='',
        help="writes the results to file")
    parser.add_argument('-s', dest="search_field", action="store", default='album',
        help="what field to search. default is 'album', other allowed" + \
            " variables are 'artist' and 'track'")
    parser.add_argument('search_term', metavar="<SEARCH TERM>", nargs="+",
        help="the term or terms to search for")
    #print "search_term: {0}".format(search_term) #debug
    #print "creating searcher object" #debug
    my_searcher = searcher()
    #print "running search" #debug
    args = parser.parse_args()
    print "args: {}".format(args) #debug
    print " ".join(args.search_term) #debug
    search_term = " ".join(args.search_term)
    result = my_searcher.search(search_term, False, args.search_field)
    if args.to_file is '':
        print result #debug
    else:
        with open(args.to_file, 'w') as fd:
            fd.write(result)
