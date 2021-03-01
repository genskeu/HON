//event listerner to display and update roi coordinates via ui 
$(document).ready(function () {
  $(".dicom_img").on("cornerstonetoolsmeasurementrestored", restore_roi_container)
  $(".dicom_img").on("cornerstonetoolsmeasurementcompleted", add_completed_measurement)
  $(".dicom_img").on("cornerstonetoolsmeasurementmodified", update_roi_container)
  $(".dicom_img").on("cornerstonetoolsmeasurementremoved", delete_roi_container)
})

// function used when drawing an roi manually and when restoring annotations from db
function add_roi_container(uuid,div_id_numb,toolName,tool_number,tool_state_data,element){ 
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

  //add delete button for roi 
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

    $("#container_" + uuid).append(point_div)

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
  const tool_header_last = $($("." + toolName)[$("." + toolName).length - 1]).text()
  let tool_number = 1
  if(tool_header_last){
    tool_number = Number(tool_header_last.match(/\d+/)[0]) + 1
  }

  add_roi_container(uuid, div_id_numb,toolName,tool_number,tool_state_data,element)
}

// show roi coordinates on ui when loaded from db
function restore_roi_container(e,image_id,element) {
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
          roi_div.remove()        }
      })
    })
  })
}


//delete all annotations
$(document).ready(function () {
  $(".delete_ann").click(function () {
    var index = this.id.match(/\d+/)[0]
    index = Number(index)
    var elements = cornerstone.getEnabledElements()
    var element = elements[index].element
    var tools = $(".tool_select option:selected").filter(function(){return this.value != ""} )

    //delte scales for rois
    tools.each(function (i,tool) {
      let roi_scales = $("." + tool.value + " .scale_values:visible")
      roi_scales.each(function (index, scale) {
        $(scale).remove()
      })

      //delete roi data shown to user
      $("#rois_img_" + index).find(".roi_pos").remove()

      //delete rois from element
      cornerstoneTools.clearToolState(element, tool.value)
    })

    cornerstone.updateImage(element)
  })
})


//copy roi from other image