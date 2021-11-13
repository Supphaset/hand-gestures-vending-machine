def get_database():
    from pymongo import MongoClient
    import certifi
    import pymongo

    CONNECTION_STRING = 'mongodb+srv://mechatronic:mechatronic@cluster0.el0zv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

    return client['mechatronic']


if __name__ == '__main__':
    dbname = get_database()
    collection_name = dbname['items']
    item_1 = {
        'name': 'Item_1',
        'qty': 3
    }
    item_2 = {
        'name': 'Item_2',
        'qty': 3
    }
    item_3 = {
        'name': 'Item_3',
        'qty': 3
    }
    item_4 = {
        'name': 'Item_4',
        'qty': 3
    }
    item_5 = {
        'name': 'Item_5',
        'qty': 3
    }
    collection_name.delete_many({})
    collection_name.insert_many([item_1, item_2, item_3, item_4, item_5])
