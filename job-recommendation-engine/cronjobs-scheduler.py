#!/Users/silviuh1/PycharmProjects/job-recommendation-engine/venv/bin/python
from crontab import CronTab

if __name__ == '__main__':
    users_cron = CronTab(user='silviuh1')
    # job = my_cron.new(
    #     command='/Users/silviuh1/PycharmProjects/job-recommendation-engine/venv/bin/python'
    #             ' /Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/server-endpoint-engine.py'
    #             ' emil@gmail.com /Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/job-portal/resumes/emil/CV-Cebotarosh.pdf',
    #     comment='emil@gmail.com')
    #
    # job.minute.every(1)
    # my_cron.write()
    for job in users_cron:
        print(job)
