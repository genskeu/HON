//reset viewport
$(document).ready(function() {
  $(".reset").click(function() {
    var img_index = this.id.match(/\d+$/)[0]
    img_index = Number(img_index)
    var div_id = "dicom_img_"+img_index
    var element = document.getElementById(div_id)

    url = this.value
    //case 1 imgset data has already been saved to db
    if(url){
      $.getJSON(url, function(imgset){
        const current_imgset = imgset.images
        const image = current_imgset.filter(function(image){
          return image["div_id"] == div_id
        })[0]
        cornerstone.setViewport(element,image.viewport)
      })
    } else {
      //case 2 imgset data has not been saved to db
      cornerstone.reset(element)
    }
  })
})

//voi,zoom,pos manual
$(document).ready(function(){
  $(".viewport_prop").change(function(){
    var input = this.value
    var input_type = this.id.match(/^\D*/)[0]
    var id = this.id.match(/\d+$/)[0]
    var element = document.getElementById("dicom_img_"+id)
    var value = input.match(/-*\d+\.*\d*/)[0]
    var viewport = cornerstone.getViewport(element)
    if(!viewport){
      return
    }
    if(input_type == "ww_"){
      viewport.voi.windowWidth = Number(value)
    }else if(input_type == "wc_"){
      viewport.voi.windowCenter = Number(value)
    }
    else if(input_type == "zoom_"){
      viewport.scale = Number(value)
    }else if (input_type == "pos_x_") {
      viewport.translation.x = Number(value)
    }else if (input_type == "pos_y_") {
      viewport.translation.y = Number(value)
    }
    cornerstone.setViewport(element,viewport)
  })
})

//update saved imgsets
$(document).ready(function(){
  $("#update_viewports").click(function(){
    let viewport_settings = {}
    let study_id = $("#content").attr("study_id")
    viewport_settings["ww"] = Number($("#def_ww").val())
    viewport_settings["wc"] = Number($("#def_wc").val())
    viewport_settings["zoom"] = Number($("#def_zoom").val())
    viewport_settings["pos_x"] = Number($("#def_pos_x").val())
    viewport_settings["pos_y"] = Number($("#def_pos_y").val())

    $.ajax({
      type: 'PUT',
      url: "/study/imgsets/" + study_id,
      data: JSON.stringify(viewport_settings),
      dataType: 'json',
      contentType: 'application/json; charset=utf-8',
      success: function(response) {
        $(".imgset_active").click()
      },
      error: function(response) {
        alert("An unknown server error occurred")
      }
    });
  })
})

//update imgset currently displayed
$(document).ready(function(){
  $(".viewport_prop_def").change(function(){
    var input = this.value
    var input_type = this.id.match(/^\D*/)[0].replace("def_","")
    var value = Number(input.match(/-*\d+\.*\d*/)[0])
    $("." + input_type).val(value)
    $("." + input_type).change()
  })
})