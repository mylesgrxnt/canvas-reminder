# canvas-reminder
Problem: Canvas sends out daily summaries for assignments and tests, usually only notifying users until after the deadlines have passed for that day.
Solution: Run a Python script that emails your assignments and tests to you every day for the current day and following day using the Canvas API.

SETUP INSTRUCTIONS
1) Use pip3 to install the following packages
   pip3 install canvasapi
   pip3 install datetime
   pip3 install schedule
2) Go to your university Canvas website and go to Account > Settings > Approved Integrations > New Access Token. Fill out the fields however you like (setting expiration date to your date of graduation) and click "Generate Token". Copy this value into app.py as canvas_key.
3) While you are on Canvas, copy the url of your specific institution (for example, "https://bostoncollege.instructure.com/" ) and add it to app.py as api_url.
4) Look through various classes in Canvas until you find a class that has a "People" section. Click on the "People" section and click on yourself. Get your userID in the url: https://university.instructure.com/courses/1234567/users/{userID} and add it to app.py as userID.
5) Now, setup a new gmail account to send emails with (or use an existing account). Add the email address to app.py as sender_email. On Google, go to Account > Security > How you sign in to Google > 2-Step Verification > App Passwords. Generate a new App Password and then copy it into app.py as sender_password.
6) Then, put in a receiver email to receive the notification as receiver_email in app.py.
7) Finally, change the timezone in reformat_date_time() if you live somewhere that is not US Eastern Time
8) From here, simply keep the script running and you will receive notifications every day at 8 AM detailing all your assignments, quizzes, and tests due that day and the next day.
