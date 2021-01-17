from reminderquipo.models import User, Post
from reminderquipo.email import send_email
from datetime import datetime
import time

def scheduler():
    while True:
        now = datetime.now()
        for post in Post.query.all():
            print(post.date_submission)
            difference = int((post.date_submission - now).seconds/60)
            if difference == 0:
                subject = f"Your {post.title} assignment is overdue"
                body = f"Greetings {post.author.username},\nYou have an assignment due on {post.date_submission} for {post.title}.\nDetails:\n{post.content}"
                send_email(post.author.email,
                        subject=subject,
                        body=body)
                post.state = "overdue"
            elif difference == 30:
                subject = f"Less than half an hour remaining for {post.title} assignment"
                body = f"Greetings {post.author.username},\nYou have an assignment due on {post.date_submission} for {post.title}.\nDetails:\n{post.content}"
                send_email(post.author.email,
                        subject=subject,
                        body=body)
                print("less than half hour")
            elif difference == 60:
                subject = f"About an hour remaining for {post.title} assignment"
                body = f"Greetings {post.author.username},\nYou have an assignment due on {post.date_submission} for {post.title}.\nDetails:\n{post.content}"
                send_email(post.author.email,
                        subject=subject,
                        body=body)
                print("hour")
            elif difference == 120:
                subject = f"About two hours remaining for {post.title} assignment"
                body = f"Greetings {post.author.username},\nYou have an assignment due on {post.date_submission} for {post.title}.\nDetails:\n{post.content}"
                send_email(post.author.email,
                        subject=subject,
                        body=body)
                print("two hours")
            elif difference == 300:
                subject = f"About three hours remaining for {post.title} assignment"
                body = f"Greetings {post.author.username},\nYou have an assignment due on {post.date_submission} for {post.title}.\nDetails:\n{post.content}"
                send_email(post.author.email,
                        subject=subject,
                        body=body)
                print("five hour")
            elif difference == 720:
                subject = f"Half a day remaining for {post.title} assignment"
                body = f"Greetings {post.author.username},\nYou have an assignment due on {post.date_submission} for {post.title}.\nDetails:\n{post.content}"
                send_email(post.author.email,
                        subject=subject,
                        body=body)
                print("half day")
            elif difference == 1440:
                subject = f"Assignment due in one day for {post.title} assignment"
                body = f"Greetings {post.author.username},\nYou have an assignment due on {post.date_submission} for {post.title}.\nDetails:\n{post.content}"
                send_email(post.author.email,
                        subject=subject,
                        body=body)
                print("day")
            elif difference == 2160:
                print("one and half day")
            elif difference == 2880:
                print("two day")
            else:
                pass

        time.sleep(60) #because we are comparing in minutes

for user in User.query.all():
    print(user)
