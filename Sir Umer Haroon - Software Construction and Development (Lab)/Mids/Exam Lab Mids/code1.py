# Name: Awais Qarni
import re
import xml.etree.ElementTree as ET

FILE_NAME = "detox_sessions.xml"
DAILY_LIMIT_MINUTES = 120

def validate_app_name(name):
    pattern = r"^[a-zA-Z0-9\s_-]+$"
    return bool(re.match(pattern, name))

def validate_time(time_str):
    pattern = r"^\d{1,2}:\d{2}$"
    return bool(re.match(pattern, time_str))

def validate_duration(duration_str):
    pattern = r"^(\d+h)?(\d+m)?$"
    if not re.match(pattern, duration_str):
        return None
    hours = 0
    minutes = 0
    if "h" in duration_str:
        parts = duration_str.split("h")
        hours = int(parts[0])
        duration_str = parts[1]
    if "m" in duration_str:
        parts = duration_str.split("m")
        minutes = int(parts[0])
    total = hours * 60 + minutes
    return total if total > 0 else None

def save_sessions_to_xml(sessions, filename):
    root = ET.Element("detox_log")
    for session in sessions:
        item = ET.SubElement(root, "session")
        ET.SubElement(item, "app_name").text = session["app_name"]
        ET.SubElement(item, "duration_min").text = str(session["duration_min"])
        ET.SubElement(item, "category").text = session["category"]
        ET.SubElement(item, "time_str").text = session["time_str"]
    tree = ET.ElementTree(root)
    ET.indent(tree, space=" ")
    tree.write(filename, encoding="utf-8", xml_declaration=True)

def load_sessions_from_xml(filename):
    sessions = []
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        for elem in root.findall("session"):
            app_name = elem.find("app_name").text
            duration_min = int(elem.find("duration_min").text)
            category = elem.find("category").text
            time_str = elem.find("time_str").text
            session = {
                "app_name": app_name,
                "duration_min": duration_min,
                "category": category,
                "time_str": time_str
            }
            sessions.append(session)
    except FileNotFoundError:
        return []
    except Exception:
        return []
    return sessions

def add_session(sessions):
    app_name = input("Enter App/Activity Name: ").strip()
    if not validate_app_name(app_name):
        print("Invalid app name.")
        return
    time_str = input("Enter Time (HH:MM e.g. 14:30): ").strip()
    if not validate_time(time_str):
        print("Invalid time format.")
        return
    duration_str = input("Enter Duration (e.g. 45m, 1h30m, 2h): ").strip()
    duration_min = validate_duration(duration_str)
    if duration_min is None:
        print("Invalid duration format.")
        return
    category = input("Enter Category (Work/Social/Offline): ").strip()
    new_session = {
        "app_name": app_name,
        "duration_min": duration_min,
        "category": category,
        "time_str": time_str
    }
    sessions.append(new_session)
    save_sessions_to_xml(sessions, FILE_NAME)
    print("Session logged successfully!")

def view_sessions(sessions):
    if not sessions:
        print("No sessions recorded yet.")
        return
    print("\n--- Logged Sessions ---")
    for index, s in enumerate(sessions, start=1):
        print(f"{index}. [{s['time_str']}] {s['app_name']} ({s['category']}) - {s['duration_min']} mins")

def check_daily_limit(sessions):
    total_minutes = sum(s["duration_min"] for s in sessions)
    print(f"\nTotal Screen Time: {total_minutes} mins / Limit: {DAILY_LIMIT_MINUTES} mins")
    if total_minutes <= DAILY_LIMIT_MINUTES:
        remaining = DAILY_LIMIT_MINUTES - total_minutes
        print(f"Goal met! You have {remaining} minutes remaining.")
    else:
        exceeded = total_minutes - DAILY_LIMIT_MINUTES
        print(f"Warning: You exceeded the limit by {exceeded} minutes!")

def main():
    sessions = load_sessions_from_xml(FILE_NAME)
    while True:
        print("\n=== Focus Session Manager (Digital Detox) ===")
        print("1. Log New Session")
        print("2. View All Sessions")
        print("3. Check Daily Limit & Streak")
        print("4. Exit")
        choice = input("Enter choice (1-4): ").strip()
        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            check_daily_limit(sessions)
        elif choice == "4":
            print("Exiting Focus Session Manager. Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
