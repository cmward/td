#!/usr/bin/env python
"""Less elegant, less functional, and all around stupider version of
Steve Losh's t (http://stevelosh.com/projects/t/).

Create independent todo lists for individual directories.
"""
import argparse
import os
import time

def _parse_time():
    """Return the current time, nicely formatted."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def _parse_task_from_file(line):
    """Read task from td.txt file and create the corresponding
    task object.
    """
    time = line[1:20]
    line = line[22:]
    completed = False
    if line.endswith("*done*"):
        completed = True
        line = line[:line.find("*done*")-1]
    if line.find("*un*") != -1:
        # +5 skips over '*un* '
        username = line[line.find("*un*")+5:]
        line = line[:line.find("*un*")]
    else:
        username = None
    text = line
    task = Task(text, time, username, completed)
    return task

class Task(object):
    """Structure representing a single task. Stores the task string,
    the time it was created, the username of its creator (if it has one),
    and a flag indicating whether or not it's completed.
    """
    def __init__(self, text, time, username=None, completed=False):
        """Each task object will have to have all of these parameters
        supplied at time of creation.
        """
        self.text = text
        self.time = time
        self.username = username
        self.completed = completed

    def __str__(self):
        if self.username:
            return "[" + self.time + "]" + " " + self.text + " " + \
                    "(" + self.username + ")"
        else:
            return "[" + self.time + "]" + " " + self.text

class TaskDict(object):
    """Maps ids to tasks. Ids are created for each item in the list
    sequentially.

    Read in from the task text file on init and write out with write().
    Creates td.txt in dir if it doesn't already exist.
    """
    def __init__(self, directory):
        self.tasks = {}
        self.completed_tasks = {}
        self.directory = os.path.abspath(directory)
        self.file = os.path.join(self.directory, "td.txt")
        try:
            with open(self.file, 'r') as task_file:
                i, j = 0, 0
                for line in task_file:
                    clean_line = line.strip()
                    if clean_line != "":
                        task = _parse_task_from_file(clean_line)
                        if task.completed:
                            self.completed_tasks[i] = task
                            i += 1
                        else:
                            self.tasks[j] = task
                            j += 1
        except IOError:
            print "Couldn't find td.txt. Creating it in %s." \
                    % os.path.abspath(directory)
            self.write()

    def _next_id(self, dict_name):
        """Return the next available id."""
        return len(self.__dict__[dict_name])

    def _update_ids(self, delete_n, dict_name):
        """Subtract 1 from all ids greater than n in the specified dict.
        """
        dictionary = self.__dict__[dict_name]
        for key in dictionary.iterkeys():
            if key > delete_n:
                dictionary[key-1] = dictionary.pop(key)

    def add_task(self, text, username=None):
        """Add a task to the task dictionary."""
        new_task = Task(text, _parse_time(), username, completed=False)
        self.tasks[self._next_id('tasks')] = new_task

    def complete_task(self, task_id):
        """ Remove the task specified by the given id from the tasks dict
        and add it to the completed_tasks dict.
        """
        task = self.tasks[task_id]
        text = task.text + " *done*"
        username = task.username
        self.completed_tasks[self._next_id('completed_tasks')] = \
                Task(text, _parse_time(), username, completed=True) 
        del self.tasks[task_id]
        self._update_ids(task_id, 'tasks')

    def edit_task(self, new_task, task_id):
        """Change a task in the dictionary."""
        self.tasks[task_id].text = new_task

    def wipe_completed_history(self):
        """Wipe the completed tasks dictionary. Won't take effect in the
        .txt file until write() is called.
        """
        self.completed_tasks = {}
        print "Completed task history wiped."

    def print_dict(self, dict_name):
        """Print the entire dictionary specified by dict_name."""
        task_dict = self.__dict__[dict_name]
        if len(task_dict) == 0:
            print "No tasks in this list."
        else:
            for task_id, task in task_dict.iteritems():
                print task_id, ">>", task 

    def write(self):
        """Write the tasks and completed tasks out to a .txt file.
        Overwrites the existing file.
        """
        with open(self.file, 'w') as out:
            for task in self.tasks.values():
                out.write(str(task) + '\n')
            out.write('\n')
            for completed in self.completed_tasks.values():
                out.write(str(completed) + " " + "*done*" + '\n')

def _main():
    """Parse arguments and perform the proper actions."""
    parser = argparse.ArgumentParser(prog="td")
    parser.add_argument("--dir", dest="dir",
                        help="Work on tasks in DIR")
    parser.add_argument("-c", "--complete", dest="complete",
                        required=False, help="Mark task as completed")
    parser.add_argument("-e", "--edit", dest="edit",
                        required=False, help="Edit TASK")
    parser.add_argument("-w", "--wipe", dest="wipe",
                        required=False, action="store_true",
                        help="Wipe completed task history")
    parser.add_argument("-f", "--finished", action="store_true",
                        help="Display list of finished tasks.")
    parser.add_argument("-u", "--username", dest="username",
                        required=False)
    parser.add_argument("text", nargs="*", metavar="TASK",
                        help="Add TASK to the list.")
    args = parser.parse_args()

    tasks = TaskDict(args.dir)
    task = ' '.join(args.text)
    if args.complete:
        tasks.complete_task(int(args.complete))
        tasks.write()
    elif args.edit and args.text:
        tasks.edit_task(task, int(args.edit))
        tasks.write()
    elif args.wipe:
        print "Wipe completed task history? (y/n)"
        user_input = raw_input()
        if user_input == "y":
            tasks.wipe_completed_history()
            tasks.write()
        elif input == "n":
            quit()
        else:
            print "Please enter (y) or (n)"
    elif args.text:
        if args.username:
            tasks.add_task(task, username=args.username)
        else:
            tasks.add_task(task)
        tasks.write()
    elif args.finished:
        tasks.print_dict("completed_tasks")
    else:
        tasks.print_dict("tasks")

if __name__ == "__main__":
    _main()
