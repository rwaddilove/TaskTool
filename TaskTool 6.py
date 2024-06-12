# TaskTool - a To-Do / Task manager
# By Roland Waddilove as a Python learning exercise
# Saves settings to your home folder
# Saves tasks as TaskTool.csv
# You can choose where to save the data file. If you save it in a synced folder,
# you can use TaskTool across computers. Eg. I use Mega online drive and sync a
# folder across Mac and PC. TaskTool therefore appears on both computers.
# It's not perfect, it's a learning exercise for me.

import os
import csv
import datetime


def select_folder() -> str:
    """Allow user to browse the disk and select a folder. Most system folders are hidden."""
    print("---------------------------------")
    print("Select folder to use for TaskTool")
    print("---------------------------------")
    os.chdir(os.path.expanduser('~'))       # user's home folder
    print("Current folder: ", os.getcwd())
    inp = ''
    while inp != 'Y' and inp != 'N':
        inp = input("Use this (Y)es (N)o? ").upper()
    if inp == 'Y': return os.getcwd()

    # select folder to store task data
    while inp != 'U':
        dirs = []
        i = 0
        print("\nCurrent Folder: ", os.getcwd())
        for item in os.listdir():
            if os.path.isdir(item) and not item.startswith('.'):
                dirs.append(item)
                print(i, item)
                i += 1
        inp = input(f"Enter num, (B)ack, (U)se this: ").upper()
        if inp.isdigit():
            i = int(inp)
            if i < len(dirs): os.chdir(dirs[i])
        if inp == 'B' and os.getcwd() != os.path.expanduser('~'): os.chdir('..')
    return os.getcwd()


def read_settings(settings) -> None:   # 0=settings-filename, 1=data-filename, 3=path
    os.chdir(os.path.expanduser('~'))      # go to home folder
    if os.path.isfile(settings[0]):            # does settings file exist?
        with open(settings[0], 'r') as f:
            settings.clear()
            for line in f.readlines():
                settings.append(line.strip())          # read settings
        return
    # create settings file
    settings[2] = select_folder()                 # get path to tasks
    write_settings(settings)


def write_settings(settings) -> None:               # don't really need a csv file
    os.chdir(os.path.expanduser('~'))     # save to home folder
    with open(settings[0], 'w') as f:
        f.write(settings[0] + '\n')                 # write settings
        f.write(settings[1] + '\n')
        f.write(settings[2])


def read_tasks(tasks, settings) -> None:
    tasks.clear()
    os.chdir(settings[2])                 # change to our folder
    if not os.path.isfile(settings[1]):   # does tasks file exist?
        tasks.clear()
        tasks.append(['Title', 'Due', 'Repeat', 'Label', 'Done', 'Notes'])
        return

    with open(settings[1], 'r') as f:          # read tasks
        csvreader = csv.reader(f)
        for line in csvreader:                         # read tasks (1st line = field names)
            if line != []: tasks.append(line)          # avoid blank lines


def write_tasks(tasks, settings) -> None:
    os.chdir(settings[2])                       # change to our folder
    with open(settings[1], 'w') as f:      # should check for errors here
        csvwriter = csv.writer(f)
        csvwriter.writerows(tasks)              # 1st line = field names


def show_tasks(tasks) -> None:   # tasks[0] = title, due, repeat, label, done, notes
    print("----------------------------")
    print("   Your tasks")
    print("----------------------------")
    print(f"   {tasks[0][0]}                          {tasks[0][1]}         {tasks[0][4]}  {tasks[0][3]}")
    if len(tasks) == 1: return
    for i in range(1, len(tasks)):
        print(f"{i}".ljust(3), end='')
        print(f"{tasks[i][0][:30]}".ljust(31), end='')
        print(f"{tasks[i][1]}".rjust(10), end='')
        print(f"{tasks[i][4]}".center(8), end='')
        print(f"{tasks[i][3]}")
    print()


def wrap(string, width):
    s=''
    for i in range(0,len(string), width):
        s = s + string[i:i + width]
        s = s + '\n'
    return s


def task_menu(tasks) -> str:
    inp = input("(A)dd, (D)one, (T)rash, (V)iew, (E)dit, (S)ort (Q)uit: ").upper()
    if inp == 'Q': return 'Q'           # quit!
    if inp == 'A':
        add_task(tasks)
        return ' '
    if inp == 'S':
        s = input("Sort by 1.Title, 2.Due, 3.Label, 4.Done: ").upper()
        if s == '1': sort_tasks(tasks, 0)
        if s == '2': sort_tasks(tasks, 1)
        if s == '3': sort_tasks(tasks, 3)
        if s == '4': sort_tasks(tasks, 4)
        return inp

    i = input("Task: ").strip()
    if not i.isdigit(): return ' '      # return nothing if no task selected
    i = int(i)
    if i < 1 or i >= len(tasks): return ' ' # return nothing if no task selected

    if inp == 'V': show_task_details(tasks,i)
    if inp == 'D': done_task(tasks, i)
    if inp == 'T': trash_task(tasks, i)
    if inp == 'E': edit_task(tasks, i)
    return inp


def edit_task(tasks, i):    # tasks[] = title, due, repeat, label, done, notes
    if i < 1 or i >= len(tasks): return
    print("--------------------")
    print("   Edit Task")
    print("--------------------")
