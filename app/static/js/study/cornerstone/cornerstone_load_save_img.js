//load images
function loadDicom(stack,div_id,viewport=null,tool_state=null){
  //where to display
  const element = document.getElementById(div_id)
  // reset tool data
  cornerstoneTools.globalImageIdSpecificToolStateManager.clear(element)
  // empty roi containers
  id = div_id.match(/\d+/)[0]
  $("#rois_img_" + id).find(".roi_pos").remove()
  // preload entire stack
  stack.imageIds.map(imageId => cornerstone.loadAndCacheImage(imageId))
  // load and display specified image
  const promise = cornerstone.loadAndCacheImage(stack.imageIds[stack.currentImageIdIndex]).then(function(image) {
    if(!viewport){
      viewport = cornerstone.getDefaultViewportForImage(element,image)
    }
    cornerstone.displayImage(element, image, viewport)
    cornerstoneTools.addStackStateManager(element, ['stack']);
    cornerstoneTools.addToolState(element, 'stack', stack)
    },function(error){
      alert("Problem loading:"+stack.imageIds)
      throw error;
    })
  //load saved tool state
  if(tool_state){
    $(tool_state).each((index,state) => {
      if(state){
        cornerstoneTools.globalImageIdSpecificToolStateManager.restoreImageIdToolState(stack.imageIds[index],state)
        $(element).trigger("cornerstonetoolsmeasurementrestored", [stack.imageIds[index], element])
      }
    })
  }
  return promise
}


//save image data
function get_imgset_data(){
    const enabled_elements = cornerstone.getEnabledElements();
    imgset = []
    enabled_elements.forEach(function(element, index){
      let div_id = element.element.id
      stack = get_stack_data(div_id)
      if(stack){
        imgset.push(stack)
      }
    })

  return imgset
}

function get_stack_data(div_id){
  var element = document.getElementById(div_id)
  var viewport = cornerstone.getViewport(element)
  var enabled_element = cornerstone.getEnabledElement(element)
  var element_tool_state_manager = cornerstoneTools.getElementToolStateManager(element)

  if(viewport && enabled_element.image && $("#"+div_id).children().is(':visible')){
    var stack = {}
    stack["div_id"] = div_id
    image_ids = element_tool_state_manager.saveToolState().stack.data[0].imageIds
    stack["tool_state"] = image_ids.map((id) => cornerstoneTools.globalImageIdSpecificToolStateManager.saveImageIdToolState(id))
    image_ids = image_ids.map((id) => id.replace(/wadouri:/,""))
    url_list = image_ids[0].split("/")
    url_list.pop()
    stack["base_url"] = url_list.join("/") + "/"
    stack["image_names"] = image_ids.map((id) => id.split("/").pop())
    stack["name"] = $("#sel_" + div_id.split("_")[2] +" option:selected").text() || $("#vote_"+div_id.split("_")[2]).attr('name');
    stack["viewport"] = viewport
    return stack
  } else {
    return null
  }
}
