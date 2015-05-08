
 /**
  * Sizun - Software Quality Inspection
  * MIT License
  * (C) 2015 David Rieger
  */


var GLOBAL_LANGUAGE = "java"

var inspection_names = new Array();
inspection_names["CC"] = "Cyclomatic complexity"
inspection_names["CD"] = "Code Duplications"
inspection_names["FE"] = "Feature Envy"

//Number of violation boxes in one row (for full display size)
var SPLIT_VIOLATIONS_BY = 3

$(document).foundation();

hide_error()
check_connection()
