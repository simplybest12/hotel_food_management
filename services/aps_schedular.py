from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from services.functions import delete_expired_otps

app = FastAPI()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_expired_otps, 'cron', hour=12)  # Run at 12 PM every day
    scheduler.start()

