###Software

System version:	macOS 12.5.1 (21G83)  
Python version: 3.10

##Install Python

To launch the script you have **Python of version 3.10 or higher**.
Check current version of python on your computer by running the command in terminal:
```commandline
python3 --version
```
You can download the latest version of Python from official site: [Link to download](https://www.python.org/downloads/)

## Downloading files

To download script and required for installation files run the commands:

```commandline
 git clone https://github.com/vladissta/Virtual_environment_research
 cd Virtual_environment_research
```

##Virtual environment
After installation it would be better to create new virtual environment, where you will work with script.  

### Problem with autoactivation of conda virtual environment
Initially, we recommend to check if you work in some virtual environment by default 
(sometimes when you launch a terminal, it _automatically activates_ virtual environment).  
It often happens if you earlier worked with such package manager as **conda**.

When you launch the terminal this situation often looks like this:
>(base) Name_of_machine:~ username$

The word _base_ in brackets means you work in virtual environment named _base_   

To turn off automatic activation of virtual environment in conda you can open terminal and run the following command
```commandline
conda config --set auto_activate_base false
```
Then you can relaunch terminal or run the following command to deactivate conda virtual environment :
```commandline
conda deactivate
```

### Creating new virtual environment
You can create virtual environment right in the directory with script or in another directory.    
To create virtual environment named _venv_ in current directory (with script)   
using the _venv_ module in Python run in the terminal:
```commandline
python -m venv venv
```
You can specify the path to and name of virtual environment:
```commandline
python -m venv path/name_of_venv
```
After that you should activate virtual environment.
If it in current directory:
```commandline
source venv/bin/activate 
```
If it in specified directory:
```commandline
source path/name_of_venv/bin/activate  
```
## Installing packages

Script works with several packages, that should be installed in yor virtual environment.  
File **requirements.txt** contains list of required versions of packages needed to script work correctly.  
To install this packages run:
```commandline
pip install --ignore-requires-python -r requirements.txt 
```

##Launching the script

Finally, script can be launched from current directory by command in terminal:
```commandline
python pain.py
```
To deactivate virtual environment after finishing work with script:
```commandline
deactivate
```
