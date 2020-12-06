from apscheduler.schedulers.blocking import BlockingScheduler
from elysian_wishlist.modules.cron.cronFunctionality import *

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=5)
def timed_job():
    print('This job is run every five minutes.')
    scheduledTask()


sched.start()
