from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    @register_job(scheduler, IntervalTrigger(seconds=60), name="run_bot", replace_existing=True)
    def task():
        call_command('run_bot')
    
    register_events(scheduler)
    scheduler.start()
    logger.info("Scheduler started")
