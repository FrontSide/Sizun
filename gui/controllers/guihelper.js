
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

        printdata += "<div class='row'>"
        printdata += "<div class='large-5 columns panel-metric-header metricname-panel'>" + k + "</div>"
        printdata += "<div class='large-5 columns panel-metric-header escalaton-panel'> Excalation Level: " + v["ESCALATION"] + "</div>"
        printdata += "</div>"

        $.each(v["VIOLATIONS"], function(k, violation){

            if (violation["CODE"]) {
                code = String(violation["CODE"]).replace(new RegExp(',', 'g'), "<br />");
                printdata += "<div class='panel violation-container-panel'>"
                printdata += "<pre><code class='" + GLOBAL_LANGUAGE + "'>" + code + "</code></pre><br />"
            }

            if (violation["FILE"]) {

                if (violation["FILE"].constructor === Object) {

                    console.log("Keys in \"Files\":: " + Object.keys(violation["FILE"]))

                    printdata += "<span class='label radius'>Files: </span><br /><code>"

                    $.each(violation["FILE"], function(filename, line){
                        printdata += filename + " :: " + line + "<br />"
                    })

                    printdata += "</code><br />"
                } else {
                    printdata += "<span class='label radius'>File: </span>"
                    printdata += "<code>" + violation["FILE"] + "</code><br />"
                }
            }

            if (violation["LINE"]) {
                printdata += "<span class='label radius'>Line: </span>"
                printdata += "<code>" + violation["LINE"] + "</code><br />"
            }

            if (violation["INFO"]) {
                printdata += "<span class='label radius'>Info: </span>"
                printdata += "<code>" + violation["INFO"] + "</code><br />"
            }

            printdata += "</div>"
        })
    })

    $("#c_result").html(printdata)

    //Syntax Highlighting
    $('pre code').each(function(i, block) {
        hljs.highlightBlock(block);
    });

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
