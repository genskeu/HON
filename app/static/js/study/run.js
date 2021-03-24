// tool display properties
cornerstoneTools.toolColors.setToolColor("lightgreen")
cornerstoneTools.toolColors.setActiveColor("lightgreen")
cornerstoneTools.toolStyle.setToolWidth(3)


// function to preload images before study can be started
// validation check if all data is accessible
$(document).ready(function(){
  $("#start_study").prop('disabled', true);
    study_id = $("#content").attr("study_id");
    // ajax request to get all images
    $.ajax({
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
    })
})

//button to start study (hides study description)
$(document).ready(function () {
  $("#start_study").click(function () {
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
            updateProgressbar(Number(response.imgset.position), response["study_length"])
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
    result["scale_input"] = get_scale_data()
    if(!result["scale_input"]){
      return
    }

    // get infos on picked stack
    result["picked_stack"] = get_stack_data("dicom_img_" + this.id[this.id.length - 1])

    //validate roi number
    if (!check_ann_number(result["picked_stack"].tool_state)) {
      alert("Incorrect number of markings!\nPlease check that exactly " + $("#numb_rois").val() + " markings have been placed.")
      return
    }

    // disable vote buttons
    $(".vote_button").each(function (index, button) {
      $(button).prop('disabled', true);
    })

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
        if (response["status"] == "done") {
          $("#imgset").replaceWith("<h1>You are done. Thanks!</h1>")
          $("#design_settings").fadeOut()
          $("#viewport_settings").fadeOut()
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
                })
            }, response["transition_time"] * 1000)
          })
          current_imgset = response
          updateProgressbar(Number(response.imgset["position"]), response["study_length"])
        }
      },
      error: function (response) {
        alert("An unknown server error occurred.")
      }
    })
  })
})


function get_scale_data(){
  if(document.getElementById("scale_0") == null){
      return null
  }
  scale_data = {}
  $(".scale").each(function(index,scale){
    if(!scale_data){
      return false
    }
    let text = $(scale).find(".scale_text").text()
    scale_data[text] = {}
    scale_data[text]["uuids"] = []
    scale_data[text]["values"] = []
    $(scale).find(".scale_values:visible").each(function(index,values){
      if(!$("input[name='" + values.id + "']:checked").val()){
        alert("No value selected: " + text)
        scale_data = false
        return false
      }
      scale_data[text]["values"].push($("input[name='" + values.id + "']:checked").val())
      if(values.classList[values.classList.length-1] != "scale_values"){
        scale_data[text]["uuids"].push(values.classList[values.classList.length-1])
      }
    })
  })
  return scale_data
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
  if(numb_rois != counted_roi_number && numb_rois != "-1"){
    return false
  } else {
    return true
  }
}


//input to scale via keyboard (not working)
document.addEventListener("keydown",function(event){
  scale = document.getElementById("scale_1")
  if (event.keyCode > 47 & event.keyCode < 58 & scale != null) {
    scaleRadio = document.getElementById(event.key)
    if(scaleRadio != null){
        scaleRadio.checked = true
    }
  }
})

//set hotkeys for tools
//$("#tool_act_left option, #tool_act_wheel option").each(function(index,option){
//  document.addEventListener("keydown",function(event){
//    if(option.attributes.key){
//      if (event.key == option.attributes.key.value) {
//        option.selected = true
//      $("#"+option.parentElement.id).change()
//      }
//    }
//  })
//})
