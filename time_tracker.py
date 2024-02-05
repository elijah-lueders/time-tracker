#!/usr/bin/env python3

import datetime
import json


def main():
    today = datetime.date.today().strftime("%m-%d-%Y")
    filename = f"{today}-log.json"
    # filename = input("Enter the filename: ")

    while True:
        view_entries(filename)
        choice = input("[1]ADD [2]EDIT [3]DEL [4]REPORT [0]EXIT -->")

        if choice == "1":
            add_entry(filename)
        elif choice == "2":
            edit_entry(filename)
        elif choice == "3":
            delete_entry(filename)
        elif choice == "4":
            generate_report(filename)
            break
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def view_entries(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        for i, entry in enumerate(data["entries"], start=1):
            print(
                f"{str(i).rjust(3)}| {entry['timestamp']} | {entry['category'].ljust(8)} | {entry['description']}"
            )


def add_entry(filename):
    timestamp = input("Enter timestamp: ")
    category = input("Enter category: ")
    description = input("Enter description: ")

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
    entry_num = int(input("Enter the number of the entry to edit: ")) - 1

    with open(filename, "r+") as f:
        data = json.load(f)
        entry = data["entries"][entry_num]

        print("Hit enter to keep the current value.")
        timestamp = input(f"Enter new timestamp (current: {entry['timestamp']}): ")
        category = input(f"Enter new category (current: {entry['category']}): ")
        description = input(
            f"Enter new description (current: {entry['description']}): "
        )

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
    entry_num = int(input("Enter the number of the entry to delete: ")) - 1

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
            # add the time spent to the category
            report[entry["category"]] += time_spent.total_seconds() / 3600
        else:
            break
    # print the report
    print("Time spent on each category:")
    for category, time in report.items():
        print(f"{category}: {round(time, 2)} hours")


if __name__ == "__main__":
    main()
