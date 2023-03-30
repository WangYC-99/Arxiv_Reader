import streamlit as st
import pymongo as mg

mg_client = mg.MongoClient("mongodb://localhost:27017/")
db_pub = mg_client['publications']
co_important = db_pub['important']
co_interesting = db_pub['interesting']
co_read = db_pub['read']
co_unread = db_pub['unread']
important_pubs = co_important.find({}).sort([("_id", -1)])
global note_text

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

def move_to_interesting(current_pub):
    co_interesting.insert_one(current_pub)
    co_important.delete_one(current_pub)

def move_to_read(current_pub):
    co_read.insert_one(current_pub)
    co_important.delete_one(current_pub)

def move_to_unread(current_pub):
    co_unread.insert_one(current_pub)
    co_important.delete_one(current_pub)

def main():
    global note_text
    # st.title('Life is short, Reading is long')
    note_text = st.text_input('notes', '')
    st.text(note_text)
    st.text('hello')
    with st.sidebar:
        st.image('icon-trans.png', width = 150)
        st.markdown('**WangYC @ RUC**')
        st.markdown('**All rights reserved ©️2023**')
    

main()