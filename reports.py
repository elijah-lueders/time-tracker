#!/usr/bin/env python3

import datetime
import json
import os

def calculate_filename_for_day(day):
    """Generate the filename for the log file based on the given day."""
    return day.strftime("%m-%d-%Y") + "-log.json"

def log_file_exists(filename):
    """Check if a log file exists for the given filename."""
    return os.path.exists(filename)

def generate_report_from_file(filename):
    """Generate and print a report from the log file."""
    with open(filename, "r") as f:
        data = json.load(f)
    
    print(f"Report for {filename[:-8]}")
    report = {}
    total_seconds = {}
    for i, entry in enumerate(data["entries"]):
        category = entry["category"]
        start_time = datetime.datetime.strptime(entry["timestamp"], "%H:%M:%S")
        if i + 1 < len(data["entries"]):
            end_time = datetime.datetime.strptime(data["entries"][i + 1]["timestamp"], "%H:%M:%S")
        else:
            if datetime.datetime.now().strftime("%m-%d-%Y") == filename[:-9]:  # Today's file
                end_time = datetime.datetime.now()
            else:  # Not today's file, assume end of the day
                end_time = datetime.datetime.combine(start_time.date(), datetime.time(23, 59, 59))
        
        duration = (end_time - start_time).total_seconds()
        
        if category not in report:
            report[category] = 1
            total_seconds[category] = duration
        else:
            report[category] += 1
            total_seconds[category] += duration
    
    for category, count in report.items():
        hours = int(total_seconds[category] // 3600)
        minutes = int((total_seconds[category] % 3600) // 60)
        print(f"{category}: {count} entries, Total Time: {hours}h {minutes}m")
    print("")

def main():
    days_back = int(input("How many days of reports do you want (including today)? "))

    for i in range(days_back):
        day = datetime.date.today() - datetime.timedelta(days=i)
        filename = calculate_filename_for_day(day)
        
        if log_file_exists(filename):
            generate_report_from_file(filename)
        else:
            print(f"No log file for {day.strftime('%m-%d-%Y')}. No time logged for this day.")

if __name__ == "__main__":
    main()
