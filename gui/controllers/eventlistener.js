
 /**
  * Sizun - Software Quality Inspection
  * MIT License
  * (C) 2015 David Rieger
  */

  $("#i_sourcepath").keyup(function(e){
      console.log("i_sourcepath TRIGGERED");
      /* from http_req.js */
      srcpath = $("#i_sourcepath").val()

      if (srcpath.indexOf("/") === 0) {
          update_sourcepath(srcpath);
      }

      if (e.which == 13) {

          //Clone git repo first if applicable
          if (srcpath.indexOf("http") === 0) {
              open_progress_modal("Clone GIT Repository...")
              update_git(srcpath)
              close_progress_modal()
          }

          run_inspection();
      }
  });

  $("#b_run").click(function(){
      console.log("b_run TRIGGERED");

      //Clone git repo first if applicable
      if ($("#i_sourcepath").val().indexOf("http") === 0) {
          open_progress_modal("Clone GIT Repository...")
          update_git(srcpath)
          close_progress_modal()
      }

      run_inspection();
  });

  $("#b_settings").click(function(){
      console.log("b_settings TRIGGERED");
      get_all_rulesettings()
  })


  function activate_slider_listener() {
      $('[data-slider]').on('change.fndtn.slider', function(){
          console.log("slider TRIGGERED");

          metric = $(this).attr('id').split("::")[0]
          rule = $(this).attr('id').split("::")[1]
          value = $(this).attr('data-slider')

          update_rule(metric, rule, value)

      });
  }
