# Bash utilities written on python


## Contents

### install.py 
Script to install all scripts from **scripts directory** into your environment

It will allow you to execute scripts without specifying path:
```commandline
wc.py -l file.txt
```
To do that run the **install.py** in current direction and follow the instructions:
```commandline
cd terminal_utilities
./install.py 
```

### scripts 
Directory contains all scripts:
- **ls.py** [_directory_]   
Displays list of contents of _directory_. If _directory_ is not specified, displays contents of current directory
```commandline
ls.py
ls.py path/to/dir/
```
- **rm.py** [_-r_] _path_  
Removes files or directories specified in _path_  
**[!]** To remove directories _-r_ flag should be specified. It will remove directories recursively
```commandline
rm.py file1 file2
rm.py -r directory1 directory2
```
- **sort.py** _file_  
Sorts lines of text from _stdin_ or from files specified in _file_ alphabetically
```commandline
sort.py textfile1 textfile2
cat textfile | sort.py
```
- **wc.py** [_-l_][_-w_][_-c_]  _file_  
Counts lines (_-l_), words (_-w_) and characters (_-c_) of _file_ or _stdin_ if certain flag is specified  
If no flags are specified, counts all statistics
If several files were specified in _file_ displays statistics of each file and total sum of them 
```commandline
wc.py -l -w -c file1 file2
wc.py file1 file2
cat file | wc.py 
```

### screenshots_of_comparisons  
Directory contains screenshots where displayed work of bash utilities and their python analogs

### files_for_testing  
Files which  were used for testing (they were displayed on screenshots)
