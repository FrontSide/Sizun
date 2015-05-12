
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

        switch (parseInt(v["ESCALATION"])) {
            case 1: esc_level = "success"; break;
            case 2: esc_level = "secondary"; break;
            case 3: esc_level = "secondary"; break;
            case 4: esc_level = "alert"; break;
            default: esc_level = "secondary";
        }

        printdata += "<hr /><div class='panel violation-container-panel violation-container-category-panel  fit-to-content-container'>"
        printdata += "<div class='large-8 columns'><b>" + inspection_names[k] + "</b></div>"
        printdata += "<div class='large-4 columns align-right'>"
        printdata += "<label class='" + esc_level + " radius label'>Escalation Level: " + v["ESCALATION"] + "</label></div>"
        printdata += "</div>"

        var vio_counter = 0
        var modulo_result = v["VIOLATIONS"].length % SPLIT_VIOLATIONS_BY
        var num_violations = modulo_result == 0 ? v["VIOLATIONS"].length : (v["VIOLATIONS"].length + SPLIT_VIOLATIONS_BY - modulo_result)

        printdata += "<div class='large-4 columns'>"

        $.each(v["VIOLATIONS"], function(k, violation){

            if ((vio_counter++ != 0) && ((vio_counter % ((num_violations / 3) + 1)  == 0))) {
                printdata += "</div><div class='large-4 columns'>"
            }

            printdata += "<div class='panel violation-container-panel'>"

            if (violation["CODE"]) {
                code = String(violation["CODE"]).replace(new RegExp(',', 'g'), "<br />");
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
        printdata += "</div>" //Closes the row for this pair of violations
    })

    $("#c_result").html(printdata)

    //Syntax Highlighting
    $('pre code').each(function(i, block) {
        hljs.highlightBlock(block);
    });

    close_progress_modal()

}

function show_settings(orig) {

    console.log("rendering settings...")

    printdata = ""

    $.each(orig, function(metric, rule){
        printdata += "<span class='label radius'>" + metric + "</span>"
        $.each(rule, function(name, value){
            slider_id = metric + name + "S"
            display_selector = metric + name
            printdata += "<span class='label radius warning'>" + name + "</span>"
            printdata += "<div class='row'>"
            printdata += "<div class='small-4 columns'>"
            printdata += "<div id='" + slider_id + "' class='range-slider' data-slider data-options=\"display_selector: #" + display_selector + "; initial: " + value + ";\">"
            printdata += "<span class='range-slider-handle' role='slider' tabindex='0'></span>"
            printdata += "<span class='range-slider-active-segment'></span></div></div>"
            printdata += "<div class='small-2 columns'>"
            printdata += "<input type='number' id='" + display_selector + "' value=" + value + " />"
            printdata += "</div></div>"
        })
    })

    $("#a_settings").html(printdata)

    /* Set Values for Sliders */
    $.each(orig, function(metric, rule){
        $.each(rule, function(name, value){
            slider_id = metric + name + "S"
            display_selector = metric + name
            // $("#" + slider_id).foundation('slider', 'set_value', value);
        })
    })

    $(document).foundation('slider', 'reflow');

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
    $("#c_error").attr("class", "alert-box " + level_class + " radius")

}

function open_progress_modal() {
    $('#m_insp_prog').foundation('reveal', 'open');
}

function close_progress_modal() {
    $('#m_insp_prog').foundation('reveal', 'close');
}

function hide_error() {
    $("#c_error").css("display", "none")
}
