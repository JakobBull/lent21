''' functions to aid with finding video codes from youtube and creating lists of them '''

from youtube_search import YoutubeSearch
from sql_utils import sqliteExecute
from random import randint

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

def get_related_questions(search_key, max_questions=10, random=True):
    query = 'SELECT * FROM Questions WHERE topics = ?'
    params = (search_key,)
    result = sqliteExecute(query, params)

    related_questions = []
    
    if random == True:

        i = 0
        counter = 0

        while i < max_questions and counter < 100:

            # pick random number
            r = randint(0,len(result)-1)
            q_id = result[r][0]
            name = result[r][-1]

            if (q_id, name) not in related_questions:
                related_questions.append((q_id, name))

                i += 1
                
            counter += 1
    else:
        for i in range((result)):
            if i < max_questions:
                related_questions.append((result[i][0], result[i][-1]))
            else:
                break
    
    return related_questions