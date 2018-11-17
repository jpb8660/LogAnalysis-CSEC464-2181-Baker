# Jacob Baker
# Log Search
# Desc: Searches through files in a drive to find logs and
# search through the logs for specific keywords or times

import os
import platform
import sys
import datetime

from pathlib import Path

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

folder_loc = os.getcwd()

# Compiles a list of logs from a specified drive
# and outputs it to a file for later use
def list_of_logs(drive, prnt):
    filepath = folder_loc + "\\log_list_of_" + drive + ".txt"
    log_list = open(filepath, 'w')
    log_list.close()
    log_list = open(filepath, 'a', encoding="utf-8")
    
    x = 0
    for root, dirs, files in os.walk(drive + ":\\"):
        for file in files:
            data = os.path.join(root, file)
            if os.access(data, os.R_OK):
                if file.endswith(".log"):
                    if prnt == "1":
                        print(data)
                    log_list.write(data)
                    log_list.write(" \n")
                    x += 1
                if "log" in file and file.endswith(".txt"):
                    if prnt == "1":
                        print(data)
                    log_list.write(data)
                    log_list.write(" \n")
                    x += 1
    print(str(x) + " log related files found")
    log_list.close()

# Searches through a list of logs to find logs
# that have the keyword in the file or filename
def keyword_search(drive, keyword):
    filepath = folder_loc + "\\log_list_of_" + drive + ".txt"
    file_exists = Path(filepath)
    if file_exists.is_file():
        log_list = open(filepath, 'r')
        for path in log_list:
            path = path.replace(" \n", "")
            file_exists = Path(path)
            if file_exists.is_file():
                file = open(path, 'r', encoding="utf-8")
                for line in file:
                    if keyword in line:
                        print(path)
                        print(line)
    else:
        choice = input("Couldn't find log list for this drive.  Compile new one? (y or n)\n")
        while True:
            if choice == "y":
                list_of_logs(drive, "2")
                keyword_search(drive, keyword)
                break
            elif choice == "n":
                break
            else:
                print("Please choose an option.")

# Searches through a list of logs to fing logs
# that have been modified or created during
# the timeframe
def timeline_search(drive):
    filepath = folder_loc + "\\log_list_of_" + drive + ".txt"
    file_exists = Path(filepath)
    if file_exists.is_file():
        log_list = open(filepath, 'r')
        begin_date = input("When do you want to start the timeline? (YYYY-MM-DD)\n")
        year, month, day = map(int, begin_date.split('-'))
        date1 = datetime.datetime(year, month, day)
        
        end_date = input("When do you want to start the timeline? (YYYY-MM-DD)\n")
        year, month, day = map(int, end_date.split('-'))
        date2 = datetime.datetime(year, month, day)

        filename = folder_loc + "\\timeline_search_between_" + str(begin_date) + "_and_" + str(end_date) + "_of_" + drive + ".txt"
        file = open(filename, 'w')
        
        for path in log_list:
            path = path.replace(" \n", "")
            file_exists = Path(path)
            if file_exists.is_file():
                ctime = os.path.getctime(path)
                mtime = os.path.getmtime(path)
                ctime = datetime.datetime.fromtimestamp(ctime)
                mtime = datetime.datetime.fromtimestamp(mtime)
                if(ctime >= date1 and ctime <= date2):
                    print(path)
                    print("Created: " + str(ctime))
                    print("")
                    file.write(path + "\nCreated: " + str(ctime) + "\n")
                if(mtime >= date1 and mtime <= date2):
                    print(path)
                    print("Modified: " + str(mtime))
                    print("")
                    file.write(path + "\nModified: " + str(mtime) + "\n")
    else:
        choice = input("Couldn't find log list for this drive.  Compile new one? (y or n)\n")
        while True:
            if choice == "y":
                list_of_logs(drive, "2")
                timeline_search(drive)
                break
            elif choice == "n":
                break
            else:
                print("Please choose an option.")

# Reads and prints specified file
def read_file(filepath):
    file_exists = Path(filepath)
    if file_exists.is_file():
        with open(filepath, 'r', encoding="utf-8") as file:
            line = file.readline()
            x = 1
            while line:
                print("{}: {}".format(x, line.strip()))
                line = file.readline()
                x += 1
        file.close()
    else:
        print("File doesn't exist")

# Creates a menu for the user to choose how to
# interact with the logs
def log_menu():
    menu = {}
    menu["1"] = "List Logs"
    menu["2"] = "Keyword Search"
    menu["3"] = "Timeline Search"
    menu["4"] = "Examine Log"
    menu["5"] = "Back"
    while True:
        print("Log Search\n-----------------------------")
        options = menu.keys()
        #options.sort()
        for option in options:
            print(option, menu[option])
        choice = input("What would you like to do:\n")
        if choice == "1":
            drive = input("Which drive do you want to search?\n")
            list_of_logs(drive, "1")
        elif choice == "2":
            drive = input("Which drive do you want to search?\n")
            keyword = input("What do you want to search for?\n")
            keyword_search(drive, keyword)
        elif choice == "3":
            drive = input("Which drive do you want to search?\n")
            timeline_search(drive)
        elif choice == "4":
            filepath = input("Which file do you want to look at? (Filepath)\n")
            read_file(filepath)
        elif choice == "5":
            break
        else:
            print("Please choose an option.")

# Creates a menu for the user to specify what
# tool they want to use
def main_menu():
    menu = {}
    menu["1"] = "Log Search"
    menu["2"] = "Exit"
    while True:
        print("Main Menu\n-----------------------------")
        options = menu.keys()
        #options.sort()
        for option in options:
            print(option, menu[option])
        choice = input("What would you like to do:\n")
        if choice == "1":
            log_menu()
        elif choice == "2":
            break
        else:
            print("Please choose an option.")

def main():
    main_menu()
    
if __name__ == '__main__':
    main()
