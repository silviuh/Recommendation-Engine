import json
from sys import path

import pymongo
from crontab import CronTab
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

import os.path
from os import path

app = Flask(__name__)

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


# GET requests will be blocked
@app.route('/get-score', methods=['POST'])
def get_score():
    request_data = request.get_json()
    result = {
        "container_data": []
    }
    result_data = []

    for job in request_data['jobPosting']:
        # if job['jobDescription'] == '' or request_data['resume'] == '':
        #     continue

        # result_data.append(
        #     word_crunching_engine.matching_keywords(jobDescription['jobDescription'], request_data['resume'],
        #                                             request_data['language'], jobDescription['_id'],
        #                                             jobDescription['jobName'], jobDescription['jobLocation']))
        result_data.append(
            word_crunching_engine.matching_keywords(job, request_data[
                'resume']))  # receives dict, converts into json with dumps
        # result_data.append(json.dumps(
        #     word_crunching_engine.matching_keywords(job, request_data[
        #         'resume'])))  # receives dict, converts into json with dumps

    # result['container_data'] = sorted(result_data, key=lambda k: json.loads(k)['result_data']['score'],
    #                         reverse=True)  # converts into dict for data processing - sorting with loads

    # result['container_data'] = sorted(result_data, key=lambda k: json.loads(k)['score'],
    #                                   reverse=True)

    result['container_data'] = sorted(result_data, key=lambda k: float(k['score']),
                                      reverse=True)

    # print(json.dumps(result))
    # return json.dumps(result)
    # for json in result['container_data']:
    #     print(json['jobLocation'] + " " + json['score'])
    return result


@app.route('/preprocess-jobs-for-users', methods=['POST'])
def preprocess_jobs_for_users():
    print("[STARTS] RECOMMENDING")
    request_data = request.get_json()
    result = {
        "container_data": []
    }
    result_data = []

    resume = ""
    if path.exists(request_data["resumePath"]):
        ext = os.path.splitext(str(request_data["resumePath"]))[-1].lower()
        if ext == '.pdf':
            resume = parse_pdf(request_data["resumePath"])
        elif ext == '.txt':
            with open(request_data["resumePath"], 'r') as f:
                resume = f.read()  # Read whole file in the file_content string
    else:
        return "The user resume file does not exist"

    raw_jobs = jobs_col.find()
    # print("JOBS length: " + str(len(list(raw_jobs))))

    for job in raw_jobs:
        result_data.append(
            word_crunching_engine.matching_keywords(job, resume))

    recommended_jobs = sorted(result_data, key=lambda k: float(k['score']),
                              reverse=True)

    for idx, job in enumerate(recommended_jobs):
        print("[ " + str(idx) + " ]" + " " + job["jobName"] + ": " + job["score"] + " | " + str(
            job["title_common_nr_words"]) + " | " + str(job[
                                                            "title_common_percentage"]))

    # print(recommended_jobs)

    col.update_one(
        filter={
            "email": request_data["email"],
        },
        update={
            '$set': {
                'email': request_data["email"],
                'jobs': recommended_jobs
                # 'jobs': [json.dumps(job) for job in jobs]
            }
            # '$set': {
            #     'last_update_date': now,
            # },
        },
        upsert=True,
    )

    # print(recommended_jobs)

    # print(resume)
    print("[ENDS] RECOMMENDING")
    return resume


@app.route('/register-job-for-user', methods=['POST'])
def register_recommend_job_for_user():
    request_data = request.get_json()
    email = str(request_data["email"])
    pdf_path = str(request_data["resumePath"])

    python_path = "/Users/silviuh1/PycharmProjects/job-recommendation-engine/venv/bin/python"
    engine_path = "/Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine" \
                  "/server-endpoint-engine.py"
    debug_path = "/Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine" \
                 "/user-cronjobs-logs/cron_logs.txt"
    double_arrow = ">>"
    script_command = f"{python_path} {engine_path} {email} {pdf_path} {double_arrow} {debug_path} 2>&1"

    with CronTab(user='silviuh1') as users_cron:
        new_user_job = users_cron.new(
            command=script_command,
            comment=email)

        new_user_job.minute.every(1)

        for job in users_cron:
            print(job)

    return f"[ {email} ]  JOB CREATED"


if __name__ == '__main__':
    word_crunching_engine = WordCrunchingEngine()
    app.run(host="localhost", port=8000, debug=True)
