Sizun
=====

**A one-click tool for fast and simple code smell detection for various languages, with the goal to support developers in writing clean, extensible and maintainable code**

This software implements standards and conventions from a new Software Quality Framework presented in my Bachelor Thesis.

Setup
=====

At the moment, Sizun can only be built from source.
Download the latest working release (atm. there's just the master branch, though), make sure all **Requirements** are installed and continue with **Usage**.

Requirements
============

- python3
- pip3
- [Silver Searcher](https://github.com/ggreer/the_silver_searcher)

Sizun is also using [PMD](http://pmd.sourceforge.net/pmd-5.2.3/) with CPD in version **5.2.3**.
This is, however, downloaded automatically during the first run.<br />
<sub>(Version 5.3.x of PMD would be available but CPD fails in creating a CSV output which makes the software a little useless for Sizun)</sub>

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

**Working so far:**
- Complexity Measurement for JAVA

**In effective development (Planned for v0.1.0-alpha):**
- Code Duplication Measurement for JAVA
- Complexity Measurement for PYTHON
- Lazy Class Detection for JAVA
- Large/God Class Detection for JAVA
- Long Parameter List Detection for JAVA
-

The development of Sizun has only started in mid-march 2015.
A first useable prototype should be available by mid-may!

Planned release date vor **v0.1.0-alpha** is the **28. May 2015**<br />
Current: **v0.1-dev** (initial rapid development)
