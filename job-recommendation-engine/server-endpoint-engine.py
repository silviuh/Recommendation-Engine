#!/Users/silviuh1/PycharmProjects/job-recommendation-engine/venv/bin/python

import json
from sys import path
from sys import argv

import pymongo
from crontab import CronTab
from flask import Flask, request
from googletrans import Translator
from textblob import TextBlob

from ResumeParser import ResumeParser
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

    converter.close()
    fake_file_handle.close()

    return text


def preprocess_jobs_for_users(email, resume_path):
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
                resume = f.read()
        elif ext == ".doc" or ext == ".docx":
            resume = textract.process(resume_path).decode('utf-8')
    else:
        print("The user resume file does not exist")

    # request_data = {"resumePath": resume_path}
    # resume = resume_parser.parse_request_data(request_data)

    try:
        resume_detected_language = translator.detect(
            str(resume).replace(" ", "").replace('\n', '').replace('\r', '')[:500]).lang
    except Exception as e:
        print(e)

    raw_jobs = jobs_col.find()

    for job in raw_jobs:
        result_data.append(
            word_crunching_engine.matching_keywords(job, resume, resume_detected_language))

    recommended_jobs = sorted(result_data, key=lambda k: float(k['score']),
                              reverse=True)

    col.update_one(
        filter={
            "email": email,
        },
        update={
            '$set': {
                'email': email,
                'jobs': recommended_jobs
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
    translator = Translator()
    resume_parser = ResumeParser()
    word_crunching_engine = WordCrunchingEngine()
    preprocess_jobs_for_users(str(argv[1]), str(argv[2]))  # argv[1] = email, argv[2] = resume_path
