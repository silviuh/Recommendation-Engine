from crontab import CronTab
from flask import request, app


class CronAssigner:

    def __init__(self):
        return

    def register_recommend_job_for_user(self, request_data):
        # request_data = request.get_json()
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

            new_user_job.minute.every(2)

            for job in users_cron:
                print(job)

        return f"[ {email} ]  JOB CREATED"


if __name__ == '__main__':
    cronAssigner = CronAssigner()
    request_data = {
        "email": "andrada@gmail.com",
        "resumePath": "/Users/silviuh1/workspace/dev/facultate/licenta/job-portal/resumes/andrada/DocumentatieLicenta_MunteanuLetitia.pdf"
        # "resumePath": "/Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/resume-extensions-test/CV_ROTARU_GEORGE.docx"
        # "resumePath": "/Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/resume-extensions-test/DocumentatieLicenta_MunteanuLetitia-corectat.pdf"
        # "resumePath": "/Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/resume-extensions-test/python-dev-scientist.txt"
    }
    print(cronAssigner.register_recommend_job_for_user(request_data))
