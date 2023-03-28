#   _       __        __        __
#   \_ \_   \_ \_   _/  \_   _/ _/
#     \   \   \_ \_/ _/\_ \_/ _/
#     \ all \   \___/    \___/
#    /rights \    \_ \__/ _/
#   /reserved |     \_  _/    ✿
#  |  WangYC /     _/__/_ _ _`|'
#  \  2023  /    _/ _ _ _ _ _/
#   \   © /    _/ _/
#     \_  \  _/ _/_ _ _ _ _
#       \_\_/_ _ _ _ _ _ _/

import streamlit as st
import pymongo as mg
from model import *

mg_client = mg.MongoClient("mongodb://localhost:27017/")
db_pub = mg_client['publications']
co_unread = db_pub['unread']
co_interstring = db_pub['interesting']
co_important = db_pub['important']
co_read = db_pub['read']

st.set_page_config(
    page_title="Ych's Reader", 
    page_icon="icon-trans.png"
)
def update_pub():
    try:
        current_pub = co_unread.find_one()
        return current_pub
    except:
        return

def show_st():
    global current_pub
    pub = current_pub
    try:
        st.header(pub['title'])
        # st.markdown(f"**Title:** {pub['title']}")
        st.markdown(f"**Date:** {pub['date']}")
        st.markdown(f"**Authors:** {', '.join(pub['authors'])}")
        st.markdown(f"**Page Link:** {pub['page']}")
        st.markdown(f"**PDF Link:** https://arxiv.org/pdf/{pub['page'].replace('https://arxiv.org/abs/', '')}.pdf")
        st.subheader('Abstract')
        st.markdown(pub['abstract'])
        st.subheader('Abs Trans')
        if pub['abs_trans'] == '':
            st.markdown('click the \'Translate Abs\' btn to get translation')
        else:
            st.markdown(f"**{pub['abs_trans'][0]}**")
            st.markdown(pub['abs_trans'][1])
    except:
        st.header('All recent publications have been read')

def f_interesting():
    global current_pub
    co_interstring.insert_one(current_pub)
    co_unread.delete_one(current_pub)
    current_pub = update_pub()
    # show_st()

def f_important():
    global current_pub
    co_important.insert_one(current_pub)
    co_unread.delete_one(current_pub)
    current_pub = update_pub()
    # show_st()

def f_read():
    global current_pub
    co_read.insert_one(current_pub)
    co_unread.delete_one(current_pub)
    current_pub = update_pub()
    # show_st()

def translate_abs():
    global current_pub
    current_pub = update_pub()
    title = current_pub['title']
    abs = current_pub['abstract']
    api = BaiDuFanyi()
    # api = OpenAI()
    # messages = [{'role' : 'system', 'content' : '将一下内容翻译成中文：\n'}, {'role' : 'user', 'content' : abs}]
    # show_st()
    # st.subheader('Abs Translation')
    try:
        # result = api.generate_response_chatgpt(messages=messages)
        # st.marddown(result)
        title_result = api.BdTrans(title.replace('\n', ''))
        result = api.BdTrans(abs.replace('\n', ''))
        myquery = { "_id": current_pub["_id"] }
        newvalues = { "$set": { "abs_trans": [title_result, '\n' + result]} }
        co_unread.update_one(myquery, newvalues)

    except:
        print('translation failed')



def main():
    global current_pub
    current_pub = update_pub()
    # st.title('Life is short, Reading is long')
    show_st()
    st.button('Translate Abs', on_click = translate_abs)
    # st.button('start!', on_click = show_st)
    # st.header('Classification')
    st.header(' ')
    st.subheader('Classification')
    col1, col2, col3 = st.columns(spec = 3, gap = 'small')
    with col1:
        st.button('interesting', on_click = f_interesting)
    with col2:
        st.button('important', on_click = f_important)
    with col3:
        st.button('pass', on_click = f_read)
    # st.header('Function')
    # st.subheader(' ')
    st.text(f"{co_unread.count_documents({})} pubs left in unread section")

    with st.sidebar:
        # st.header('Classification')
        st.image('icon-trans.png', width = 150)
        st.markdown('**WangYC @ RUC**')
        st.markdown('**All rights reserved ©️2023**')
    


main()
# unread_list = []
# for each in co_unread.find():
#     unread_list.append(each)

# for pub in unread_list:
#     st.title(pub['title'])
#     st.write('link : {}'.format(pub['page']))
#     st.write('published date : {}'.format(pub['date']))
#     st.write('authors : {}'.format(name for name in pub['authors']))
#     st.write(pub['abstract'])
    

