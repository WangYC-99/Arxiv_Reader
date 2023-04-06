import streamlit as st
import pymongo as mg

mg_client = mg.MongoClient("mongodb://localhost:27017/")
db_pub = mg_client['publications']
co_important = db_pub['important']
co_interesting = db_pub['interesting']
co_read = db_pub['read']
co_unread = db_pub['unread']
read_pubs = co_read.find({}).sort([("_id", -1)])

st.set_page_config(
    page_title="Ych's Reader", 
    page_icon="icon-trans.png"
)

def show_st(pub):
    try:
        st.header(pub['title'])
        # st.markdown(f"**Title:** {pub['title']}")
        st.markdown(f"**Date:** {pub['date']}")
        st.markdown(f"**Area:** {pub['Area']}")
        st.markdown(f"**Authors:** {', '.join(pub['authors'])}")
        st.markdown(f"**Page Link:** {pub['page']}")
        st.markdown(f"**PDF Link:** https://arxiv.org/pdf/{pub['page'].replace('https://arxiv.org/abs/', '')}.pdf")
        st.subheader('Abstract')
        st.text(pub['abstract'])
        if pub['abs_trans'] == '':
            st.text(' ')
        else:
            st.markdown(f"**{pub['abs_trans'][0]}**")
            st.markdown(pub['abs_trans'][1])
    except:
        st.header('All recent publications have been read')

def move_to_important(current_pub):
    co_important.insert_one(current_pub)
    co_read.delete_one(current_pub)

def move_to_interesting(current_pub):
    co_interesting.insert_one(current_pub)
    co_read.delete_one(current_pub)

def move_to_unread(current_pub):
    co_unread.insert_one(current_pub)
    co_read.delete_one(current_pub)

def main():
    st.title('Life is short, Reading is long')
    with st.sidebar:
        st.image('icon-trans.png', width = 150)
        st.markdown('**WangYC @ RUC**')
        st.markdown('**All rights reserved ©️2023**')

    for each in read_pubs:
        show_st(each)
        st.button('move to important', key = each['_id'] + '.1', on_click = move_to_important, kwargs = dict(current_pub = each))
        st.button('move to interesting', key = each['_id'] + '.2', on_click = move_to_interesting, kwargs = dict(current_pub = each))
        st.button('move to unread', key = each['_id'] + '.3', on_click = move_to_unread, kwargs = dict(current_pub = each))

main()