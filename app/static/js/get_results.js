// get request for study by study id
$(document).ready(function(){
    $(".get_results_btn").click(function(){
        // build url
        study_id = this.id.match(/\d+/)[0]
        version = "short"
        include_explanation = $("#include_explanations_" + study_id).is(":checked")
        url="/results/"+ study_id + "?include_explanation=" + include_explanation + "?version=" + version
        // loading animation
        $("#loader_anim_man_" + study_id).addClass("loader")
        $("#loader_text_man_" + study_id).fadeIn()
        //disable buttons
        var buttons = $(".get_results_btn");
        buttons.each(function (index, button) {
          $(button).prop('disabled', true);
        })
        $.ajax({
          type: 'GET',
          url: url
      }).done(function(){
        window.location = "/results/download/" + study_id
        $("#loader_text_man_" + study_id).text("Download successful!")
      }).fail(function(){
        $("#loader_text_man_" + study_id).text("An error occurred!")
      }).always(function(){
        $("#loader_anim_man_" + study_id).removeClass("loader")
        buttons.each(function (index, button) {
          $(button).prop('disabled', false);
        })
      })
    })
  })