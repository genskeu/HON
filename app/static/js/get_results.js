// get request for results by study id
$(document).ready(function () {
  $(".get_results_btn").click(function () {
    // build url
    study_id = this.id.match(/\d+/)[0]
    version = "short"
    include_explanation = $("#include_explanations_" + study_id).is(":checked")
    url = "/results/" + study_id + "?include_explanation=" + include_explanation + "?version=" + version
    // loading animation
    $("#loader_anim_" + study_id).addClass("loader")
    $("#loader_text_" + study_id).fadeIn()
    $("#loader_text_" + study_id).text("Please wait.")
    //disable buttons
    var buttons = $(".get_results_btn");
    buttons.each(function (index, button) {
      $(button).prop('disabled', true);
    })
    $.ajax({
      type: 'GET',
      url: url
    }).done(function () {
      window.location = "/results/" + study_id + "/download"
      $("#loader_text_" + study_id).text("Download successful!")
    }).fail(function () {
      $("#loader_text_" + study_id).text("An error occurred!")
    }).always(function () {
      $("#loader_anim_" + study_id).removeClass("loader")
      buttons.each(function (index, button) {
        $(button).prop('disabled', false);
      })
    })
  })
})

// get request for segmentation data by study id
$(document).ready(function () {
  $(".get_seg_btn").click(function () {
    // build url
    study_id = this.id.match(/\d+/)[0]
    url = "/results/seg_data/" + study_id
    // loading animation
    $("#loader_anim_" + study_id).addClass("loader")
    $("#loader_text_" + study_id).fadeIn()
    $("#loader_text_" + study_id).text("Please wait.")
    //disable buttons
    var buttons = $(".get_seg_btn");
    buttons.each(function (index, button) {
      $(button).prop('disabled', true);
    })
    $.ajax({
      type: 'GET',
      url: url
    }).done(function () {
      window.location = url + "/download"
      $("#loader_text_" + study_id).text("Download successful!")
    }).fail(function () {
      $("#loader_text_" + study_id).text("An error occurred!")
    }).always(function () {
      $("#loader_anim_" + study_id).removeClass("loader")
      buttons.each(function (index, button) {
        $(button).prop('disabled', false);
      })
    })
  })
})