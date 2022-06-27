#!/Users/silviuh1/PycharmProjects/job-recommendation-engine/venv/bin/python
from crontab import CronTab

if __name__ == '__main__':
    users_cron = CronTab(user='silviuh1')
    with CronTab(user='silviuh1') as users_cron:
        #     emils_job = users_cron.new(
        #         command="/Users/silviuh1/PycharmProjects/job-recommendation-engine/venv/bin/python /Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/server-endpoint-engine.py emil@gmail.com /Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/job-portal/resumes/emil/CV-Cebotarosh.pdf >> /Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/user-cronjobs-logs/cron_logs.txt 2>&1",
        #         comment='emil@gmail.com')
        #
        #     hrSpecialist_job = users_cron.new(
        #         command="/Users/silviuh1/PycharmProjects/job-recommendation-engine/venv/bin/python /Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/server-endpoint-engine.py hrSpecialist@gmail.com /Users/silviuh1/workspace/dev/facultate/licenta/job-portal/resumes/hrSpecialist/hr_specialist.pdf >> /Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/user-cronjobs-logs/cron_logs_2.txt 2>&1",
        #         comment='hrSpecialist@gmail.com'
        #     )
        #
        # emils_job.minute.every(1)
        # hrSpecialist_job.minute.every(1)
        #
        # for job in users_cron:
        #     print(job)

        users_cron.remove_all()
