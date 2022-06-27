#!/Users/silviuh1/PycharmProjects/job-recommendation-engine/venv/bin/python

import json
from sys import path
from sys import argv

import pymongo
from flask import Flask, request
from textblob import TextBlob
from WordCrunchingEngine import WordCrunchingEngine
import textract
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io
import logging

import os.path
from os import path

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["job_platform"]
col = db["users_recommended_jobs"]
jobs_col = db["jobs"]


def parse_pdf(file_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(file_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    return text


def preprocess_jobs_for_users(email, resume_path):
    # logger = logging.getLogger()
    # handler = logging.FileHandler('user-cronjobs-logs/' + email + ".log")
    # logger.addHandler(handler)
    # logger.error('Our First Log Message')

    Log_Format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(
        filename="/Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/user-cronjobs-logs/" + email + ".log",
        filemode="a+",
        format=Log_Format,
        level=logging.INFO)
    logger = logging.getLogger()

    print("[ " + email + " ]:" + " START")
    logger.info("\n\n\n\n[STARTS] RECOMMENDING")
    result_data = []

    resume = ""
    if path.exists(resume_path):
        ext = os.path.splitext(str(resume_path))[-1].lower()
        if ext == '.pdf':
            resume = parse_pdf(resume_path)
        elif ext == '.txt':
            with open(resume_path, 'r') as f:
                resume = f.read()  # Read whole file in the file_content string
    else:
        print("The user resume file does not exist")
        # return "The user resume file does not exist"

    raw_jobs = jobs_col.find()
    # print("JOBS length: " + str(len(list(raw_jobs))))

    for job in raw_jobs:
        result_data.append(
            word_crunching_engine.matching_keywords(job, resume))

    recommended_jobs = sorted(result_data, key=lambda k: float(k['score']),
                              reverse=True)

    # for idx, job in enumerate(recommended_jobs):
    #     print("[ " + str(idx) + " ]" + " " + job["jobName"] + ": " + job["score"] + " | " + str(
    #         job["title_common_nr_words"]) + " | " + str(job[
    #                                                         "title_common_percentage"]))

    # print(recommended_jobs)

    col.update_one(
        filter={
            "email": email,
        },
        update={
            '$set': {
                'email': email,
                'jobs': recommended_jobs
                # 'jobs': [json.dumps(job) for job in jobs]
            }
            # '$set': {
            #     'last_update_date': now,
            # },
        },
        upsert=True,
    )

    print("[ " + email + " ]:" + " END")
    logger.info("[ENDS] RECOMMENDING")


if __name__ == '__main__':
    word_crunching_engine = WordCrunchingEngine()
    print(str(argv[1]))
    print(str(argv[2]))
    preprocess_jobs_for_users(str(argv[1]), str(argv[2]))  # argv[1] = email, argv[2] = resume_path
