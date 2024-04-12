#!/usr/bin/env python3

import datetime
import os
import json


def main():
    today = datetime.date.today().strftime("%m-%d-%Y")
    filename = f"{today}-log.json"

    # Check if file exists, create if not
    if not os.path.exists(filename):
        create_log_file(filename)

    with open(filename, "r") as f:
        data = json.load(f)
        hl = "===========================================\n"
        print(hl, data["filename"])
        for entry in data["entries"]:
            print(
                f"{entry['timestamp']} | {entry['category'].ljust(9,'-')}> {entry['description']}"
            )
        print(hl)
    # Load existing categories
    categories = load_categories(filename)

    # Prompt user for category selection or addition
    category = prompt_for_category(categories, filename)

    # Prompt user for description
    description = input("Enter a description: ")

    # Create timestamp
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    # Add log entry to file
    append_log_entry(filename, timestamp, category, description)

    print("Log entry added successfully!")


def create_log_file(filename):
    data = {
        "filename": filename,
        "categories": ["BREAK", "OTHER", "IPOP"],
        "entries": [],
    }
    with open(filename, "w") as f:
        json.dump(data, f)


def load_categories(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        return data["categories"]


def prompt_for_category(categories, filename):
    while True:
        msg = "Categories: "
        for i, category in enumerate(categories):
            msg += f"[{i+1}]{category} "

        choice = input(msg + " -->")

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

        # if choice.isdigit() and 0 <= int(choice) <= len(categories):
        #     if int(choice) == 0:
        #         new_category = input("Enter new category: ")
        #         categories.append(new_category)
        #         with open(filename, "r+") as f:
        #             data = json.load(f)
        #             data["categories"].append(new_category)
        #             f.seek(0)
        #             json.dump(data, f)
        #             f.truncate()
        #         return new_category
        #     else:
        #         return categories[int(choice) - 1]
        # else:
        #     print("Invalid choice. Please try again.")


def append_log_entry(filename, timestamp, category, description):
    with open(filename, "r+") as f:
        data = json.load(f)
        data["entries"].append(
            {"timestamp": timestamp, "category": category, "description": description}
        )
        f.seek(0)
        json.dump(data, f)
        f.truncate()


if __name__ == "__main__":
    main()
