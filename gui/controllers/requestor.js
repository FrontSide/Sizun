
 /**
  * Sizun - Software Quality Inspection
  * MIT License
  * (C) 2015 David Rieger
  */

HOST = "localhost"
PORT = "8373"

function check_connection() {
    console.log("check connection:")
    try {
        $.getJSON("http://" + HOST + ":" + PORT + "/", function (data) {
        }).done(function() {
            hide_error()
            enable_run_btn()
        }).fail(function() {
            notice_noconnect()
        })
    } catch(e) {
        notice_noconnect()
    }
}

function get_language() {
    console.log("check connection:")
        $.getJSON("http://" + HOST + ":" + PORT + "/language/get", function (data) {
        }).done(function(data) {
            hide_error()
            notice_language(data["LANG"])
        }).fail(function(data) {
            prompt_error(data.responseJSON["message"], data.responseJSON["type"])
        })
}

function update_sourcepath(SOURCEPATH) {
    console.log("update sourcepath...")
    $.getJSON("http://" + HOST + ":" + PORT + "/sourcepath/set/" + SOURCEPATH + "'", function (data) {
        }).done(function() {
            hide_error()
            get_language()
        }).fail(function() {
            prompt_error("failed to update sourcepath", "warning")
        })
}

function run_inspection() {
    console.log("run inspection...")
    $.getJSON("http://" + HOST + ":" + PORT + "/run", function (data) {
        }).done(function(data) {
            hide_error()
            show_inspection_results(data)
        }).fail(function(data) {
            notice_noconnect()
        })
}
