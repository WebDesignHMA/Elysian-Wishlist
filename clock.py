from apscheduler.schedulers.blocking import BlockingScheduler
from elysian_wishlist.modules.cron.cronFunctionality import *

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=5)
def timed_job():
    print('This job is run every 5 mins.')
    scheduledTask()


sched.start()
