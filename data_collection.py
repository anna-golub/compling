import requests
import json
from pprint import pprint
import time

access_token = ''
vk_config = {'token': access_token,
             'client_id': '',
             'version': '5.124',
             'domain': 'https://api.vk.com/method/'}


def get_data(offset: int):
    words_count = 0
    posts_count = 0
    comments_count = 0

    req = requests.get(vk_config['domain'] + 'wall.get',
                       params={'access_token': vk_config['token'],
                               'v': vk_config['version'],
                               'account_id': vk_config['client_id'],
                               'domain': 'comfortnayazona',
                               'count': 100,
                               'offset': offset})
    posts_data = req.json()['response']['items']
    for i in range(len(posts_data)):
        time.sleep(1)

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
        post_id = len(texts_data)

        words_number = 0
        word_arr = posts_data[i]['text'].split('\n')
        word_arr = [v.split() for v in word_arr]
        for arr in word_arr:
            words_number += len(arr)
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
            comments_count += 1
            comment_id = len(texts_data)
            texts_data[post_id]['comments_ids'].append(comment_id)

            words_number = 0
            word_arr = comments_data[j]['text'].split('\n')
            word_arr = [v.split() for v in word_arr]
            for arr in word_arr:
                words_number += len(arr)
            words_count += words_number

            texts_data[comment_id] = {'type': 'comment',
                                      'text': comments_data[j]['text'],
                                      'words_number': words_number,
                                      'post_id': post_id}
        texts_data[post_id]['comments_number'] = len(texts_data[post_id]['comments_ids'])

        print('post_id =', post_id, 'comments number =', texts_data[post_id]['comments_number'])
        if texts_data[post_id]['comments_number'] == 0:
            print(comment_req.json())

    return words_count, posts_count, comments_count


if __name__ == '__main__':
    texts_data = dict()
    words_total, posts_total, comments_total = 0, 0, 0

    for k in range(5):
        print(k)
        w, p, c = get_data(offset=k * 50)
        words_total += w
        posts_total += p
        comments_total += c
        if words_total >= 10000 and len(texts_data) >= 200:
            print('texts:', len(texts_data), 'words:', words_total)
            print('posts:', posts_total, 'comments:', comments_total)
            print('words average =', round(words_total/len(texts_data), 3))
            break

    with open('corpus.json', 'w', encoding='utf-8') as fout:
        json.dump(texts_data, fout, ensure_ascii=False)
    # pprint(texts_data)
