#!/Users/silviuh1/PycharmProjects/job-recommendation-engine/venv/bin/python
from crontab import CronTab

if __name__ == '__main__':
    users_cron = CronTab(user='silviuh1')
    with CronTab(user='silviuh1') as users_cron:
        users_cron.remove_all()
