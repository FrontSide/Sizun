
 /**
  * Sizun - Software Quality Inspection
  * MIT License
  * (C) 2015 David Rieger
  */

function notice_noconnect() {
    $("#b_run").html("NO CONNECTION TO SIZUN SERVER")
    $("#b_run").attr("disabled", "disabled")
}

function enable_run_btn() {
    $("#b_run").removeAttr("disabled")
}
