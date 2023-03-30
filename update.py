 # -*- coding: utf-8 -*-

import requests
import re
import json
import pymongo as mg
import sys


def update_pubs(area, retrive_num):

    response = requests.get(url='https://arxiv.org/list/cs.{}/pastweek?skip=0&show={}'.format(area, retrive_num))
    result = response.text

    comb_pattern = re.compile(r'<dt>[\s\S]*?<\/dt>\n<dd>[\s\S]*?<\/dd>')
    title_pattern = re.compile(r'Title:<\/span>([\s\S]*?)\n<\/div>')
    author_pattern = re.compile(r'<a href="\/search\/[\s\S]*?>([\s\S]*?)<\/a>')
    url_pattern = re.compile(r'<a href="([\s\S]*?)" title="Abstract">')
    abstract_pattern = re.compile(r'<span class="descriptor">Abstract:<\/span>([\s\S]*?)<')
    date_pattern = re.compile(r'<div class=\"dateline\">[\s\S]*?\[Submitted on ([\s\S]*?)\][\s\S]*?<\/div>')

    print('Retriving recent publications ...')

    publication_library = re.findall(pattern=comb_pattern, string=result)

    pub_content_list = []

    counter = 1
    for pub in publication_library:
        print('\r {} / {}  [#{}]'.format(str(counter), str(len(publication_library)), int(counter / len(publication_library) * 15) * '#' + (15 - int(counter / len(publication_library) * 15)) * '·') , end='')
        title = re.findall(pattern=title_pattern, string=pub)[0]
        author_list = re.findall(pattern=author_pattern, string=pub)
        url = re.findall(pattern=url_pattern, string=pub)[0]
        abstract_page_txt = requests.get(url='https://arxiv.org' + url).text
        abstract = re.findall(pattern=abstract_pattern, string=abstract_page_txt)[0]
        date = re.findall(pattern=date_pattern, string=abstract_page_txt)[0]
        id = url.replace('/abs/', '')

        pub_content_list.append({
            '_id' : id,
            'date' : date,
            'area' : area,
            'title' : title,
            'authors' : author_list,
            'abstract' : abstract,
            'page' : 'https://arxiv.org' + url,
            'abs_trans' : ''
        })

        counter += 1

    mg_client = mg.MongoClient("mongodb://localhost:27017/")
    db_pub = mg_client['publications']

    co_unread = db_pub['unread']
    co_interesting = db_pub['interesting']
    co_read = db_pub['read']
    co_important = db_pub['important']

    print('\n updating database')
    # co_unread.insert_many(pub_content_list)
    for each in pub_content_list:
        query = {"_id" : each["_id"]}
        if co_interesting.count_documents(query) == 0 and co_read.count_documents(query) == 0 and co_important.count_documents(query) == 0 and co_unread.count_documents(query) == 0:
            try:
                co_unread.insert_one(each)
            except:
                print('error : https://arxiv.org/abs/{}'.format(each["_id"]))
                continue
        else :
            print('exist : https://arxiv.org/abs/{}'.format(each["_id"]))
    # with open('pubs.json', mode='w', encoding='utf-8') as f:
    #     f.write(json.dumps(pub_content_list, ensure_ascii= True, indent=4))

if __name__ == '__main__':
    area = sys.argv[1]
    retrive_num = sys.argv[2]
    update_pubs(area, retrive_num)