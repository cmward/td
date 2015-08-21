#!/usr/bin/env python
"""Less elegant, less functional, and all around stupider version of
Steve Losh's t (http://stevelosh.com/projects/t/).

Create independent todo lists for individual directories.
"""
import argparse, os, time, pickle

def _parse_time():
    """Return the current time, nicely formatted."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

class Task(object):
    """Structure representing a single task. Stores the task string,
    the time it was created, the username of its creator (if it has one),
    and a flag indicating whether or not it's completed.
    """
    def __init__(self, text, timestamp, username=None, completed=False):
        """Each task object will have to have all of these parameters
        supplied at time of creation.
        """
        self.text = text
        self.timestamp = timestamp
        self.username = username
        self.completed = completed

    def __str__(self):
        if self.username:
            return "[" + self.timestamp + "]" + " " + self.text + " " + \
                    "(" + self.username + ")"
        else:
            return "[" + self.timestamp + "]" + " " + self.text

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
        self.file = os.path.join(self.directory, ".td.p")
        try:
            with open(self.file) as pfile:
                td_obj = pickle.load(pfile)
                self.tasks = td_obj.tasks
                self.completed_tasks = td_obj.completed_tasks
        except IOError:
            print "Couldn't find .td.p. One will be created in %s." \
                    % os.path.abspath(directory)

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

def write_dict(task_dict):
    """Write the tasks and completed tasks out to a .txt file.
    Overwrites the existing file.
    """
    with open(task_dict.file, 'w') as pfile:
        pickle.dump(task_dict, pfile)

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
        write_dict(tasks)
    elif args.edit and args.text:
        tasks.edit_task(task, int(args.edit))
        write_dict(tasks)
    elif args.wipe:
        print "Wipe completed task history? (y/n)"
        user_input = raw_input()
        if user_input == "y":
            tasks.wipe_completed_history()
            write_dict(tasks)
        elif input == "n":
            quit()
        else:
            print "Please enter (y) or (n)"
    elif args.text:
        if args.username:
            tasks.add_task(task, username=args.username)
        else:
            tasks.add_task(task)
        write_dict(tasks)
    elif args.finished:
        tasks.print_dict("completed_tasks")
    else:
        tasks.print_dict("tasks")

if __name__ == "__main__":
    _main()
