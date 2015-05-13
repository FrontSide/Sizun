# Sizun

####A one-click tool for fast and simple code smell detection for various languages, with the goal to support developers in writing clean, extensible and maintainable code

This software implements standards and conventions from a new Software Quality Framework presented in my Bachelor Thesis.

---
![Home Screen](https://raw.githubusercontent.com/FrontSide/Sizun/107c8bffccf012bf65e26890c79de07310acf878/showcase/gui_homescreen.png)

---

![Settings](https://raw.githubusercontent.com/FrontSide/Sizun/107c8bffccf012bf65e26890c79de07310acf878/showcase/gui_settings.png)

---

![Results](https://raw.githubusercontent.com/FrontSide/Sizun/107c8bffccf012bf65e26890c79de07310acf878/showcase/gui_results1.png)

---

## Setup

**Download the latest [Release](https://github.com/FrontSide/Sizun/releases) (or the current master if you are feeling lucky) and unzip it.**<br />

Make sure you have all the necessary requirements - as listed below - installed.
All other dependencies are installed during the first run.

## Requirements

- python3.4+ with pip
- [Silver Searcher](https://github.com/ggreer/the_silver_searcher)

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
Support for Mac is currently not planned, should, however, not be such a problem to realise.

### Programming Languages
Currently Sizun focuses on the inspection of **Java** and **Python** source code.

Intended is support for: **C**, **C++**, **C#**, **Scala**, **Ruby**, **Javascript** and **PHP** and whatever there is.

Not intended is support for: **Whitespace**

## Features
Currently the following code smells are detected:
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

### Send API calls to:

    localhost:8373

#### Example:

    curl localhost:8373/run
