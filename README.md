Sizun
=====

A tool for inspecting and assessing the quality of source code with the goal
to support developers in writing clean, extensible and maintainable code.

This software implements standards and conventions from a new Software Quality Framework.

Install
=======

At the momentm, Sizun can only be built from source. 
Download the latest working release (atm. there's just the master branch, though).

Make sure that python3 and pip is installed.

Go into the Sizun directory and download all required packages with:
  
    pip install -r requirements.txt

Now install Silver Searcher (https://github.com/ggreer/the_silver_searcher)[with those install instructions].

That's it.


Usage
=====

Start Sizun (on linux)
    ./sizun 

or on windows
    .\sizun.bat


Open the config file from 
    
    config/application.sizun

enter the path to the src folder of the application that you want to inspect with Sizun

    [BASIC]
    sourcepath = /path/to/my/projects/src

send an HTTP GET request to 

    localhost:5000/run
   
from your browser or from wherever you want.
(There's no frontend interface available yet for Sizun!)

That's it! Your code is now being inspected.
You receive the results as a JSON response.
Additionally xyz.out files are created in the results folder.


Development
===========

The development of Sizun has only started in mid-march 2015. 
A first useable prototype should be available by mid-may!

v0.1-DEV



