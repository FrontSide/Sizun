
 /**
  * Sizun - Software Quality Inspection
  * MIT License
  * (C) 2015 David Rieger
  */

function notice_noconnect() {
    prompt_error("No connection to Sizun Server!", "error")
    $("#b_run").attr("disabled", "disabled")
}

function enable_run_btn() {
    $("#b_run").removeAttr("disabled")
}

function notice_language(LANGUAGE) {
    $("#l_language").html(LANGUAGE)
}

function show_inspection_results(result) {
    printdata = ""
    $.each(result, function(k, v){
        printdata += "<h2>" + k + "</h2>"
        $.each(v, function(k, v){
            printdata += "<h4>" + k + "</h4>"
            printdata += v
        })
    })

    $("#c_result").html(printdata)
}

function prompt_error(MESSAGE, LEVEL) {

    console.log("Error occurred: LEVEL:: " + LEVEL + ", MESSAGE:: " + MESSAGE)

    $("#c_error").css("display", "block")

    switch (LEVEL) {
        case "error": level_class = "alert"; break;
        case "warning": level_class = "warning"; break;
        case "success": level_class = "success"; break;
        default: level_class = "info"
    }

    $("#c_error > #c_error_text").html(MESSAGE)
    $("#c_error").addClass(level_class)

}

function hide_error() {
    $("#c_error").css("display", "none")
}
