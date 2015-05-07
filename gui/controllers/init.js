
 /**
  * Sizun - Software Quality Inspection
  * MIT License
  * (C) 2015 David Rieger
  */


var GLOBAL_LANGUAGE = "java"

var inspection_names = new Array();
inspection_names["CC"] = "Cyclomatic complexity"
inspection_names["CD"] = "Code Duplications"


$(document).foundation();

hide_error()
check_connection()
