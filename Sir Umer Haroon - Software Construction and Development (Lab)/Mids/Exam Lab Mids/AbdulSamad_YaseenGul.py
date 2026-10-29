'''
For this Lab Mid Term Exam I am choosing a mix up of two differnet ideas which is
(Focus Session Manager with Streak Tracker)

Design decisions:
- I used XML to save the sessions because it is easy to read and the task asked for it.
- I used regex to check the app name, date, time and duration before saving them.
- Every function does only one job (validate, load, save, add, view, check) so the code stays clean.
- Streak means how many days in a row (newest first) the total screen time stayed under the daily limit.
  Offline sessions are not counted as screen time.
'''

import re 
import xml.etree.ElementTree as ET
from datetime import datetime, date

import os 
XML_FILE_NAME = os.path.basename("detox_sessions.xml")
DAILY_LIMIT_MINUTES = 120
MINUTES_PER_HOUR = 60
MAX_HOUR = 23
MAX_MINUTE = 59
DATE_FORMAT = "%Y-%m-%d"
OFFLINE_CATEGORY = "Offline"
VALID_CATEGORIES = ("Work", "Social", "Offline")

# regex patterns
APP_NAME_PATTERN = r"^[a-zA-Z0-9\s_-]+$"
TIME_PATTERN = r"^\d{1,2}:\d{2}$"
DURATION_PATTERN = r"^(\d+h)?(\d+m)?$"
DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"

# xml tag names
ROOT_TAG = "detox_log"
SESSION_TAG = "session"
APP_TAG = "app_name"
DURATION_TAG = "duration_min"
CATEGORY_TAG = "category"
TIME_TAG = "time_str"
DATE_TAG = "date_str"


def load_sessions_from_xml(file_name: str) -> list: # the function returns a list
    ''' This function loads all the sessions from the xml file, if the file is missing or corrupt it gives an empty list '''
    # root = ET.Element("detox_log")
    sessions = []
    try:
        tree = ET.parse(file_name)
        root = tree.getroot()
        for element in root.findall(SESSION_TAG):
            try:
                app_name = element.find(APP_TAG).text
                duration_min = int(element.find(DURATION_TAG).text)
                category = element.find(CATEGORY_TAG).text
                time_str = element.find(TIME_TAG).text
                date_str = element.find(DATE_TAG).text
            except (AttributeError, ValueError): # a tag is missing or the duration is not a number
                print("Skipped one broken session in the file.")
                continue
            session = {
                "app_name": app_name,
                "duration_min": duration_min,
                "category": category,
                "time_str": time_str,
                "date_str": date_str
            }
            sessions.append(session)
    except FileNotFoundError:
        return []
    except ET.ParseError:
        print("The file cannot be opened due to parsing errors ")
    
    return sessions



def validate_app_name(app_name: str) -> bool:
    ''' This function validates that whether the app name is valid or not using regex'''
    pattern = APP_NAME_PATTERN # app_name can contain alphanumeric characters and also space, underscore and hyphen# app_name can contain alphanumeric characters and also space, underscore and hyphen
    return bool(re.match(pattern, app_name))

def validate_time(time: str) -> bool:
    ''' This functoin is used to check whether the time stamp in pefect condition o not like in this format (14:30) or not'''
    pattern = TIME_PATTERN
    if not re.match(pattern, time): # we must conver the match object to bool because it does no return something directly
        return False
    hours, minutes = time.split(":") # "14:30" becomes "14" and "30"
    return int(hours) <= MAX_HOUR and int(minutes) <= MAX_MINUTE # this rejects 99:99
    

def validate_date(date_str: str) -> bool:
    ''' This function checks the date like 2026-10-29 using regex and also checks that the date really exists '''
    pattern = DATE_PATTERN
    if not re.match(pattern, date_str):
        return False
    try:
        datetime.strptime(date_str, DATE_FORMAT) # this rejects dates like 2026-13-45
    except ValueError:
        return False
    return True

def validate_duration(duration: str):
    ''' This function checks the duration like 1h30m with regex and gives the total minutes, or None if it is invalid '''
    pattern = DURATION_PATTERN
    if not re.match(pattern, duration):
        return None
    hours = 0
    minutes = 0

    if "h" in duration:
        parts = duration.split("h")
        hours = int(parts[0])
        duration = parts[1]
    if "m" in duration:
        parts = duration.split("m")
        minutes = int(parts[0])
    total = hours * MINUTES_PER_HOUR + minutes

    if total > 0:
        return total 
    else:
        return None


def save_sessions_to_xml(sessions: list, file_name: str):
    ''' This function saves all the sessions into the xml file '''
    root = ET.Element(ROOT_TAG) # find the root element of the whole tree
    for session in sessions:
        item = ET.SubElement(root, SESSION_TAG) 
        ET.SubElement(item, APP_TAG).text = session["app_name"]
        ET.SubElement(item, DURATION_TAG).text = str(session["duration_min"])
        ET.SubElement(item, CATEGORY_TAG).text = session["category"]
        ET.SubElement(item, TIME_TAG).text = session["time_str"]
        ET.SubElement(item, DATE_TAG).text = session["date_str"]
    tree = ET.ElementTree(root)
    ET.indent(tree, space=" ")
    try:
        tree.write(file_name)
    except OSError: # for example no permission to write the file
        print("Error: could not save the file.")



