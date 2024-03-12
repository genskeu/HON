// tool display properties
cornerstoneTools.toolColors.setToolColor("lightgreen")
cornerstoneTools.toolColors.setActiveColor("lightgreen")
cornerstoneTools.toolStyle.setToolWidth(3)


// function to preload images before study can be started
// validation check if all data is accessible
$(document).ready(function(){
  //$("#start_study").prop('disabled', true);
    study_id = $("#content").attr("study_id");
    // ajax request to get all images
/*     $.ajax({
        type: 'GET',
        url: '/study/get_cs_stacks/' + study_id + '/single_images',
        dataType: 'json',
        contentType: 'application/json; charresponse=utf-8',
        success: function(response) {
          //loop over stacks (single image stacks in this case)
          let i = 0
          response.cs_stacks.forEach(function(cs_stack){
            cs_stack.imageIds.map(imageId => cornerstone.loadAndCacheImage(imageId).then(
              function(){
                progress = ++i/response.cs_stacks.length * 100
                //display progress
                $("#load_prog").text("Loading (" + Number(progress).toFixed(2) + "%)")
                if(progress == 100){
                  $("#start_study").prop('disabled', false);
                }
              })
            )
          })
        }
    }) */
})

//button to start study (hides study description)
$(document).ready(function () {
  $("#start_study").click(function () {
    $("#loader_text").fadeIn()
    $("#loader_anim").addClass("loader")
    //switch from discription to study
    const url = $(this).attr("formaction");
    $.when($('#study_description').fadeOut()).done(
      function () { $('#content').fadeTo(200, 1) }).done(
        //success
        function () {
          //load first image set
          $.getJSON(url, function (response) {
            image_stacks = response.imgset.image_stacks
            image_stacks.forEach(function (image_stack) {
              loadDicom(
                image_stack["cs_stack"],
                image_stack["div_id"],
                image_stack["viewport"])
            })
            $("#loader_text").fadeOut()
            $("#loader_anim").removeClass("loader")
          })
          //error handling
        }).fail(function () {
          alert("Error loading first imgset.")
        })
  })
})





function updateProgressbar(current, max){
  $('#progressbar').text(current + "/" + max + " items finished");
  $('#progressbar').width((Number(current)/Number(max)*100)+"%");
}


//sent data to server (flask app)
$(document).ready(function () {
  $(".vote_button").click(function () {
    var result = {}
    // get scale data
    // no scale present
    if(document.getElementById("scale_0") == null){
      result["scale_input"] = null
    // scale present
    } else {
      result["scale_input"] = get_scale_data()
      // not all scales checked
      if(!result["scale_input"]){
        return
      }
    }

    // get infos on picked stack
    result["picked_stack"] = get_stack_data("dicom_img_" + this.id[this.id.length - 1])

    //validate roi number
    if (!check_ann_number(result["picked_stack"].tool_state)) {
      alert("Incorrect number of annotations!\nPlease check a maximum of " + $("#numb_rois").val() + " annotations have been placed.")
      return
    }

    // disable vote buttons
    $(".vote_button").each(function (index, button) {
      $(button).prop('disabled', true);
    })
    $("#loader_text").fadeIn()
    $("#loader_anim").addClass("loader")

    // ajax post request
    var url = $(this).val();
    $.ajax({
      type: 'POST',
      url: url,
      data: JSON.stringify(result),
      dataType: 'json',
      contentType: 'application/json; charresponse=utf-8',
      // load next imgset
      success: function (response) {
        if (response["error"]){
          $("#loader_text").text(response["error"])
          return
        }

        if (response["status"] == "done") {
          $("#imgset").replaceWith("<h1>You are done. Thanks!</h1>")
          $("#design_settings").fadeOut()
          $("#viewport_settings").fadeOut()
          $("#loader_text").fadeOut()
          $("#loader_anim").removeClass("loader")
          updateProgressbar(Number(response["study_length"]), response["study_length"])
        } else {
          //load next imgset
          image_stacks = response.imgset.image_stacks
          var promises_1 = []
          $.when($(".dicom_img").children().fadeOut()).done(function () {
            setTimeout(function () {
              image_stacks.forEach(
                //load images
                function (image_stack) {
                  promises_1.push(
                    loadDicom(
                      image_stack["cs_stack"],
                      image_stack["div_id"],
                      image_stack["viewport"]))
                })
              Promise.all(promises_1).then(
                function () {
                  //reset scale
                  $("input:radio").prop("checked", false)
                  //fade in after images loaded
                  image_stacks.forEach(function (image_stack) {
                    $("#" + image_stack["div_id"]).children().fadeIn()
                  })
                  image_stacks.forEach(
                    function (image_stack) {
                      //update links of vote buttons and reactivate
                      var id = image_stack["div_id"].match(/\d*$/)[0]
                      $("#vote_" + id).val("/vote/" + response["study_id"] + "/" + (response.imgset["position"]));
                      $("#vote_" + id).prop('disabled', false);
                      $("#vote_" + id).attr('name', image_stack["name"]);
                      //reset roi scales (copies)
                      let roi_scales = $(".RectangleRoi .scale_values:visible, .EllipticalRoi .scale_values:visible, .FreeHandRoi .scale_values:visible")
                      roi_scales.each(function (index, scale) {
                        $(scale).remove()
                      })
                    })
                    $("#loader_text").fadeOut()
                    $("#loader_anim").removeClass("loader")
                })
            }, response["transition_time"] * 1000)
          })
          current_imgset = response
          updateProgressbar(Number(response["imgsets_finished"]), response["study_length"])
        }
      },
      error: function (response) {
        alert("An unknown server error occurred. Please reload the page and try again.")
        $("#loader_text").fadeOut()
        $("#loader_anim").removeClass("loader")
      }
    })
  })
})


