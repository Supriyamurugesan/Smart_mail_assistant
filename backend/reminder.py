from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379/0")

@app.task
def send_reminder(email_id):
    print(f"Reminder: Follow up on email {email_id}")


send_reminder.apply_async(args=["email123"], countdown=7200)
