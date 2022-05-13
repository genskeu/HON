//auto imgsets collect data and send request
$(document).ready(function() {
  $("#btn_auto_imgset").click(function(){
    start = Math.floor(Date.now() / 1000)

    let data = {}
    data["imgset_type"] = $("#imgset_type :selected").val();
    data["order"] = $("#imgset_order").val()
    data["pos_pattern"] = $("#pos_pattern").val();
    data["neg_pattern"] = $("#neg_pattern").val();
    data["ref_stack_name"] = $("#sel_11 :selected").text()
    data["stackmode"] = "single_images"
    if($("#stack_mode").val() == "Stackmode On"){
      data["stackmode"] = "image_stacks"
    }
    data["study_id"] = $("#content").attr("study_id");
    data["div_ids"] = [];
    data["div_ids_ref"] = [];

    for(i=2; i < Number($("#numb_img").val()) + 2;i++){
      data["div_ids"].push("dicom_img_" + i);
    }

    for(i=0; i < Number($("#numb_refimg").val());i++){
      data["div_ids_ref"].push("dicom_img_" + i);
    }

    let viewport = cornerstone.getViewport(document.getElementById("dicom_img_16"))
    let viewport_ref = viewport
    if($("#ref_viewport_auto").is(":checked")){
      viewport_ref = cornerstone.getViewport(document.getElementById("dicom_img_17"))
    }

    if(!viewport | ($("#ref_viewport_auto").is(":checked") & !viewport_ref) ){
      return alert("Please define the viewport settings.\n To do so use the dropdown menus to load an image and if necessary adjust the display settings.\n")
    }

    data["viewport"] = viewport
    data["viewport_ref"] = viewport_ref

    //deactivate all btn
    var buttons = $(".btn");
        buttons.each(function(index,button){
          $(button).prop('disabled', true);
        })
    $("#loader_anim").addClass("loader")
        $("#loader_text").fadeIn()
    
    // sent request
    $.ajax({
        type: 'POST',
        url: "/study/imgsets/auto",
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
      }).done(function(response){
        $("#sidebar").empty()
        imgsets = response["imgsets"]
        imgsets.forEach(function(imgset){
          add_sidebar_entry(imgset.position,imgset.study_id)
          $('#imgset_'+imgset.position).click(load_imgset_on_click)
        })
        if(response["error"]){
          alert(response["error"])
        }
        if(response["error_imgsets"]){
          alert(response["error_imgsets"])
        }
        $('#imgset_'+0).addClass("imgset_active");
        //$('#imgset_'+0).click()
        // show sidebar (navigation between imgsets) if closed
        var sidebar_width = $("#sidebar").width();
        if(sidebar_width == 0){
          $("#sidebar_btn").click();
        };
      }).fail(function(){
        alert("An unknown server error occurred")
      }).always(function(){
        //reactivate all buttons
        buttons.each(function(index,button){
          $(button).prop('disabled', false);
        })
        $("#loader_text").fadeOut()
        $("#loader_anim").removeClass("loader")
      })
  })
})

// animations for the auto create section
// the idea is to collect the data in a sequential manner
// to avoid errors and increase userfriendliness
$(document).ready(function(){
  $("#imgset_type").change(function(){
    if($(this).val() == "standard"){
      $("#row_pos_pattern").fadeOut()
      $("#row_neg_pattern").fadeOut()
      $("#viewport_settings_auto").fadeIn()
      $("#viewport_info_10").fadeIn()
      $("#pos_pattern").val("").change()
      $("#neg_pattern").val("").change()
    } else if ($(this).val() == "afc") {
      $("#row_pos_pattern").fadeIn()
      $("#row_neg_pattern").fadeIn()
      $("#viewport_settings_auto").fadeOut()
      $("#viewport_info_10").fadeOut()
      $("#refstack_settings_auto").fadeOut()
      $("#sel_auto").val("").change()
    } else {
      $("#row_pos_pattern").fadeOut()
      $("#row_neg_pattern").fadeOut()
      $("#viewport_settings_auto").fadeOut()
      $("#viewport_info_10").fadeOut()
      $("#refstack_settings_auto").fadeOut()
      $("#sel_auto").val("").change()
      $("#btn_auto_imgset").fadeOut()
      $("#pos_pattern").val("").change()
      $("#neg_pattern").val("").change()
    }
  })
})


$(document).ready(function(){
  $("#dicom_img_16").on("ImageDisplayComplete",function(){
    if($("#numb_refimg").val() > 0){
      $("#refstack_settings_auto").fadeIn()
    }
    $("#btn_auto_imgset").fadeIn()
  })
  $("#dicom_img_16").on("ImageDisplayFailed",function(){
    $("#refstack_settings_auto").fadeOut()
    $("#btn_auto_imgset").fadeOut()
  })
})

$(document).ready(function(){
  $("#ref_viewport_auto").change(function(){
    $("#dicom_img_17").toggle()
    $("#viewport_info_17").toggle()
  })
})

$(document).ready(function(){
  $(".pattern_imgset_auto").change(function(){
    if($("#imgset_type").val() != "afc"){
      return
    }
    neg_pattern = $("#neg_pattern").val()
    pos_pattern = $("#pos_pattern").val()
    if(neg_pattern != "" && pos_pattern != ""){
      $("#viewport_settings_auto").fadeIn()
      $("#viewport_info_16").fadeIn()
    } else {
      $("#viewport_settings_auto").fadeOut()
      $("#viewport_info_16").fadeOut()
      $("#refstack_settings_auto").fadeOut()
      $("#btn_auto_imgset").fadeOut()
    }
  })
})



$(document).ready(() => {
  $("#imgset_creation_mode").click(function() {
    if($("#imgset_creation_mode_text").text() == "Mode:auto"){
      $("#viewports_man_container").show("slow")
      $("#viewports_auto_container").hide("slow")
      $("#imgset_creation_mode_text").text("Mode:manual")
    } else {
      $("#viewports_man_container").hide("slow")
      $("#viewports_auto_container").show("slow")
      $("#imgset_creation_mode_text").text("Mode:auto")
      var patterns = []
      $("#sel_2 option").each(function(){
        var image_name = $(this).text()
        var pattern = image_name.split("_")[1]
        if(pattern && !patterns.includes(pattern) ){
          patterns.push(pattern)
        }
      })
      $("#pos_pattern").empty()
      $("#pos_pattern").append(new Option("", ""));
      $("#neg_pattern").empty()
      $("#neg_pattern").append(new Option("", ""));
      patterns.forEach((pattern) => {
        $("#pos_pattern").append(new Option(pattern, pattern));
        $("#neg_pattern").append(new Option(pattern, pattern));
      })
    }
    $("#roi_settings_container").toggle("slow")
    $.when($("#imgset").toggle("slow")).done(function(){
      $("#imgset_auto").toggle("medium")
    })
  })
})


