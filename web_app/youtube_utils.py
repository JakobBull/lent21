''' functions to aid with finding video codes from youtube and creating lists of them '''

from youtube_search import YoutubeSearch

def youtube_search(key_list, max_results=10, return_type='dict'):

    ''' 

    input a list of key terms and recieve a json or dict of
    youtube videos when keywords are searched

    '''

    if return_type == 'dict':
        results = YoutubeSearch(key_list, max_results).to_dict()
    elif return_type == 'json':
        results = YoutubeSearch(key_list, max_results).to_json()
    else:
        ValueError('return_type must equal dict or json')

    return results

def get_video_code(url):

    ''' 

    input a url strig of a youtube video and return the code

    '''

    assert type(url) == str
    assert url[:24] == 'https://www.youtube.com/'
    print(url[:24])
    start = url.index('=')
    code = url[start+1:]

    return code

#print(get_video_code('https://www.youtube.com/watch?v=Fnp2em6txUY'))
#print(youtube_search('hello world', return_type='json'))