//scales
//update scale
function update_scale(event) {
  let id = event.target.id.match(/\d*$/)[0]
  $("#scale_values_" + id).empty()
  $("#scale_labels_" + id).empty()
  $("#scale_text_" + id).empty()
  min = Number($("#scale_min_input_" + id).val())
  max = Number($("#scale_max_input_" + id).val())
  $("#scale_text_" + id).text($("#scale_text_input_" + id).val())
  if (min < max) {
    for (var i = min; i <= max; i++) {
      $("#scale_values_" + id).append("<div class='col-1' id='scale_value_" + id + "_" + i + "'></div>")
      $("#scale_value_" + id + "_" + i).append("<div class='row mx-auto'>" + i.toString() + "</div>")
      $("#scale_value_" + id + "_" + i).append("<input type='radio' name=scale_values_" + id + " value=" + i.toString() + ">")
    }
  }
}

//add change and remove function to exisitng scales
$(document).ready(function(){
  // change
  $(".scale_text_input, .scale_min_input, .scale_max_input").change(function (event) {update_scale(event)})
  $(".scale_text_input, .scale_min_input, .scale_max_input").change()

  //remove scale functionality
  $(".scale_rm").click(function () {
    let id = event.target.id.match(/\d*$/)[0]
    $("#scale_" + id).remove()
  })
})


//add scale input fields to define scale during study set up
$(document).ready(function () {
  $("#add_scale").click(function () {
    //clone hidden template defined in design.html
    let scale_template = $("#scale_").clone()
    //adjust the ids
    let id_names = ["scale_view_admin_", "scale_heading_",
                "scale_text_input_", "scale_min_input_", 
                "scale_max_input_" , "scale_type_input", 
                "scale_rm_", "scale_view_user_", 
                "scale_text_","scale_values_"]
    let index;
    if($(".scale").length == 0){
      index = 0
    } else {
      index = $(".scale").last().attr("id").match(/\d$/)[0]
      index = Number(index) + 1
    }
    id_names.forEach(function(id){
      scale_template.find("#" + id).attr("id",id + index)
    })
    scale_template.attr("id","scale_" + index)
    scale_template.find("#" + "scale_heading_" + index).text("Scale " + (index + 1))
    scale_template.removeClass("scale_template")
    scale_template.addClass("scale")
    scale_template.css("display","")
    scale_template.appendTo("#scales")
    
    $("#scale_rm_" + index).click(function () {
      let id = event.target.id.match(/\d*$/)[0]   
      $("#scale_" + id).remove()
    })

    //function to update preview based on user input
       $("#scale_text_input_" + index + " , #scale_min_input_" + index + " , #scale_max_input_" + index).change(function (event) { update_scale(event) })
  })
})

//copy scale on roi drawn
$(document).ready(function () {
  var elements = document.getElementsByClassName("dicom_img")
  for (i = 0; i < elements.length; i++) {
    elements[i].addEventListener('cornerstonetoolsmeasurementadded', repeat_scale);
  }
})

// roi scale should be repeated for every roi 
// not be present before roi is drawn
function repeat_scale(e) {
  let scales = $("." + e.detail.toolType + ".scale_values:hidden")
  if(! e.detail.toolType.includes("Roi") & scales.length){
    return
  }
  let id = e.detail.measurementData.uuid

  scales.each(function (index, scale) {
      let scale_copy = $(scale).clone()
      scale_copy.addClass(id)
      scale_copy.children().each(function () {
        $(this).children("input").attr("name", scale_copy.attr("id") + "_" + id)
        $(this).children("input").prop("checked", false)
      })
      scale_copy.attr("id",scale_copy.attr("id") + "_" + id)
      $("#" + scale.parentElement.id).append(scale_copy)
      $('.'+id).show();
  })
}

//remove scale on roi deleted
$(document).ready(function () {
  var elements = document.getElementsByClassName("dicom_img")
  for (i = 0; i < elements.length; i++) {
    elements[i].addEventListener('cornerstonetoolsmeasurementremoved', remove_scale);
  }
})

//delete ann scales
function remove_scale(e){
  let id = e.detail.measurementData.uuid
  let roi_scales = $("." + id + ".scale_values:visible")
  roi_scales.each(function(index,scale){
    $(scale).remove()
  })
} 
