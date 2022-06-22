import json

from flask import Flask, request
from textblob import TextBlob
from WordCrunchingEngine import WordCrunchingEngine

app = Flask(__name__)


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
    for json in result['container_data']:
        print(json['jobLocation'] + " " + json['score'])
    return result


if __name__ == '__main__':
    word_crunching_engine = WordCrunchingEngine()
    app.run(host="localhost", port=8000, debug=True)