def add_session(sessions: list):
    ''' This function takes all the inputs from the user, checks them and logs a new session '''

    app_name = input("Enter App/Activity Name: ").strip()
    if not validate_app_name(app_name):
        print("Invalid app name.")
        return
    
    date_str = input("Enter Date (YYYY-MM-DD e.g. 2026-10-29): ").strip()
    if not validate_date(date_str):
        print("Invalid date format.")
        return
    
    time_str = input("Enter Time (HH:MM e.g. 14:30): ").strip()
    if not validate_time(time_str):
        print("Invalid time format.")
        return
    
    duration = input("Enter Duration (e.g. 45m, 1h30m, 2h): ").strip()
    duration_min= validate_duration(duration)
    if duration_min is None:
        print("Invalid duration format.")
        return
    
    category = input("Enter Category (Work/Social/Offline): ").strip()
    category = category.capitalize() # social becomes Social
    if category not in VALID_CATEGORIES:
        print("Invalid category.")
        return
    new_session = {
        "app_name": app_name,
        "duration_min": duration_min,
        "category": category,
        "time_str": time_str,
        "date_str": date_str
    }
    sessions.append(new_session)
    save_sessions_to_xml(sessions, XML_FILE_NAME)
    print("Session logged successfully!")



def view_sessions(sessions: list): 
    ''' This function just print the all the sessions '''
    
    if not sessions: # the sessions list is empty 
        print("No sessions recorded yet.")
        return
    
    print("\n\t--- Logged Sessions--- ")
    for index, session in enumerate(sessions): #enumerate is used to just combine things in a tuple like compact them into one 
        print(f"{index + 1}. {session['date_str']} [{session['time_str']}] {session['app_name']} ({session['category']}) - {session['duration_min']} mins")


def minutes_per_day(sessions: list) -> dict:
    ''' This function adds the minutes of every day and returns them like {"2026-10-29": 90}, offline sessions are skipped because they are not screen time '''
    totals = {}
    for session in sessions:
        if session["category"] == OFFLINE_CATEGORY:
            continue
        day = session["date_str"]
        totals[day] = totals.get(day, 0) + session["duration_min"] # get gives 0 if the day is not in the dictionary yet
    return totals

def calculate_streak(sessions: list) -> int:
    ''' This function counts how many days in a row (from the newest day) the total time was under the limit '''
    totals = minutes_per_day(sessions)
    streak = 0
    previous_day = None
    for day_str in sorted(totals, reverse=True): # newest day first
        current_day = datetime.strptime(day_str, DATE_FORMAT).date()
        if totals[day_str] > DAILY_LIMIT_MINUTES:
            break # the limit was broken so the streak stops here
        if previous_day is not None and (previous_day - current_day).days != 1:
            break # a day is missing in between so the streak stops here
        streak += 1
        previous_day = current_day
    return streak


def check_daily_limit(sessions: list):
    ''' This function checks the screen time of today against the limit and shows the streak '''

    if not sessions: # the sessions list is empty 
        print("No sessions recorded yet.")
        return
    
    today_str = date.today().strftime(DATE_FORMAT)
    total_minutes = minutes_per_day(sessions).get(today_str, 0) # only today's sessions are counted

    print(f"\nToday's Screen Time: {total_minutes} mins and Limit: {DAILY_LIMIT_MINUTES} mins")
    if total_minutes <= DAILY_LIMIT_MINUTES:
        remaining = DAILY_LIMIT_MINUTES - total_minutes
        print(f"Goal met! You have {remaining} minutes remaining.") # like we are in the green zone right now 
    else:
        exceeded = total_minutes - DAILY_LIMIT_MINUTES
        print(f"Warning: You exceeded the limit by {exceeded} minutes!")

    print(f"Current Streak: {calculate_streak(sessions)} day(s) under the limit")

def main():
    ''' This is the entry point, it loads the saved sessions and shows the menu again and again '''

    # print("hello")

    sessions = load_sessions_from_xml(XML_FILE_NAME)
    
    try:
        while True:
            print("\t\n *- Focus Session Manager with Streak Tracker *-\t ")
            print("1. Log New Session")
            print("2. View All Sessions")
            print("3. Check Daily Limit & Streak")
            print("4. Exit")
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                add_session(sessions)
            elif choice == "2":
                view_sessions(sessions)
            elif choice == "3":
                check_daily_limit(sessions)
            elif choice == "4":
                print("Exiting Focus Session Manage.")
                break
            else:
                print("Invalid choice, try again.")
    except (KeyboardInterrupt, EOFError): # Ctrl+C or Ctrl+D should not crash the program
        print("\nProgram stopped.")


# by this line we simple tell the python interpreter that if the file is ran as a main program only
#  in this file so let it run else if it is used in other headers or import so not run 
if __name__ == "__main__":
    main()