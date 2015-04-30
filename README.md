# Sizun

####A one-click tool for fast and simple code smell detection for various languages, with the goal to support developers in writing clean, extensible and maintainable code

This software implements standards and conventions from a new Software Quality Framework presented in my Bachelor Thesis.

## Setup

At the moment, Sizun can only be built from source.
Download the latest working release (atm. there's just the master branch, though), make sure all **Requirements** are installed and continue with **Usage**.

## Requirements

- python3.4+ with pip
- [Silver Searcher](https://github.com/ggreer/the_silver_searcher)

Sizun is also using [PMD](http://pmd.sourceforge.net/pmd-5.2.3/) with CPD in version **5.2.3**.
This is, however, downloaded automatically during the first run.<br />
<sub>(Version 5.3.x of PMD would be available but CPD fails in creating a CSV output which makes the software a little useless for Sizun)</sub>

## Usage
### 1. Run with:

    ./run

### 2. Open the config file:

    config/application.sizun

### 3. Change the sourcepath to the one of your application to be inspected:

    [BASIC]
    sourcepath = /path/to/my/projects/src

### 4. Send and HTTP GET Request to:

    localhost:5000/run


#### from your browser or from wherever you want.

#####That's it! Your code is now being inspected. You receive the results as a JSON response.

## Support
### OS
Sizun is developed and tested under **Linux**. It is also meant to be working under Windows in the near future.
Support for Mac is right now not planned, should, however, not be such a problem to realise.

### Programming Languages
Currently Sizun focuses on the inspection of **Java** source code.

Also in development is **Python** support.

Intended is support for: **C**, **C++**, **C#**, **Scala**, **Ruby**, **Javascript** and **PHP** and whatever there is.

Not intended is support for: **Whitespace**

## API
#### Sizun is developed with a web-framework and thus offers a ReST-API

Request | Description
------- | -----------
`/run`  | Run full code inspection
`/sourcepath/set/[sourcepath]`  | Set path to application to inspect
`/language/set/[language]`  | Set programming language*
TBA  | Activate Metric Execution
TBA  | Deactivate Metric Execution
TBA  | Change rule for Inspection Metric
*The sourcecode's language is by default automatically detected.


## Development

### Core Application

**Working so far:**
- Complexity Measurement for JAVA
- Code Duplication Measurement for JAVA

**In effective development (Planned for v0.1.0-alpha):**
- Complexity Measurement for PYTHON
- Lazy Class Detection for JAVA
- Large/God Class Detection for JAVA
- Long Parameter List Detection for JAVA
- ReST API command for changing Metric Rules
- ReST API command for (de)activating Metric Executions

The development of Sizun has only started in mid-march 2015.
A first useable prototype should be available by mid-may!

Planned release date vor **v0.1.0-alpha** is the **28. May 2015**<br />
Current: **v0.1-dev** (initial rapid development)

### In-Browser GUI
Currently not in development, but definitely planned. Should be easy to implement due to the ReST-API and the JSON responses.
