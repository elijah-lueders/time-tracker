#!/usr/bin/env python3

import datetime
import os
import json


def main():
    today = datetime.date.today()
    weekday = today.weekday()
    filenames = {}
    for i in range(weekday+1):
        day = today - datetime.timedelta(i)
        filenames[day.strftime("%a").upper()] = f"{day.strftime("%m-%d-%Y")}-log.json"
    filesFormatted=""
    for d in filenames:
        filesFormatted = f"[{d}|{filenames[d][:5]}] " + filesFormatted
    print(filesFormatted)
        
    day = input("Choose a day --> ")[:3].upper()
    if day == "":
        day = today.strftime("%a").upper()
    if day in filenames:
        filename = filenames[day]

    # Check if file exists, create if not
    if not os.path.exists(filename):
        create_log_file(filename)

    while True:
        view_entries(filename)
        choice = input("[1]ADD [2]EDIT [3]DEL [4]REPORT [0]EXIT -->") or "add"

        if choice == "1" or choice.lower() == "add":
            log_new_entry(filename)
        elif choice == "2" or choice.lower() == "edit":
            edit_entry(filename)
        elif choice == "3" or choice.lower() == "del":
            delete_entry(filename)
        elif choice == "4" or choice.lower() == "report":
            generate_report(filename)
            break
        elif choice == "0" or choice.lower() == "exit":
            break
        else:
            print("Invalid choice. Please try again.")


def get_map_of_days():
    days = {}
    date = datetime.date.today()
    delta = 0
    dayofweek = date.strftime("%a").lower()
    while dayofweek != "sun":
        date = date - datetime.timedelta(days=delta)
        dayofweek = date.strftime("%a").lower()
        days[dayofweek] = date.strftime("%m-%d-%Y")
        delta += 1
    return days


def create_log_file(filename):
    data = {
        "filename": filename,
        "categories": ["BREAK", "OTHER", "IPOP"],
        "entries": [],
    }
    with open(filename, "w") as f:
        json.dump(data, f)


def view_entries(filename):
    _ = os.system("cls")

    with open(filename, "r") as f:
        data = json.load(f)
        hl = "===========================================\n"
        print(f"{hl} {data['filename']} \n{hl}")

        for i, entry in enumerate(data["entries"], start=1):
            print(
                f"{str(i).rjust(3)}| {entry['timestamp']} | {entry['category'].ljust(8)} | {entry['description']}"
            )
        print(hl)


def log_new_entry(filename):    
    categories = load_categories(filename)

    timestamp = input("Timestamp --> ")
    category = prompt_for_category(categories, filename)
    description = input("Description --> ")

    if timestamp == "":
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    append_entry(filename, timestamp, category, description)

def load_categories(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        return data["categories"]


def prompt_for_category(categories, filename):
    while True:
        msg = "Categories: "
        for i, category in enumerate(categories):
            msg += f"[{i+1}]{category} "

        choice = input(msg + " --> ")

        if choice.isdigit():
            if 1 <= int(choice) <= len(categories):
                return categories[int(choice) - 1]
            else:
                print(
                    "Not an existing category. Choose again or enter a string for a new category."
                )
        elif choice.upper() in categories:
            return choice.upper()
        else:
            new_category = choice.upper()
            categories.append(new_category)
            with open(filename, "r+") as f:
                data = json.load(f)
                data["categories"].append(new_category)
                f.seek(0)
                json.dump(data, f)
                f.truncate()
            return new_category


def append_entry(filename, timestamp, category, description):
    with open(filename, "r+") as f:
        data = json.load(f)
        data["entries"].append(
            {"timestamp": timestamp, "category": category, "description": description}
        )
        data["entries"].sort(key=lambda x: x["timestamp"])
        f.seek(0)
        json.dump(data, f)
        f.truncate()


def edit_entry(filename):
    view_entries(filename)
    entry_num = int(input("Entry # to edit --> ")) - 1

    with open(filename, "r+") as f:
        data = json.load(f)
        entry = data["entries"][entry_num]
        categories = load_categories(filename)

        fill = '-'
        align = '^'
        width = 20
        timestamp =     input(f"Timestamp   [CUR]{entry['timestamp']:{fill}{align}{width}}> ")
        category =      input(f"Category    [CUR]{entry['category']:{fill}{align}{width}}> ")
        description =   input(f"Description [CUR]{entry['description'][:16]:{fill}{align}{width}}> ")

        if timestamp == "":
            timestamp = entry["timestamp"]
        if category == "":
            category = entry["category"]
        if description == "":
            description = entry["description"]

        data["entries"][entry_num] = {
            "timestamp": timestamp,
            "category": category,
            "description": description,
        }
        f.seek(0)
        json.dump(data, f)
        f.truncate()


def delete_entry(filename):
    view_entries(filename)
    entry_num = int(input("Entry # to delete --> ")) - 1

    with open(filename, "r+") as f:
        data = json.load(f)
        del data["entries"][entry_num]
        f.seek(0)
        json.dump(data, f)
        f.truncate()


def generate_report(filename):
    # open file and read the data
    with open(filename, "r") as f:
        data = json.load(f)
    # create a dictionary to store the time spent on each category
    report = {}
    # iterate over the entries
    for entry in data["entries"]:
        # if the category is not in the report, add it
        if entry["category"] not in report:
            report[entry["category"]] = 0
        # if the entry is not the last one
        if entry != data["entries"][-1]:
            # calculate the time spent between the current entry and the next one
            time_spent = datetime.datetime.strptime(
                data["entries"][data["entries"].index(entry) + 1]["timestamp"],
                "%H:%M:%S",
            ) - datetime.datetime.strptime(entry["timestamp"], "%H:%M:%S")
        elif entry["category"] != "BREAK":
            time_spent = datetime.datetime.now() - datetime.datetime.strptime(entry["timestamp"], "%H:%M:%S")
            # add the time spent to the category
        report[entry["category"]] += time_spent.total_seconds() / 3600
    # print the report
    print("Category Totals:")
    for category, time in report.items():
        print(f"{category}: {round(time, 2)} hours")


if __name__ == "__main__":
    main()
