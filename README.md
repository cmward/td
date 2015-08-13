## td
Less elegant, less functional, and all around stupider version of [Steve Losh's t] (http://stevelosh.com/projects/t/). Create independent todo lists for individual directories.

### Install
Create the following alias in your .bashrc:  
`alias td="python path/to/td.py --dir '.'"`  
That should be it.

### Usage
`td` will list the tasks in the list in your working directory if it finds a td file, and if not, it will create such a file.  
```
-c ID           completes a task, moving it to the completed list  
-f              lists completed tasks for the current directory  
-e ID TASK      edits the task with ID to be TASK  
-u USERNAME     add a username stamp to the task
-w              wipes the history of completed tasks in the current directory
```

Example usage:  
```
$ td Watch 7 seasons of House, M.D.
Couldn't find .td.p. One will be created in /Users/chris/code/td.
$ td
0 >> [2015-08-13 14:33:19] Watch 7 seasons of House, M.D.
$ td Tighten up those graphics on level 3 -u paul
$ td
0 >> [2015-08-13 14:33:19] Watch 7 seasons of House, M.D.
1 >> [2015-08-13 14:34:00] Tighten up those graphics on level 3 (paul)
```

The lists are stored as `.td.p`.
