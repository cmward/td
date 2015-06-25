Create independent todo lists for individual directories. 

## td
Less elegant, less functional, and all around stupider version of [Steve Losh's t] (http://stevelosh.com/projects/t/).

# Install
Create the following alias in your .bashrc:
`alias td="python path/to/td.py --dir '.'"`
That should be it.

# Usage
`$ td` will list the tasks in the list in your working directory if it finds a td file, and if not, it will create such a file. 
`
-c ID      completes a task, moving it to the completed list

-f         lists completed tasks for the current directory

-e ID TASK edits the task with ID to be TASK

-w         wipes the history of completed tasks in the current directory
`

The lists are stored as `.td.txt`.
