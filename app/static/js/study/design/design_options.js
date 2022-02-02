//color settings
$(document).ready(function() {
  $("#background_color").change(function() {
    document.body.style.backgroundColor=$("#background_color").val();
    $("div.card").css({"background-color":$("#background_color").val()});
    $("#text_color").change(function() {
      document.body.style.color=$("#text_color").val();
    })
  })
})

//number ref-imgs and imgs
$(document).ready(function() {
  $("#numb_img, #numb_refimg").change(function() {

    let img_container;
    let viewport_set;
    let roi_set;
    let img_numb_change = Number($(this).val())

    if(this.id == "numb_img"){
      img_container = $(".dicom_container_img")
      viewport_set = $(".comp_viewport")
      roi_set = $(".comp_rois")
    } else if (this.id == "numb_refimg") {
      img_container = $(".dicom_container_refimg")
      viewport_set = $(".ref_viewport")
      roi_set = $(".ref_rois")
      if(img_numb_change){
        $("#refstack_settings_auto").fadeIn()
      } else {
        $("#refstack_settings_auto").fadeOut()
      }
    }

    img_container.each(function(index){
      // hide not needed viewports
      $(this).width(0)
      if(index < img_numb_change){
        $(this).fadeIn()
        $(viewport_set[index]).fadeIn()
        $(roi_set[index]).fadeIn()
      } else {
        $(this).fadeOut()
        $(viewport_set[index]).fadeOut()
        $(roi_set[index]).fadeOut()
      }
    }).promise().done(function(){
      img_container.each(function(){
        //resize viewports
        if($("#img_width").val() == "" ){
          $("#dicom_img_" + this.id.slice(-1)).width($(this).width())
          $("#img_width").val($(this).width())
        } else {
          $("#dicom_img_" + this.id.slice(-1)).width($("#img_width").val())
        }
        if($("#img_height").val() == "" ){
          $("#dicom_img_" + this.id.slice(-1)).height($(this).width())
          $("#img_height").val($(this).width())
        } else {
          $("#dicom_img_" + this.id.slice(-1)).height($("#img_height").val())
        }
      })
    })
    //adjust allignment
    if(img_numb_change % 2 == 0){
      for(i=0; i<img_numb_change; i++ ){
        if(i % 2 == 0){
          $(img_container[i]).children().addClass("float-right")
          $(img_container[i]).children().children().addClass("float-right")
        } else {
          $(img_container[i]).children().addClass("float-left")
          $(img_container[i]).children().children().addClass("float-left")
        }
      }
    } else {
      for(i=0; i<img_numb_change; i++ ){
        if(i % 2 == 0){
          $(img_container[i]).children().removeClass("float-right")
          $(img_container[i]).children().children().removeClass("float-right")
        } else {
          $(img_container[i]).children().removeClass("float-left")
          $(img_container[i]).children().children().removeClass("float-left")
        }
      }
    }

  })
})

//define image size
$(document).ready(function(){
  $(".image_size").change(function(){
    let value = this.value
    let dicom_containers = $(".dicom_container")
    if(this.id == "img_width"){
      cornerstone.getEnabledElements().forEach(function(element){
        $(element.element).width(Number(value))
        cornerstone.resize(element.element)
      })

    } else if(this.id == "img_height") {
      cornerstone.getEnabledElements().forEach(function(element,index){
        $(element.element).height(Number(value))
        cornerstone.resize(element.element)
      })
    }
  })
})

//tool hot keys, avoid conflicts
$(document).ready(function(){
  $(".tool_hotkeys").change(function(){
    // check for conflicts
    hotkey_sel = this
    hotkeys = $(".tool_hotkeys")
    hotkeys.each(function(index,hotkey){
      if(hotkey == hotkey_sel){
        return true
      }
      if(hotkey.value==hotkey_sel.value && hotkey.value != ""){
        hotkey.value = ""
      }
    })
  })
})


//sent design settings to server
$(document).ready( function() {
  $('#submit_design,#return_study_ov').click(function() {
    var design = {}
    var study_id = $("#content").attr("study_id")
    design["study_id"] = study_id
    design["instructions"] = $("#instructions").val()
    design["button_labels"] = $("#button_labels").val()
    design["text_color"] =  $("#text_color").val()
    design["background_color"] =  $("#background_color").val()
    design["numb_img"] = $("#numb_img").val()
    design["numb_refimg"] = $("#numb_refimg").val()
    design["img_width"] = $("#img_width").val()
    design["img_height"] = $("#img_height").val()
    design["numb_rois"] = $("#numb_rois").val()
    regexp_1st_numb = /\d+\.*\d*/
    regexp_2nd_numb = /\d+\.*\d*$/

    design["transition_time"]=Number($("#transition_time").val())

    var tools = {}
    $('input:checkbox[name=toolsCheck]').each(function(){
        tool =  {}
        tool["label"] = this.value
        tool["key_binding"] = null
        if(this.checked){
          tool["status"] = "active"
        } else {
          tool["status"] = "inactive"
        }
        tools[this.id] = tool
      }
    )
    design["tools"] = tools
    design["show_viewport_info"] = $("#show_viewport_info").val() == "Enabled"
    var scales = []
    let scale_inputs = $(".scale")
    if(scale_inputs.length > 0){
      scale_inputs.each(function(index,scale){
        scale_data = {}
        scale_data["min"] = $(scale).find(".scale_min_input").val()
        scale_data["max"] = $(scale).find(".scale_max_input").val()
        scale_data["text"] = $(scale).find(".scale_text_input").val()
        scale_data["type"] = $(scale).find(".scale_type_input").val()
        scales.push(scale_data)
      })
    }
    design["scales"] = scales

    $.ajax({
        type: 'POST',
        url: window.location.href,
        data: JSON.stringify(design),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            alert("Design saved successfully.")

              $("#design_btn").click()
              var sidebar_width = document.getElementById("sidebar").style.width
              if(sidebar_width == ""|
                 sidebar_width == "0px"){
                $("#sidebar_btn").click()
              }
        },
        error: function(response) {
            alert("An unknown server error occurred")
            //reactivate all buttons
            buttons.each(function(index,button){
              $(button).prop('disabled', false);
            })
            $("#loader_text_auto").fadeOut()
            $("#loader_anim_auto").removeClass("loader")
        }
    })
  });
});

//show viewport info
$(document).ready(() => {
  $("#show_viewport_info").click(function() {
    if(this.value == "Enabled"){
      $(".overlay").fadeOut()
      this.value = "Disabled"
      $(this).removeClass("btn-success")
      $(this).addClass("btn-danger")
    } else {
      $(".overlay").fadeIn()
      this.value = "Enabled"
      $(this).removeClass("btn-danger")
      $(this).addClass("btn-success")
    }
  })
})

$(document).ready(() => {
  $("#instructions_input_field").change(function() {
    $("#instructions_user_view").empty()
    $("#instructions_user_view").text($("#instructions").val())
  })
})


//update design when page first loads
$(document).ready( function() {
  $("#background_color").change();
  $("#text_color").change();
  $("#numb_img").change();
  $("#numb_refimg").change();
  $("#scale_text_input_1").change();
  $("#tools").val("")
  $(".sel_image").each((index,sel) => $(sel).val("") )
  $("#stack_mode").click()
})

