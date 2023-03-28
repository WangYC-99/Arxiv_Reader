import pymongo as mg

mg_client = mg.MongoClient("mongodb://localhost:27017/")
db_pub = mg_client['publications']
co_unread = db_pub['unread']
co_interesting = db_pub['interesting']
co_important = db_pub['important']
co_read = db_pub['read']

co_read.delete_many({})
co_unread.delete_many({})
co_interesting.delete_many({})
co_important.delete_many({})
