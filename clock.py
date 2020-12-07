from apscheduler.schedulers.blocking import BlockingScheduler
from elysian_wishlist.modules.cron.cronFunctionality import *

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=12)
def timed_job():
    print('This job is run every 12 hours.')
    scheduledTask()


sched.start()
