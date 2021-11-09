//event listerner to display and update roi coordinates via ui 
$(document).ready(function () {
  $(".dicom_img").on("cornerstonetoolsmeasurementrestored", restore_roi_container)
  $(".dicom_img").on("cornerstonetoolsmeasurementcompleted", add_completed_measurement)
  $(".dicom_img").on("cornerstonetoolsmeasurementmodified", update_roi_container)
  $(".dicom_img").on("cornerstonetoolsmeasurementremoved", delete_roi_container)
})

// function used when drawing an roi manually and when restoring annotations from db
function add_roi_container(uuid,div_id_numb,toolName,tool_number,tool_state_data,element){ 
  //check if roi container exists already
  if(!uuid | $("#container_" + uuid).length){
    return
  }
  // add roi container
    let roi_info =
    '<div id="container_' + uuid + '" class="mt-1 badge-light roi_pos  ' + toolName + '">\
        <div class="row mx-auto">\
          <h6 class="col mt-2">' + toolName + " " + tool_number + '</h6>\
        </div>\
    </div>'

  $("#rois_img_" + div_id_numb).append(roi_info)



  // get roi coordinates
  let points = []
  if (toolName == "FreehandRoi") {
    points = tool_state_data.handles.points
  } else if (toolName == "EllipticalRoi" | toolName == "RectangleRoi") {
    points.push(
      tool_state_data.handles.start,
    )
    points.push(
      tool_state_data.handles.end,
    )
  }
  
  // show roi coordinates in container
  // coordinates only show study during setup
  if(window.location.href.includes("design")){
    add_roi_coordinates_container(points,toolName,uuid)
  }

  //add copy and delete button for roi 
  let del_btn = '<div class="row mx-auto">\
                  <button id="del_btn_' + uuid + '" class="col btn btn-danger">\
                    delete ' + toolName + " " + tool_number + '\
                  </button>\
                </div>'
  $("#container_" + uuid).append(del_btn)

  $("#del_btn_" + uuid).click(function(){
    delete_tool_state_by_uuid(uuid)
    cornerstone.updateImage(element)
  })
}

// 
function add_roi_coordinates_container(points,toolName,uuid){
  points.forEach(function (point, i) {
    let point_name = "Point " + i
    if (i == 0) { point_name = "Start" }
    if (i == points.length - 1) { point_name = "End" }
    let point_div = '<div id="point_' + i + '" class="row mx-auto">\
                        <div class="input-group">\
                            <div class="input-group-prepend col-4 px-0 mx-0">\
                              <span class="input-group-text col-12">' + point_name + '</span>\
                            </div>\
                            <input id="x_' + i + uuid + '" type="Number" data-roitype="' + toolName + '" data-uuid="' + uuid + '" step="any" class="form-control roi_pos_input" placeholder="x" value="' + Number.parseFloat(point.x).toFixed(2) + '">\
                            </input>\
                            <input id="y_' + i + uuid + '" type="Number" data-roitype="' + toolName + '" data-uuid="' + uuid + '" step="any" class="form-control roi_pos_input" placeholder="y" value="' + Number.parseFloat(point.y).toFixed(2) + '">\
                            </input>\
                        </div>\
                      </div>'

    // freehand rois have many points
    // default = collapse them
    if (i == 2){
      let points_btn = 
      '<button class="btn btn-dark col-12 mb-2" data-toggle="collapse" data-target="#points_' + uuid + '" aria-expanded="false"\
      aria-controls="sidebar" data-toggle="tooltip" data-placement="left">\
        Points\
      </button>'
      let points = 
        '<div id="points_' + uuid + '" class="row mx-auto collapse">\
        </div>'
        $("#container_" + uuid).append(points_btn)
        $("#container_" + uuid).append(points)

    } 
    if (i == 0 | i == points.length - 1){
      $("#container_" + uuid).append(point_div)
    } else {
      $("#points_" + uuid).append(point_div)
    }

    //fct to update roi pos on input
    $("#x_" + i + uuid).change(function () { 
      point.x = $(this).val()
      cornerstone.updateImage(element)
    })
    $("#y_" + i + uuid).change(function () {
      point.y = $(this).val()
      cornerstone.updateImage(element)
    })

  })
}


