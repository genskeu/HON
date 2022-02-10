//load images
function loadDicom(stack,div_id,viewport=null,tool_state=null,seg_data=null){
  //where to display
  const element = document.getElementById(div_id)
  // reset tool data
  cornerstoneTools.globalImageIdSpecificToolStateManager.clear(element)
  var segmentation = cornerstoneTools.getModule("segmentation") 
  segmentation.state.series = {}
  // empty roi containers
  id = div_id.match(/\d+/)[0]
  $("#rois_img_" + id).find(".roi_pos").remove()
  // load and display specified image
  const promise = cornerstone.loadAndCacheImage(stack.imageIds[stack.currentImageIdIndex]).then(function(image) {
    // preload entire stack (performance issues big stacks)
    if(stack.imageIds.length < 100){
      stack.imageIds.map(imageId => cornerstone.loadAndCacheImage(imageId))
    }
    if(!viewport){
      viewport = cornerstone.getDefaultViewportForImage(element,image)
    }
    cornerstone.displayImage(element, image, viewport)
    cornerstoneTools.addStackStateManager(element, ['stack']);
    cornerstoneTools.addToolState(element, 'stack', stack)
    },function(error){
      $("#error_msg").fadeIn()
      $("#error_msg").append("<p>" + "Problem loading:"+stack.imageIds + "</p>")
      throw error;
    }).then(function() {
      //load saved tool state
      if(tool_state){
        $(tool_state).each((index,state) => {
          if(state){
            cornerstoneTools.globalImageIdSpecificToolStateManager.restoreImageIdToolState(stack.imageIds[index],state)
            $(element).trigger("cornerstonetoolsmeasurementrestored", [stack.imageIds[index], element])
          }
        })
      }
      //load saved seg state
      if(seg_data){
        seg_data = JSON.parse(seg_data)
        segmentation.setters.activeLabelmapIndex(element,0)
        labelmap3D = segmentation.getters.labelmap3D(element,0)
        labelmap3D.labelmaps2D = Array(seg_data.length)
        seg_data.forEach(function(seg,index){
          if(seg){
            l2dforImageIdIndex = {pixelData : Uint16Array.from(seg),segmentsOnLabelmap : [0,1]  }
            labelmap3D.labelmaps2D.splice(index,0,l2dforImageIdIndex)
          }
        })
      }
    })        
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
  const element = document.getElementById(div_id)
  const viewport = cornerstone.getViewport(element)
  const enabled_element = cornerstone.getEnabledElement(element)
  const element_tool_state_manager = cornerstoneTools.getElementToolStateManager(element)
  const image = cornerstone.getImage(element)
  
  
  if(viewport && enabled_element.image && $("#"+div_id).children().is(':visible')){
    var stack = {}
    stack["div_id"] = div_id
    image_ids = element_tool_state_manager.saveToolState().stack.data[0].imageIds
    stack["tool_state"] = image_ids.map((id) => cornerstoneTools.globalImageIdSpecificToolStateManager.saveImageIdToolState(id))
    stack["segmentation_data"] = get_seg_data(image_ids, image.rows, image.columns)    
    image_ids = image_ids.map((id) => id.replace(/wadouri:/,""))
    url_list = image_ids[0].split("/")
    url_list.pop()
    stack["base_url"] = url_list.join("/") + "/"
    stack["image_names"] = image_ids.map((id) => id.split("/").pop())
    stack["name"] = $("#sel_" + div_id.split("_")[2] +" option:selected").text() || $("#vote_"+div_id.split("_")[2]).attr('name');
    if(!stack["name"]){
      alert("Stack name not specified. Ensure there is a name displayed in the select menu below each image.")
      return
    }
    stack["viewport"] = viewport
    return stack
  } else {
    return null
  }
}

function get_seg_data(image_ids_stack, rows, cols){
  const segmentation_data = cornerstoneTools.getModule("segmentation").state.series
  const seg_ids = Object.keys(segmentation_data)
  var seg_arrays = null
  // seg series are identified via the first image within a stack
  const id = image_ids_stack[0]
  // what to do when id is present multiple times in seg_ids (e.g. multiple image viewer with same stack?)
  if(seg_ids.includes(id)){
    seg_arrays = []
    // only working with one segmentation 3D map for now
    labelmaps2D = segmentation_data[id].labelmaps3D[0].labelmaps2D
    for(i=0;i<image_ids_stack.length;i++){
      seg_arrays.push(labelmaps2D[i] ? Array.from(labelmaps2D[i].pixelData) : undefined)
    }
    seg_arrays.push([rows,cols])
    seg_arrays = JSON.stringify(seg_arrays)
  }
  return seg_arrays
}