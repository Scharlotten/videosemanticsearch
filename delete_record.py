from astrapy import DataAPIClient

# Initialize the client
client = DataAPIClient("AstraCS:xZZxdLNLDuHQLsJCufhzpgXe:0dc79e1207afcf8a82d53f0a6c39d76eb66835072383f5ee7c1b7e0af3f4de17")
db = client.get_database_by_api_endpoint(
     "https://1e68bb5b-25b9-4ec7-8ca9-634838472600-us-east-2.apps.astra.datastax.com",
    namespace="default_keyspace",
)
mycoll = db.get_collection("mycollection")      

#mycoll.insert_one({"name": "Jane Doe"})
#print(f"Successfully inserted into collection")

g = mycoll.find_one({"name": "Jane Doe"})
print(g)
   

#mycoll.delete_one({"name": "Jane Doe"})
#print("Successfully deleted from collection")
#print(f"Connected to Astra DB: {db.list_collection_names()}")