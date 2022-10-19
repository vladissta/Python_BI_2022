# Pain launching guide on macOS

This guide will help you to install and launch script `pain.py`

**All commands below should be run in Terminal**  
To open Terminal on macOS you can follow one of instructions below:
 - Open Launchpad from your Dock with the keyboard shortcut F4, or tap the six-square-icon button on the Touch Bar.  
Find the **Utilities** folder and click it. Choose Terminal.  
 - In the Finder: open the **Applications** folder  
Usually you can find the icon of the folder on the left in the Finder window.  
Find in **Applications** folder **Utilities** and open it. Then click on Terminal there.

## Recommended software

System version:    ≤ 10.8 macOS  
Python version: ≤ 3.10

## Install Python

To launch the script you should have **Python of version 3.10 or higher**.
Check current version of python on your computer by running the command:

```commandline
python --version
```

This message means python is not installed:
> python --version: command not found

You can download the latest version of Python from official site: [Link to download](https://www.python.org/downloads/)

## Downloading files

To download script and required for installation files run the commands:

```commandline
 git clone https://github.com/vladissta/Virtual_environment_research
 cd Virtual_environment_research
```

## Virtual environment

**After downloading, it would be better to create new virtual environment, where you will work with script.**

### Problem with auto-activation of conda virtual environment

Initially, we recommend to check if you work in some virtual environment by default
Sometimes when you launch a Terminal, it _automatically activates_ virtual environment  
It often happens if you earlier worked with such package manager as **conda**.

When you launch the Terminal this situation often looks like this:
> (base) Name_of_machine:~ username$

The word `base` in brackets means you work in virtual environment named _base_

To turn off automatic activation of virtual environment in conda you can run the following command

```commandline
conda config --set auto_activate_base false
```

Then you can relaunch Terminal or run the following command to deactivate conda virtual environment:

```commandline
conda deactivate
```

### Creating new virtual environment

You can create virtual environment right in the directory with script or in another directory.    
To create virtual environment named _venv_ in current directory (with script)   
using the _venv_ module in Python run:

```commandline
python -m venv venv
```

After that you should activate virtual environment:

```commandline
source venv/bin/activate 
```

**You will no longer need to create new virtual environment, but
you should always activate this virtual environment before working with script.**

_Also, you can specify the path to and name of virtual environment if you want to:_

```commandline
python -m venv path/name_of_venv
source path/name_of_venv/bin/activate  
```

## Installing packages

Script works with several packages, that should be installed in yor virtual environment before launching the script.  
File **requirements.txt** contains the list of required versions of packages needed to script work correctly.  
To install this packages run:

```commandline
pip install --ignore-requires-python -r requirements.txt 
```

## Launching the script

Finally, script can be launched from current directory by command in terminal:

```commandline
python pain.py
```

To deactivate virtual environment after finishing work with script :

```commandline
deactivate
```

## Further work

**If you want to work with script again in the future, you will need to follow a few steps:**

### 1) Go to directory with script

```commandline
cd path/Virtual_environment_research
```

Where `path` is directory where you downloaded files

### 2) Activate virtual environment
    
```commandline
source venv/bin/activate 
```
or if you specified name of and path to environment: 
```commandline
source path/name_of_venv/bin/activate 
```
### 3) Work with script

To launch the script 
```commandline
python pain.py
```
### 4) Deactivate virtual environment after end of the work with script
    
```commandline
deactivate
```