#    show_task_details(tasks, i)
    print(f"0. Title: {tasks[i][0]}")
    print(f"1. Due: {tasks[i][1]}")
    print(f"2. Repeat: {tasks[i][2]}")
    print(f"3. Label: {tasks[i][3]}")
    print(f"4. Done: {tasks[i][4]}")
    print(f"5. Notes: {tasks[i][5]}")
    n = input("Edit which one (0-5): ").strip()
    if n not in '012345': return        # abort if no or bad input

    if n == '0': tasks[i][0] = input("Title: ")[:50]    # limit length
    if n == '1': tasks[i][1] = enter_date()
    if n == '2': tasks[i][2] = enter_repeat()
    if n == '3': tasks[i][3] = input("Label: ")[:10]    # limit length
    if n == '5': tasks[i][5] = input("Notes: ")[:250]   # limit length


def add_task(tasks) -> None:             # tasks[] = title, due, repeat, label, done, notes
    print("\n------------------------------")
    print("     Add task")
    print("------------------------------")
    i = len(tasks)
    tasks.append(['','', '', '', '', ''])   # add a row, then set details
    tasks[i][0] = input("Title: ")[:50]     # limit length
    tasks[i][1] = enter_date()
    tasks[i][2] = enter_repeat()
    tasks[i][3] = input("Label: ")[:10]     # limit length
    tasks[i][5] = input("Notes: ")[:500]    # etc.


def enter_repeat() -> str:
    repeat = input("Repeat (D)aily, (W)eekly, (M)onthly, (Y)early: ").upper()
    if repeat not in 'DWMY':
        repeat = ''
    return repeat


def notifications(tasks):
    if len(tasks) < 2: return   # header + task needer
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    cr = 0
    for i in range(1, len(tasks)):
        if tasks[i][1] and tasks[i][1] < today:
            cr = 1
            print(f"Task overdue: {tasks[i][0][:40]}")
    if cr: print()      # add blank line if any notifications printed


def enter_date() -> str:        # used in add_task() and edit_task()
    due = input(f"Date (eg. 2025-09-26): ").strip()
    try:
        d = datetime.datetime.strptime(due, "%Y-%m-%d")
        due = datetime.datetime.strftime(d, '%Y-%m-%d')
    except ValueError:
        due = ''
        print('Date not set.')      # has to be like this: 2025-09-26
    return due


def show_task_details(tasks, i):
    print("\n--------------------")
    print("     Task Details")
    print("--------------------")
    print(f"Title: {tasks[i][0]}")
    print(f"Due: {tasks[i][1]}")
    print(f"Repeat: {tasks[i][2]}")
    print(f"Label: {tasks[i][3]}")
    print(f"Done: {tasks[i][4]}")
#    print(f"Notes: {tasks[i][5]}")
    print("Notes: ", wrap(tasks[i][5], 50))
    input("Continue...")


def done_task(tasks, i) -> None:      # tasks[] = title, due, repeat, label, done, notes
    if tasks[i][4] == 'Y':    # if done...
        tasks[i][4] = ''      # reset and return
        return
    tasks[i][4] = 'Y'         # set done
    if tasks[i][1] == '' or tasks[i][2] == '': return    # no due or no repeat

    # set next repeat due date. (Repeat on 29th Feb isn't handled!)
    if tasks[i][2] == 'M': tasks[i][1] = add_months(tasks[i][1], 1)
    due = datetime.datetime.strptime(tasks[i][1], "%Y-%m-%d")
    if tasks[i][2] == 'D': due += datetime.timedelta(days=1)
    if tasks[i][2] == 'W': due += datetime.timedelta(days=7)
    if tasks[i][2] == 'Y': tasks[i][1] = add_months(tasks[i][1], 12)
    tasks[i][1] = datetime.date.strftime(due, "%Y-%m-%d")
    tasks[i][4] = ''         # task has new date, set not done
    input(f"Task {i} repeats. Next due {tasks[i][1]}...")


def add_months(d, m) -> str:        # no option to add months in datetime, so DIY
    d = d.split('-')        # [yyyy, mm, dd]
    year = int(d[0])
    month = int(d[1]) + m  # add month
    if m > 12:
        year += 1
        month -= 12
    return str(year) + '-' + str(month) + '-' + d[2]


def trash_task(tasks, i) -> None:
    inp = input(f"Delete task '{tasks[i][0]}'.\n(Y)es, (N)o: ").upper()
    if inp == 'Y':
        tasks.pop(i)


def sort_tasks(a, col) -> None:     #sort a list of lists by a column
    # could have used tasks.sort(key=lambda x:x[0]) if headers weren't in first row
    if len(a) < 3: return       # need at least header + 2 rows to sort
    swap = True
    while swap:
        swap = False
        for i in range(2, len(a)):              # skip header row
            if a[i-1][col] > a[i][col]:
                a[i-1], a[i] = a[i], a[i-1]
                swap = True


# =============== M A I N ================
# os.system('cls') if os.name == 'nt' else os.system('clear')

settings = ['TaskTool.txt', 'TaskTool.csv', '']     # 0=settings, datafile, datafile path
tasks = []

read_settings(settings)     # read settings - get folder with tasks
read_tasks(tasks, settings)
sort_tasks(tasks, 1)    # sort by due date

action = ''
while action != 'Q':
    print()
    show_tasks(tasks)
    notifications(tasks)
    action = task_menu(tasks)
    write_tasks(tasks, settings)
