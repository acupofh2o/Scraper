import os
import pandas as pd
import pymongo
import json


def import_content(filepath):
    mongo_client = pymongo.MongoClient('localhost', 27017)
    mongo_db = mongo_client['Apartamente']
    collection_name = 'Apartamente_Bucuresti'
    db_collection = mongo_db[collection_name]
    collection_dir = os.path.dirname(__file__)
    file_res = os.path.join(collection_dir, filepath)

    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    db_collection.remove()
    db_collection.insert(data_json)


if __name__ == "__main__":
    filepath = '/Users/silviu/Documents/proiectvlad/proiect/date_imobiliare.ro.csv'
    import_content(filepath)
ß