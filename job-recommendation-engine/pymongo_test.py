import json

import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["job_platform"]

if __name__ == '__main__':
    collist = db.list_collection_names()
    print(collist)
    if "users_recommended_jobs" in collist:
        print("The collection exists.")

    col = db["users_recommended_jobs"]

    user = col.find_one({"email": "leti@gmail.com"})

    subdoc_to_insert = {
        "email": "leti@gmail.com",
        "jobs": [
            {"name": "galcevar", "company": "Endava"},
            {"name": "papusar", "company": "Amazon"}
        ]
    }

    jobs = [
        {"name": "galcevar", "company": "Endava"},
        {"name": "papusar", "company": "Amazon"}
    ]
    # db.Table.update({noExist: true}, {"$setOnInsert": {xxxYourDocumentxxx}}, {upsert: true})

    col.update_one(
        filter={
            "email": "jnapan@gmail.com",
        },
        update={
            '$setOnInsert': {
                'email': "alex@gmail.com",
                'jobs': jobs
                # 'jobs': [json.dumps(job) for job in jobs]
            },
            # '$set': {
            #     'last_update_date': now,
            # },
        },
        upsert=True,
    )

    mongo_client.close()
