#!/usr/bin/env python
import argparse
import os
import time

"""Less elegant, less functional, and all around stupider version of
Steve Losh's t (http://stevelosh.com/projects/t/).

Create independent todo lists for individual directories. 
"""

def _parse_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

class Tasks(object):
    """ Maps ids to tasks. Ids are created for each item in the list
    sequentially. 
    
    Read in from the task text file on init and write out with write().
    Creates td.txt in dir if it doesn't already exist.
    """
    def __init__(self, dir):
        self.tasks = {}
        self.completed_tasks = {}
        self.dir = os.path.abspath(dir)
        self.file = os.path.join(self.dir, "td.txt")
        try:
            with open(self.file, 'r') as f:
                i, j = 0, 0
                for line in f:
                    clean_line = line.strip()
                    if clean_line != "":
                        if clean_line.endswith("*done*"):
                            self.completed_tasks[j] = (clean_line[:19],
                                                       clean_line[20:])
                            j += 1
                        else:
                            self.tasks[i] = (clean_line[:19],
                                             clean_line[20:])
                            i += 1
        except IOError:
            print "Couldn't find td.txt. Creating it in %s." \
                    % os.path.abspath(dir)
            self.write()

    def _next_id(self, dict_name):
        """ Return the next available id.
        """
        return len(self.__dict__[dict_name])

    def _update_ids(self, n, dict_name):
        """ Subtract 1 from all ids greater than n in the specified dict.
        """
        d = self.__dict__[dict_name]
        for k in d.iterkeys():
            if k > n:
                d[k-1] = d.pop(k)

    def add_task(self, task):
        """ Add a task to the task dictionary.
        """
        self.tasks[self._next_id('tasks')] = (_parse_time(), task)

    def complete_task(self, task_id):
        """ Remove the task specified by the given id from the tasks dict
        and add it to the completed_tasks dict.
        """
        task = self.tasks[task_id][1] + " *done*"
        self.completed_tasks[self._next_id('completed_tasks')] = \
                (_parse_time(), task)
        del self.tasks[task_id]
        self._update_ids(task_id, 'tasks')

    def edit_task(self, new_task, task_id):
        self.tasks[task_id] = (self.tasks[task_id][0], new_task)

    def wipe_completed_history(self):
        """ Wipe the completed tasks dictionary. Won't take effect in the
        .txt file until write() is called.
        """
        self.completed_tasks = {}
        print "Completed task history wiped."

    def print_task(self, id, dict_name):
        if dict_name == "tasks":
            print self.__dict__[dict_name][id][0], ">>", \
                    id, "-", self.__dict__[dict_name][id][1] 
        else:
            print self.__dict__[dict_name][id][0], ">>", \
                    id, "-", self.__dict__[dict_name][id][1][:-6]

    def print_dict(self, dict_name):
        if len(self.__dict__[dict_name]) == 0:
            print "No tasks in this list."
        else:
            map(lambda k: self.print_task(k, dict_name), \
                self.__dict__[dict_name].keys()) 

    def write(self):
        """ Write the tasks and completed tasks out to a .txt file.
        Overwrites the existing file.
        """
        with open(self.file, 'w') as out:
            for task in self.tasks.values():
                out.write(task[0]+' '+task[1]+'\n')
            out.write('\n')
            for ct in self.completed_tasks.values():
                out.write(ct[0]+' '+ct[1]+'\n')

def _main():
    """ Parse arguments and perform the proper actions.
    """
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
    parser.add_argument("text", nargs="*", metavar="TASK",
                        help="Add TASK to the list.")
    args=parser.parse_args()
    
    t = Tasks(args.dir)
    task = ' '.join(args.text)
    if args.complete:
        t.complete_task(int(args.complete))
        t.write()
    elif args.edit and args.text:
        t.edit_task(task, int(args.edit))
        t.write()
    elif args.wipe:
        print "Wipe completed task history? (y/n)"
        input = raw_input()
        if input == "y":
            t.wipe_completed_history()
            t.write()
        elif input == "n":
            quit()
        else:
            print "Please enter (y) or (n)"
    elif args.text:
        t.add_task(task)
        t.write()
    elif args.finished:
        t.print_dict("completed_tasks")
    else:
        t.print_dict("tasks")

if __name__ == "__main__":
    _main()