function get_scale_data(){
  var scale_data = {}
  var one_scale_empty = false
  //loop over all scales
  $(".scale").each(function(index,scale){
    let text = $(scale).find(".scale_text").text()
    scale_data[text] = {}
    scale_data[text]["uuids"] = []
    scale_data[text]["values"] = []
    // for each scale check if a value has been selected
    $(scale).find(".scale_values:visible").each(function(index,values){
      // scale not checked
      if(!$("input[name='" + values.id + "']:checked").val()){
        alert("No value selected: " + text)
        one_scale_empty = true
        return
      }
      // scale checked
      scale_data[text]["values"].push($("input[name='" + values.id + "']:checked").val())
      if(values.classList[values.classList.length-1] != "scale_values"){
        scale_data[text]["uuids"].push(values.classList[values.classList.length-1])
      }
    })
  })
  //check if all scales are filled
  if(one_scale_empty){
    return
  } else {
    return scale_data
  }
}




//validation of annotation data before sending
function check_ann_number(stack_tool_state){
  let numb_rois = $("#numb_rois").val()
  //count roi and length measurements
  let counted_roi_number = 0
  for(i=0;i<stack_tool_state.length;i++){
    if(!stack_tool_state[i]){continue}
    let tool_names = Object.keys(stack_tool_state[i])
    tool_names.forEach(function(tool_name){
      if(stack_tool_state[i][tool_name]){
        counted_roi_number += stack_tool_state[i][tool_name].data.length
      }
    })
  }

  //check if selected stack has the correct number of rois marked
  if(numb_rois < counted_roi_number && numb_rois != "0"){
    return false
  } else {
    return true
  }
}


//input to scale via keyboard + spacebar next image for single image studies
function keyboard_input_1(event){
  var key_value = Number(event.key)
  if(isNaN(key_value)){
    //hot keys tools
  } else if(event.key == " " && $(".vote_button:visible").length == 1){
    //next image in single image studies such as VGA or ROC
    $(".vote_button:visible").click()
  } else {
    //fill empty scale with keyboard input
    var scale_to_fill;
    // find first empty scale
    $(".scale_values:visible").each(function(index,scale){
      // for each scale check if a value has been selected
      if($(scale).find(":radio:checked").length == 0){
        scale_to_fill = scale
        return false
      }
    })
    if(scale_to_fill){
        // fill scale with key_value
        $(scale_to_fill).find(":radio[value=" +  key_value +"]").prop('checked', true);
    }
  }
}

//next image for multy image studies via keyboard numbers
function keyboard_input_2(event){
  var key_value = Number(event.key)
  var numb_buttons = $(".vote_button:visible").length
  if(!isNaN(key_value) && key_value <= numb_buttons && key_value > 0){
    //next image in multi image studies
    $(".vote_button:visible")[key_value-1].click()
  }
}

$(document).ready(function () {
  var scale_numb = $(".scale").length
  var vote_numb = $(".vote_button").length
  if(scale_numb > 0){
    document.addEventListener("keydown", keyboard_input_1);
  } else if(vote_numb > 1){
    document.addEventListener("keydown", keyboard_input_2);
  }
})