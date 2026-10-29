Focus Session Manager with Streak Tracker

This is ou Software Development Construction Lab Exam (Mids) task where we have to develop a software/system A system that helps people reduce unhealthy screen time and regain focus and
balance in daily life. It tracks usage habits, sets limits, and encourages offline activities. The goal
is mindful technology use, not complete disconnection.

(This line has been taken from the task itself)

Now for this what i developed is that my progam will first of all display a menu

1. Log New Session
2. View All Sessions
3. Check Daily Limit & Streak
4. Exit

If the user chooses 1 the program asks for the app name, time, duration and category and checks them with regex, then the session is saved in an XML file.
If the user chooses 2 it shows all the sessions which are saved.
If the user chooses 3 it compares the total screen time with the daily limit (120 minutes) and tells whether the goal is met or exceeded.
If the user chooses 4 the program ends.

The sessions are stored in detox_sessions.xml so they are loaded again when the program starts next time.
