# Import the APIs
from canvasapi import Canvas
from datetime import datetime
from dateutil import tz
import schedule
import time
from email.message import EmailMessage
import smtplib
import ssl

# app.py is a file that contains all your sensitive information
from app import sender_email, sender_password, canvas_key, api_url, userID, receiver_email

#----------------------------------------------------------
# Initialization

# Canvas API URL
API_URL = api_url
# Canvas API key
API_KEY = canvas_key
# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
# replace userID with your userID
user = canvas.get_user(userID)
#----------------------------------------------------------
# Functions

# Change date_time in canvasapi to something accurate and usable
def reformat_date_time(time):
  from_zone = tz.gettz('UTC')
  to_zone = tz.gettz('America/New_York')
  utc = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')

  # Tell the datetime object that it's in UTC time zone since 
  # datetime objects are 'naive' by default
  utc = utc.replace(tzinfo=from_zone)

  # Convert time zone
  return utc.astimezone(to_zone)

#create a dictionary with only class name and date due
def create_important_dict(upcoming_api_call):
  class_dict = {}
  for each in upcoming_api_call:
    class_dict[each["title"]] = reformat_date_time(each["end_at"])

  return(class_dict)

def send_message(s,t):
  sender = sender_email
  sender_pass = sender_password

  receiver = receiver_email

  em = EmailMessage()
  em['From'] = sender
  em['To'] = receiver
  em['Subject'] = s
  em.set_content(t)

  context = ssl.create_default_context()

  with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(sender, sender_pass)
    smtp.sendmail(sender, receiver, em.as_string())
  
# generate reminder if a task is due that day
def remind_me():
  class_dict = create_important_dict(canvas.get_upcoming_events())
  current_date = datetime.today()
  message_list = []
  for task in class_dict:
    task_date = class_dict.get(task)
    if ((task_date.month,task_date.day) == (current_date.month,current_date.day)):
      hour = task_date.hour % 12
      am_or_pm = "AM"
      if task_date.hour > 12:
        am_or_pm = "PM"
      message_list.append(f"{task} due at {hour}:{task_date.minute} {am_or_pm} Today.")
    if ((task_date.month,task_date.day) == (current_date.month,current_date.day+1)):
      hour = task_date.hour % 12
      am_or_pm = "AM"
      if task_date.hour > 12:
        am_or_pm = "PM"
      message_list.append(f"{task} due at {hour}:{task_date.minute} {am_or_pm} Tomorrow.")
  msg = "Hello,\n\nYou have the following assignments due today and tomorrow:\n\n"
  for each in message_list:
    msg += (each + "\n")
  msg +=  "\nHave a Good Day!\n-Schedule Reminder"
  print(msg)
  send_message(f"Reminders for {current_date.month}/{current_date.day} and {current_date.month}/{current_date.day+1}",msg)

#----------------------------------------------------------
# Main body of code
def main():
  schedule.every().day.at("08:00").do(remind_me)
  while True:
    schedule.run_pending()
    time.sleep(50)

if __name__ == '__main__':
  main()