// show roi coordinates on ui when roi drawn by user
function add_completed_measurement(e) {
  const uuid = e.detail.measurementData.uuid
  const toolName = e.detail.toolName
  const tool_state_data = e.detail.measurementData
  const element = e.target

  const div_id = e.currentTarget.id
  const div_id_numb = div_id.match(/\d+/)[0]
  // number tool by types
  const tool_header_last = $($("." + toolName + ".roi_pos")[$("." + toolName + ".roi_pos").length - 1]).text()
  let tool_number = 1
  if(tool_header_last){
    tool_number = Number(tool_header_last.match(/\d+/)[0]) + 1
  }

  add_roi_container(uuid, div_id_numb,toolName,tool_number,tool_state_data,element)
}

// show roi coordinates on ui when loaded from db
function restore_roi_container(e,image_id,element) {
  // empty roi containers
  id = element.id.match(/\d+/)[0]
  $("#rois_img_" + id).find(".roi_pos").remove()
  let tool_states = cornerstoneTools.globalImageIdSpecificToolStateManager.toolState[image_id]
  let tool_names = Object.keys(tool_states)
  //loop over different tool types
  tool_names.forEach(function(tool_name){
    let tool_datas = tool_states[tool_name].data
    //loop over different states belonging to one tool and image
    tool_datas.forEach(function(tool_data,i){
      const div_id_numb = element.id.match(/\d+/)[0]
      add_roi_container(tool_data.uuid, div_id_numb, tool_name, i+1, tool_data, element)
    })
  })
}


// update roi coordinates on ui when roi is moved
function update_roi_container(e) {
  if (!e.currentTarget.className.includes("dicom_img")) {
    return
  }
  // get coordinates
  let roi_div = $("#container_" + e.detail.measurementData.uuid)
  let points = [];
  if (e.detail.toolName == "FreehandRoi") {
    points = e.detail.measurementData.handles.points
  } else if (e.detail.toolName == "EllipticalRoi" | e.detail.toolName == "RectangleRoi") {
    points.push({
      x: e.detail.measurementData.handles.start.x,
      y: e.detail.measurementData.handles.start.y
    })
    points.push({
      x: e.detail.measurementData.handles.end.x,
      y: e.detail.measurementData.handles.end.y
    })

  }
  //update ui and display points
  points.forEach(function (point, i) {
    let point_div = roi_div.find("#point_" + i)
    point_div.find("#x_" + i + e.detail.measurementData.uuid).val(point.x)
    point_div.find("#y_" + i + e.detail.measurementData.uuid).val(point.y)
  })
}

// delete roi ui when they are removed (draged out)
// does not work for freehand => use delete button
function delete_roi_container(e) {
  if (!e.currentTarget.className.includes("dicom_img")) {
    return
  }
  // rois
  try {
    let roi_div = $("#container_" + e.detail.measurementData.uuid)
    roi_div.remove()
  } catch {
    alert("Error removing roi. Please reload the imgset.")
  }
}

// delete roi button
function delete_tool_state_by_uuid(uuid){
  //loop through all tool states and delete by uuid
  let globalImageIdSpecificToolStateManager = cornerstoneTools.globalImageIdSpecificToolStateManager
  let tool_states = globalImageIdSpecificToolStateManager.toolState
  let image_ids = Object.keys(tool_states)
  // first layer are image ids
  image_ids.forEach(function(image_id){
    let tool_names = Object.keys(tool_states[image_id])
    // each image can have tool states from different tools
    tool_names.forEach(function(tool_name){
      tool_state_data = tool_states[image_id][tool_name].data
      //multp tool states for each tool
      tool_state_data.forEach(function(data,index){
        if(uuid == data.uuid){
          //remove roi
          tool_states[image_id][tool_name].data.splice(index,1)
          //remove roi container
          let roi_div = $("#container_" + uuid)
          roi_div.remove()
          //remove scales related to roi
          let roi_scales = $("." + uuid + ".scale_values:visible")
          roi_scales.each(function(index,scale){
            $(scale).remove()
          })        
        }
      })
    })
  })
}


//delete all annotations
//not needed anymore, also buggy
// $(document).ready(function () {
//   $(".delete_ann").click(function () {
//     var index = this.id.match(/\d+/)[0]
//     index = Number(index)
//     var elements = cornerstone.getEnabledElements()
//     var element = elements[index].element
//     cornerstoneTools.globalImageIdSpecificToolStateManager.clear(element)
//     var tools = $(".tool_select").filter(function(){return this.value != ""} )

//     //delte scales for rois
//     tools.each(function (i,tool) {
//       let roi_scales = $("." + tool.value + " .scale_values:visible")
//       roi_scales.each(function (index, scale) {
//         $(scale).remove()
//       })

//       //delete roi data shown to user
//       $("#rois_img_" + index).find(".roi_pos").remove()

