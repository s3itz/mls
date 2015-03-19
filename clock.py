from apscheduler.schedulers.blocking import BlockingScheduler
from manage import scrape_schedule, scrape_standings

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', hour=0)
def scrape_schedule_job():
    """Every night we want to get the latest schedule. Sometimes games change
    as the season progresses and get rescheduled.
    """
    scrape_schedule(verbose=True)

@scheduler.scheduled_job('cron', hour=0, minute=30)
def scrape_standings_job():
    """Standings will change every evening. The server doesn't usually update
    it until after midnight; so to avoid missing it, we'll schedule our scrape
    a little later.
    """
    scrape_standings()

if __name__ == '__main__':
    scheduler.start()