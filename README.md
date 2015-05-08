# Sizun

####A one-click tool for fast and simple code smell detection for various languages, with the goal to support developers in writing clean, extensible and maintainable code

This software implements standards and conventions from a new Software Quality Framework presented in my Bachelor Thesis.

## Setup

At the moment, Sizun can only be built from source.
Download the latest working release (atm. there's just the master branch, though), make sure all **Requirements** are installed and continue with **Usage**.

## Requirements

- python3.4+ with pip
- [Silver Searcher](https://github.com/ggreer/the_silver_searcher)
- [Gunicorn](http://gunicorn.org/)

Sizun is also using [PMD](http://pmd.sourceforge.net/pmd-5.2.3/) with CPD in version **5.2.3**.
This is, however, downloaded automatically during the first run.<br />
<sub>(Version 5.3.x of PMD would be available but CPD fails in creating a CSV output which makes the software a little useless for Sizun)</sub>

Right now you also might have to install some python modules manually with pip since this might request root permission. **Alternatively** you can create a python virtual environment in the application folder and install the modules there. This is, however, just a temporary problem that will be gone once a first release is here.

## Usage
### Run with:

    ./run [-s <sourcepath>] [-l <language>] ([-r]|[-G])

Whereas **-r** runs the inspection automatically after start and **-G** opens the in-browser GUI.<br>
The language parameter **-l** should only be used if the automatic detection fails.

#### Example:

    ./run -s /home/mrman/superapp/src -r

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
`/run/[metricname]`  | Execute inspection for one spectific metric
`/sourcepath/set/[sourcepath]`  | Set path to application to inspect*
`/sourcepath/get`  | Get path to application to inspect
`/language/set/[language]`  | Set programming language**
`/language/get`  | Get programming language**
`/inspection/activate/[metricname]`  | Activate Metric Execution
`/inspection/deactivate/[metricname]`  | Deactivate Metric Execution
`/inspection/isset/[metricname]`  | Check if Metric Execution is activated
`/rule/change/[metricname]/[rulename]/[value]`  | Change rule for Inspection Metric
`/rule/reset/[metricname]/[rulename]`  | Reset rule for Inspection Metric
`/rule/get/[metricname]/[rulename]`  | Get rule for Inspection Metric

####*Omit the leading '/' when setting the sourcepath
**The sourcecode's language is by default automatically detected.

### Send API calls to:

    localhost:8373

#### Example:

    curl localhost:8373/run


## Development

### Core Application

**Working so far:**
- Complexity Measurement for JAVA and PYTHON
- Code Duplication Measurement for JAVA
- ReST API as listed in doc (above)

**In effective development (Planned for v0.1.0-alpha):**
- Lazy Class Detection for JAVA
- Large/God Class Detection for JAVA
- Long Parameter List Detection for JAVA
- CLI for running inspections and simple configurations (so that nobody needs to tinker about in the config file)

The development of Sizun has only started in mid-march 2015.
A first useable prototype should be available by mid-may!

Planned release date vor **v0.1.0-alpha** is the **28. May 2015**<br />
Current: **v0.1-dev** (initial rapid development)

### In-Browser GUI
Development in branch: [gui-1](https://github.com/FrontSide/Sizun/tree/gui-1)