//       //delete rois from element
//       cornerstoneTools.clearToolState(element, tool.value)
//     })

//     cornerstone.updateImage(element)
//   })
// })


//import roi from other image
$(document).ready(function () {
  $(".import_ann").click(function(){
    // get information of target stack
    id =  this.id.match(/\d+/)[0]
    const element = document.getElementById("dicom_img_" + id)
    var tool_state_displayed_image = cornerstoneTools.getElementToolStateManager(element).toolState
    const currentImageIdIndex = tool_state_displayed_image.stack.data[0].currentImageIdIndex
    const image_id = tool_state_displayed_image.stack.data[0].imageIds[currentImageIdIndex]
    // collect user input
    const imgset_id = Number($("#import_ann_is_" + id).val()) - 1
    const image_pos = Number($("#import_ann_ip_" + id).val()) + 1
    const stack_pos = Number($("#import_ann_sp_" + id).val())
    const study_id = $("#content").attr("study_id");
    const url = "/study/imgset/" + study_id + "/" + imgset_id
    $.getJSON(url, function (response) {
      //get image set
      var image_stack = $(response.imgset.image_stacks).filter(function(){
        return $(this).attr("div_id") == "dicom_img_" + image_pos
      })
      if(image_stack.length){
        image_stack=image_stack[0]
      }else{
        alert("Image not found. Check Image-Position.")
        return
      }
      // transfer tool_state
      let state_to_import;
      if(image_stack.tool_state){
        $(image_stack.tool_state).each((index,state) => {
          if(state && index == (stack_pos - 1)){
            state_to_import = state
            }
        })
      }
      if(state_to_import){
        cornerstoneTools.globalImageIdSpecificToolStateManager.restoreImageIdToolState(image_id,state_to_import)
        $(element).trigger("cornerstonetoolsmeasurementrestored", [image_id, element])
        cornerstone.updateImage(element)
      }else{
        alert("No ROIs found. Check Stack-Position.")
      }
    }).fail(function() {
      alert( "Image-Set not found." );
  })
  })
})


//roi manual input
$(document).ready(function () {
  $(".roi_width,.roi_height,.roi_pos_x,.roi_pos_y").change(function () {
      var input = this.value
      var input_type = this.id.match(/^\D*/)[0]
      var id = this.id.match(/\d+$/)[0]
      var element = document.getElementById("dicom_img_" + id)

      var first = input.match(/-*\d+\.*\d*/)[0]
      const active_tool = document.getElementById("tools").value
      if (active_tool == "EllipticalRoi" || active_tool == "RectangleRoi") {
          var tool_state = cornerstoneTools.getToolState(element, active_tool)
          if (!tool_state) { return }
          var roi_number = tool_state.data.length || 1
          tool_state = tool_state.data[roi_number - 1].handles
          if (tool_state) {
              if (input_type == "roi_width") {
                  var width = Math.abs(tool_state.end.x - tool_state.start.x)
                  var width_new = Number(first)
                  var end_x = tool_state.end.x
                  var start_x = tool_state.start.x
                  if (end_x > start_x) {
                      tool_state.end.x += (width_new - width) / 2
                      tool_state.start.x -= (width_new - width) / 2
                  } else {
                      tool_state.end.x -= (width_new - width) / 2
                      tool_state.start.x += (width_new - width) / 2
                  }
              } else if (input_type == "roi_height") {
                  var height = Math.abs(tool_state.end.y - tool_state.start.y)
                  var height_new = Number(first)
                  var end_y = tool_state.end.y
                  var start_y = tool_state.start.y
                  if (end_y > start_y) {
                      tool_state.end.y += (height_new - height) / 2
                      tool_state.start.y -= (height_new - height) / 2
                  } else {
                      tool_state.end.y -= (height_new - height) / 2
                      tool_state.start.y += (height_new - height) / 2
                  }
              } else if (input_type == "roi_pos_x") {
                  var center_x = Math.abs(tool_state.end.x + tool_state.start.x) / 2
                  var center_x_new = Number(first)
                  tool_state.end.x += (center_x_new - center_x)
                  tool_state.start.x += (center_x_new - center_x)
              } else if (input_type == "roi_pos_y") {
                  var center_y = Math.abs(tool_state.end.y + tool_state.start.y) / 2
                  var center_y_new = Number(first)
                  tool_state.end.y += (center_y_new - center_y)
                  tool_state.start.y += (center_y_new - center_y)
              }
              cornerstone.updateImage(element)
          }
      }
  })
})