from elysian_wishlist import app
from elysian_wishlist.modules.cron.cronFunctionality import *


if __name__ == "__main__":
    #scheduler.add_job(id='Scheduled task', func=scheduledTask, trigger='interval', hours=5)
    #scheduler.start()
    app.run(port=5000, debug=True, use_reloader=False)
