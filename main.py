import uvicorn
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from crawl.run import insta_crawl_job

app = FastAPI()


@app.on_event('startup')
def init_data():
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')
    scheduler.add_job(insta_crawl_job, 'cron', minute='*/20')
    scheduler.start()
    # insta_crawl_job()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)