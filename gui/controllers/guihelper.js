
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
        var columns = new Array()

        $.each(v["VIOLATIONS"], function(k, violation){

            var column_content = ""

            column_content += "<div class='panel violation-container-panel'>"

            if (violation["CODE"]) {
                code = String(violation["CODE"]).replace(new RegExp(',', 'g'), "<br />");
                column_content += "<pre><code class='" + GLOBAL_LANGUAGE + "'>" + code + "</code></pre><br />"
            }

            if (violation["FILE"]) {

                if (violation["FILE"].constructor === Object) {

                    console.log("Keys in \"Files\":: " + Object.keys(violation["FILE"]))

                    column_content += "<span class='label radius'>Files: </span><br /><code>"

                    $.each(violation["FILE"], function(filename, line){
                        column_content += filename + " :: " + line + "<br />"
                    })

                    column_content += "</code><br />"
                } else {
                    column_content += "<span class='label radius'>File: </span>"
                    column_content += "<code>" + violation["FILE"] + "</code><br />"
                }
            }

            if (violation["LINE"]) {
                column_content += "<span class='label radius'>Line: </span>"
                column_content += "<code>" + violation["LINE"] + "</code><br />"
            }

            if (violation["INFO"]) {
                column_content += "<span class='label radius'>Info: </span>"
                column_content += "<code>" + violation["INFO"] + "</code><br />"
            }


            column_content += "</div>"
            colum_num = vio_counter++%SPLIT_VIOLATIONS_BY

            if (columns[colum_num] == null) {
                columns[colum_num] = ""
            }

            columns[colum_num] += column_content

        })



        //Add the columns to the content
        $.each(columns, function(key, content){
            printdata += "<div class='large-4 columns'>"
            printdata += content
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
        printdata += "<span class='label radius'>" + inspection_names[metric] + "</span>"
        $.each(rule, function(name, value){
            slider_id = metric + "::" +  name
            display_selector = metric + name

            start_value = Math.floor(value*0.5)
            end_value = Math.ceil(value*1.5)

            printdata += "<div class='row vertical-center-container'>"
            printdata += "<div class='small-4 columns vertical-center-box'>"
            printdata += "<span class='label radius secondary'>" + name + "</span>"
            printdata += "</div>"
            printdata += "<div class='small-4 columns vertical-center-box'>"
            printdata += "<div id='" + slider_id + "' class='range-slider' data-slider "
                            + "data-options=\"display_selector: #" + display_selector
                            + "; start: " + start_value
                            + "; end: " + end_value
                            + "; initial: " + value + "\">"
            printdata += "<span class='range-slider-handle' role='slider' tabindex='0'></span>"
            printdata += "<span class='range-slider-active-segment'></span></div></div>"
            printdata += "<div class='small-2 columns vertical-center-box'>"
            printdata += "<input type='number' id='" + display_selector + "' value=" + value + " />"
            printdata += "</div></div>"
        })
    })

    $("#a_settings").html(printdata)
    $(document).foundation('slider', 'reflow');
    activate_slider_listener()
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

function open_progress_modal(message) {
    if (message == null) {
        message = "Inspection In Progress..."
    }
    $('#t_insp_prog').html(message)
    $('#m_insp_prog').foundation('reveal', 'open');
}

function close_progress_modal() {
    $('#m_insp_prog').foundation('reveal', 'close');
}

function hide_error() {
    $("#c_error").css("display", "none")
}
