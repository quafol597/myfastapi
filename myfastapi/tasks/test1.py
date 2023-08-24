from .celery import app


@app.task
def hello():
    return "hello world"
