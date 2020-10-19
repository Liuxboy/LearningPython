#!/usr/bin/env python

import pymongo
import datetime
from pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['runoob']
collection = db['runboot']

new_posts = [
    {
        "author": "Mike",
        "text": "Another post!",
        "tags": ["bulk", "insert"]
    },
    {
        "author": "Eliot",
        "title": "MongoDB is fun",
        "text": "and pretty easy too!"
    }
]

result = collection.insert_many(new_posts)
print(result.inserted_ids)














