# Sizun

####A one-click tool for fast and simple code smell detection for various languages, with the goal to support developers in writing clean, extensible and maintainable code.

---

###Inspection of public GitHub repositories is supported

---

This software implements standards and conventions from a new Software Quality Framework presented in my Bachelor Thesis.

Master | 0.x Branch
-------|-----------
[![Master Build Status](https://travis-ci.org/FrontSide/Sizun.svg?branch=master)](https://travis-ci.org/FrontSide/Sizun) | [![0.x Build Status](https://travis-ci.org/FrontSide/Sizun.svg?branch=0.x)](https://travis-ci.org/FrontSide/Sizun)

## Setup

**Download the latest [Release](https://github.com/FrontSide/Sizun/releases) (or the current master if you are feeling lucky) and unzip it.**<br />

Make sure you have all the necessary requirements - as listed below - installed.

---

![Home Screen](https://raw.githubusercontent.com/FrontSide/Sizun/107c8bffccf012bf65e26890c79de07310acf878/showcase/gui_homescreen.png)

---

![Settings](https://raw.githubusercontent.com/FrontSide/Sizun/107c8bffccf012bf65e26890c79de07310acf878/showcase/gui_settings.png)

---

![Results](https://raw.githubusercontent.com/FrontSide/Sizun/107c8bffccf012bf65e26890c79de07310acf878/showcase/gui_results1.png)

## Requirements

- **python3.4+** with **pip** and **virtualenv**
- **[Silver Searcher](https://github.com/ggreer/the_silver_searcher)**
- **git** (optionally if you want to inspect a public repository)

## Usage
### Run with:

    ./run ([-s <sourcepath>]|[-g <url to public git>]) [-l <language>] ([-r]|[-G])

Whereas **-r** runs the inspection automatically after start and **-G** opens the in-browser GUI.<br>
The language parameter **-l** should only be used if the automatic detection is expected to fail.

#### Example:

    ./run -g https://github.com/FrontSide/Dary-The-Blog.git -r

#####That's it! Your code is now being inspected. You receive the results as a JSON response.

## Support
### OS
Sizun is developed and tested under **Linux**. It is also meant to be working under Windows in the near future.
Support for Mac is right now not planned, should, however, not be such a problem to realise.

### Programming Languages
Currently, Sizun works for the inspection of **Java** and **Python** source code.

Intended is support for: **C**, **C++**, **C#**, **Scala**, **Ruby**, **Javascript** and **PHP** and whatever there is.

Not intended is support for: **Whitespace**

## Features

- Currently the following code smells are detected:
- Complex Methods (i.e. Long Method)
- Long Parameter Lists
- Feature Envy
- Duplicated Code

## API
#### Sizun is developed with a web-framework and thus offers a ReST-API

Request | Description
------- | -----------
`/`  | Get all ReST API Mappings
`/run`  | Run full code inspection
`/run/[metricname]`  | Execute inspection for one spectific metric
`/sourcepath/set/[sourcepath]`  | Set path to application to inspect*
`/sourcepath/get`  | Get path to application to inspect
`/git/set`  | Set URL to public GIT repository to be inspected***
`/language/set/[language]`  | Set programming language**
`/language/get`  | Get programming language**
`/inspection/activate/[metricname]`  | Activate Metric Execution
`/inspection/deactivate/[metricname]`  | Deactivate Metric Execution
`/inspection/isset/[metricname]`  | Check if Metric Execution is activated
`/rule/change/[metricname]/[rulename]/[value]`  | Change rule for Inspection Metric
`/rule/reset/[metricname]/[rulename]`  | Reset rule for Inspection Metric
`/rule/get/[metricname]/[rulename]`  | Get rule for Inspection Metric
`/rule/all`  | Get all rules for all metrics with all values

####*Omit the leading '/' when setting the sourcepath
**The sourcecode's language is by default automatically detected.
***Will automatically adjust the sourcepath and language

### Send API calls to:

    localhost:8373

#### Example:

    curl localhost:8373/run
