''' functions to aid with finding video codes from youtube and creating lists of them '''

from youtube_search import YoutubeSearch
from sql_utils import sqliteExecute

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

def get_video_codes(vid_dict):

    ''' 

    input a dict from youtube_search and return list of codes

    '''

    #assert type(vid_dict) == dict

    vid_list = []
    for i, item in enumerate(vid_dict):
        vid_list.append(item['id'])

    return vid_list

def get_related_questions(search_key):
    query = 'SELECT * FROM Questions WHERE topics = ?'
    params = (search_key,)
    result = sqliteExecute(query, params)

    related_questions = []
    max_questions = 3
    for i, item in enumerate(result):
        if i < max_questions:
            related_questions.append((item[0], item[-1]))
        else:
            break
    
    return related_questions