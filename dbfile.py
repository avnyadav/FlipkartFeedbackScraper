

import pymongo

#DB_URL = 'mongodb://localhost:27017/'#'mongodb+srv://Avnish:<Aa327030>@cluster0.5fvxl.mongodb.net/<dbname>?retryWrites=true&w=majority'
DB_URL='mongodb+srv://Avnish:Aa327030@cluster0.5fvxl.mongodb.net/<dbname>?retryWrites=true&w=majority'
def getDatabaseClientObject():
    try:
        client = pymongo.MongoClient(DB_URL)
        return client
    except Exception as e:
        raise Exception("Failed to create database connection object-->", str(e))


def closeDatabaseClientobject(obj_name):
    try:
        obj_name.close()
        return True
    except Exception as e:
        raise Exception("Failed to close database connection-->", str(e))




def checkDataBase(client,db_name):
    try:
        if db_name in client.list_database_names():
            return True
        else:
            return False
    except Exception as e:
        raise Exception("Failed to check database exist or not", str(e))



def createDatabase(db_client, db_name):
    """
    db_client: client object of database
    db_name:data base name
    """
    try:
        return db_client[db_name]
    except Exception as e:
        raise Exception("Failed to create database")




def createCollectionInDatabase(database_name, collection_name):
    """
    database_name:name of data
    collection_name: name of collection
    """
    try:
        return database_name[collection_name]
    except Exception as e:
        raise Exception("Failed to create collection [{0}] in database [{1}] --error:[{2}]".format(str(collection_name),
                                                                                                   str(database_name),
                                                                                                   str(e)))



def checkExistenceCollection(COLLECTION_NAME, DB_NAME, db):
    try:
        """It verifies the existence of collection name in a database"""
        collection_list = db.list_collection_names()

        if COLLECTION_NAME in collection_list:
            print(f"Collection:'{COLLECTION_NAME}' in Database:'{DB_NAME}' exists")
            return True

        print(
            f"Collection:'{COLLECTION_NAME}' in Database:'{DB_NAME}' does not exists OR \n        no documents are present in the collection")
        return False
    except Exception as e:
        raise Exception("Exception occured:", str(e))






def CreateOneRecord(collection, data):
    try:
        collection.insert_one(data)
        print("Record inserted")
        return True
    except Exception as e:
        raise Exception("Failed to insert record ", str(e))



def getCollection(collection_name,db_name):
    try:
        collection=createCollectionInDatabase(db_name,collection_name)
        return collection
    except Exception as e:
        raise Exception("Failed to find collection",str(e))
def createMutlipleRows(collection, data):
    try:
        collection.insert_many(data)
        print("data inserted")
    except Exception as e:
        raise Exception("Failed to insert record ", str(e))



def addDatatoColleciton(data):
    try:
        client = getDatabaseClientObject()
        db_name = createDatabase(client, "flipkart")
        collection = getCollection("flipkartproduct", db_name)
        createMutlipleRows(collection,data)
        return True
    except Exception as e:
        raise Exception("Failed to fetch detail from collection", str(e))
    finally:
        closeDatabaseClientobject(client)




def getDataFromCollection(search_product):
    try:
        client = getDatabaseClientObject()
        database_name="flipkart"
        collection_name="flipkartproduct"
        if not checkDataBase(client,database_name):
            return False
        db_name = createDatabase(client, "flipkart")
        query = {"product searched": search_product}

        if not checkExistenceCollection(collection_name,database_name,db_name):
            print('collection not present')

            return False
        collection = getCollection(collection_name, db_name)
        data = []
        res = collection.find(query)
        if res.count() > 0:
            for r in res:
                data.append(r)
            return data
        else:
            return False
    except Exception as e:
        raise Exception("Failed to fetch detail from collection", str(e))
    finally:
        closeDatabaseClientobject(client)




