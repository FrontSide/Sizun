
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
            GLOBAL_LANGUAGE = data["LANGUAGE"]
            hide_error()
            notice_language(data["LANGUAGE"])
        }).fail(function(data) {
            prompt_error(data.responseJSON["message"], data.responseJSON["type"])
        })
}

function get_all_rulesettings() {
    console.log("get_all_rulesettings...")
    $.getJSON("http://" + HOST + ":" + PORT + "/rule/all", function (data) {
    }).done(function(data) {
        hide_error()
        show_settings(data)
    }).fail(function(data) {
        prompt_error(data.responseJSON["message"], data.responseJSON["type"])
    })
}

function update_rule(metric, rule, value) {
    console.log("update_rule...")
    $.getJSON("http://" + HOST + ":" + PORT + "/rule/set/" + metric + "/" + rule + "/" + value, function (data) {
    }).done(function(data) {
        hide_error()
    }).fail(function(data) {
        prompt_error(data.responseJSON["message"], data.responseJSON["type"])
    })
}

function update_sourcepath(SOURCEPATH) {
    console.log("update sourcepath...")

    $.getJSON("http://" + HOST + ":" + PORT + "/sourcepath/set/'" + SOURCEPATH + "'", function (data) {
        }).done(function() {
            hide_error()
            get_language()
        }).fail(function() {
            check_for_error(data)
        })
}

function run_inspection() {
    console.log("run inspection...")
    open_progress_modal()
    $.getJSON("http://" + HOST + ":" + PORT + "/run", function (data) {
        }).done(function(data) {
            hide_error()
            show_inspection_results(data)
        }).fail(function(data) {
            check_for_error(data)
        })
}

function check_for_error(serverresponse) {
    resp = serverresponse.responseJSON
    if (resp != null && resp.constructor == Object && resp["type"] != null) {
        prompt_error(resp["message"], resp["type"])
    } else {
        notice_noconnect()
    }
}
