
 /**
  * Sizun - Software Quality Inspection
  * MIT License
  * (C) 2015 David Rieger
  */

function check_connection() {
    console.log("check connection:")
    try {
        $.get('http://localhost:5000', function (data) {
        }).done(function() {
            enable_run_btn()
        }).fail(function() {
            notice_noconnect()
        })
    } catch(e) {
        notice_noconnect()
    }
}

function update_sourcepath(SOURCEPATH) {
    console.log("update sourcepath...")
    $.get('http://localhost:5000/sourcepath/set/' + SOURCEPATH, function (data) {
        }).done(function() {
            console.log("OK!")
        }).fail(function() {
            notice_noconnect()
        })
}

function run_inspection() {
    console.log("run inspection...")
    $.get('http://localhost:5000/run', function (data) {
        }).done(function() {
            console.log("OK!")
        }).fail(function() {
            notice_noconnect()
        })
}
