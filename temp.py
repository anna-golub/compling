import requests
import json
from pprint import pprint

access_token = '1d89d822b63e9af98d521371c965ac90abbed8b55130dece30495955ef0de46ea2b30407d33f9f22450a1'
vk_config = {'token': access_token,
             'client_id': '7219880',
             'version': '5.124',
             'domain': 'https://api.vk.com/method/'}


req = requests.get(vk_config['domain'] + 'wall.get', params={'access_token': vk_config['token'],
                                                             'v': vk_config['version'],
                                                             'account_id': vk_config['client_id'],
                                                             'domain': 'comfortnayazona',
                                                             'count': 100})
posts_data = req.json()['response']['items']
print(len(posts_data))
texts_data = dict()
words_count = 0
posts_count = 0

for i in range(len(posts_data)):
    # print(posts_data[i]['text'])
    # print()

    # запрос комментариев к посту
    comment_req = requests.get(vk_config['domain'] + 'wall.getComments',
                               params={'access_token': vk_config['token'],
                                       'v': vk_config['version'],
                                       'account_id': vk_config['client_id'],
                                       'owner_id': -112252091,
                                       'post_id': posts_data[i]['id'],
                                       'sort': 'asc'})
    comments_data = dict()
    if 'response' in comment_req.json():
        comments_data = comment_req.json()['response']['items']

    # записываем сам пост
    posts_count += 1
    print('id =', posts_data[i]['id'])

    post_id = len(texts_data)
    words_number = len(posts_data[i]['text'].split())
    words_count += words_number
    texts_data[post_id] = {'type': 'post',
                           'text': posts_data[i]['text'],
                           'words_number': words_number,
                           'comments_number': len(comments_data),
                           'comments_ids': []}

    # записываем комментарии
    for j in range(len(comments_data)):
        if 'text' not in comments_data[j]:
            continue

        comment_id = len(texts_data)
        texts_data[post_id]['comments_ids'].append(comment_id)

        try:
            words_number = len(comments_data[j]['text'].split())
        except Exception as e:
            print(str(e))
            print(comments_data[j])
            break

        words_count += words_number
        texts_data[comment_id] = {'type': 'comment',
                                  'text': comments_data[j]['text'],
                                  'words_number': words_number,
                                  'post_id': post_id}

    if words_count >= 10000 and len(texts_data) >= 200:
        print('texts:', len(texts_data), 'words:', words_count, 'posts:', posts_count)
        # break

with open('data.json', 'w', encoding='utf-8') as fout:
    json.dump(texts_data, fout, ensure_ascii=False)
# pprint(texts_data)
