
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

    $("#c_error").css("display", "block")

    switch (LEVEL) {
        case "error": colour = "#FF0000"; break;
        case "warning": colour = "#FFFF00"; break;
        case "success": colour = "#00FF00"; break;
        default: colour = "#DDD"
    }

    $("#m_error").html(MESSAGE)
    $("#c_error").css("background-color", colour)

}

function hide_error() {
    $("#c_error").css("display", "none")
}
