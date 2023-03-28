import pymongo as mg

mg_client = mg.MongoClient("mongodb://localhost:27017/")
db_pub = mg_client['publications']

co_unread = db_pub['unread']
example = co_unread.find_one()

print(example['abstract'].replace('\n', ''))
# co_intersting = db_pub['intersting']
# co_read = db_pub['read']
# co_important = db_pub['important']

# query = {"_id" : co_unread.find_one()["_id"]}
# result = co_unread.count_documents(query)
# print(result)