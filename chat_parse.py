#depends on BeautifulSoup (e.g. via "pip install beautifulsoup4")

import json, re, urllib2
from bs4 import BeautifulSoup



samples = [
    { 
        'input' :     "@chris you around?",
        'output':     json.loads('{ "mentions": [ "chris" ] }')
    },
    { 
        'input' :     "Good morning! (megusta) (coffee)",
        'output':     json.loads('{ "emoticons": [ "megusta", "coffee" ]}')
    },
    { 
        'input' :     "Olympics are starting soon; http://www.nbcolympics.com",
        'output':     json.loads('{ "links": [ { "url": "http://www.nbcolympics.com", "title": "NBC Olympics | Home of the 2016 Olympic Games in Rio" } ] }')
    },
    { 
        'input' :     "@bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016",
        'output':     json.loads('{ "mentions": [ "bob", "john" ], "emoticons": [ "success" ], "links": [ { "url": "https://twitter.com/jdorfman/status/430511497475670016", "title": "Justin Dorfman on Twitter: \\"nice @littlebigdetail from @HipChat (shows hex colors when pasted in chat). http://t.co/7cI6Gjy5pq\\"" } ] }')
    }

]



def mentionHandler(s, result):
    if 'mentions' not in result:
        result['mentions'] = []
    result['mentions'].append(s[1:])


def emoticonHandler(s, result):
    if 'emoticons' not in result:
        result['emoticons'] = []
    result['emoticons'].append(s[1:-1])


def urlHandler(s, result):
    if 'links' not in result:
        result['links'] = []
    soup = BeautifulSoup(urllib2.urlopen(s))
    result['links'].append({ 'url' : s, 'title' : soup.title.string })



url_re = re.compile("https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,}")
elements = (
    { 'regex' : re.compile("@[a-z]*"),      'handler' : mentionHandler  },      #mentions
    { 'regex' : re.compile("\([a-z]*\)"),   'handler' : emoticonHandler },      #emoticons
    { 'regex' : url_re,                     'handler' : urlHandler      }       #urls
)
    
    
    


def parse(input):
    result = {}
    
    while True:
        closest_match = None
        for element in elements: 
            match = element['regex'].search(input)
            if match:
                index = match.start(0)
                if (not closest_match) or closest_match['index'] > index:
                    closest_match = { 'match' : match, 'index' : index, 'handler' : element['handler'] } 
                
        if closest_match:
            start = closest_match['match'].start(0)
            end = closest_match['match'].end(0)
            closest_match['handler'](input[start:end], result)
            input = input[end:]
        else:
            return result
        
        
                


def main():
    for sample in samples:
        parsed = parse(sample['input'])
        if parsed != sample['output']:
            raise Exception('Wrong output for %s\nExpected: %s\nGot: %s' % (sample['input'], json.dumps(sample['output']), json.dumps(parsed)))
    
    print 'Success'




if __name__ == '__main__': 
    main()







