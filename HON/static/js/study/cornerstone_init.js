//register web image Loader
cornerstoneWebImageLoader.external.cornerstone = cornerstone;

//register WADO image Loader
cornerstoneWADOImageLoader.external.cornerstone = cornerstone;

//Init CornerstoneTools and add "buttons" to navbar
cornerstoneTools.external.cornerstone = cornerstone;
cornerstoneTools.external.Hammer = Hammer;
cornerstoneTools.external.cornerstoneMath = cornerstoneMath;
cornerstoneTools.init()

//initalize cornerstone
$(document).ready(function(){
  prepare_elements()
})

function prepare_elements(){
  var elements = document.getElementsByClassName("dicom_img")
  for(i=0;i<elements.length;i++){
    //activate elements for cornerstone
    cornerstone.disable(elements[i])
    cornerstone.enable(elements[i])

    //collect cornerstone tools to activate
    var tools = []
    $(".tool_select option:enabled").each(function(index,option){
      if(option.value && !tools.includes(option.value)){
        tools.push(option.value)
      }
    })
    $("#tools").val("")
    //add tools present in select menu
    if(tools){
      tools.forEach(function(element){
        var tool_name = element+"Tool"
        var tool = cornerstoneTools[tool_name]
        cornerstoneTools.addToolForElement(elements[i],tool);
      })
    }

    //display ww,wc,pos,zoom
    elements[i].addEventListener('cornerstoneimagerendered', onImageRendered);
    // Observe one or multiple elements
    //resizing
    var ro = new ResizeObserver(entries => {
      for (let entry of entries) {
        cornerstone.resize(entry.target)
      }
    });
    ro.observe(elements[i]);
  }
}

// function to display viewport setting: zoom, pos and ww/wc and size of window
function onImageRendered(e) {
  if(e.target.className.includes("dicom_img")){
    var id = e.target.id.split("_")[2]
  } else {
    return
  }
  const eventData = e.detail;
  const stack_pos = cornerstoneTools.getElementToolStateManager(eventData.element).saveToolState().stack.data[0].currentImageIdIndex
  const stack_size = cornerstoneTools.getElementToolStateManager(eventData.element).saveToolState().stack.data[0].imageIds.length
  // viewport
  if(document.getElementById("viewport_info_" + id)){
      //info overlay
      $("#stack_info_"+id).text("Stack: " + (stack_pos+1)+"/"+stack_size)
      $("#ww_wc_info_"+id).text("WW/WC: " + Number.parseFloat(eventData.viewport.voi.windowWidth).toFixed(0) + "/" + Number.parseFloat(eventData.viewport.voi.windowCenter).toFixed(0))
      $("#zoom_info_"+id).text("Zoom: " + Number.parseFloat(eventData.viewport.scale).toFixed(2))
      $("#position_info_"+id).text("Pos: " + Number.parseFloat(eventData.viewport.translation.x).toFixed(0)+"/"+Number.parseFloat(eventData.viewport.translation.y).toFixed(0))
      //input fields
      document.getElementById("ww_" + id).value =
        Math.round(eventData.viewport.voi.windowWidth).toFixed(0);
      document.getElementById("wc_" + id).value =
        Math.round(eventData.viewport.voi.windowCenter).toFixed(0);

      document.getElementById("zoom_" + id).value =
        Number.parseFloat(eventData.viewport.scale).toFixed(2) ;

      document.getElementById("pos_x_" + id).value =
        Number.parseFloat(eventData.viewport.translation.x).toFixed(0)
      document.getElementById("pos_y_" + id).value =
        Number.parseFloat(eventData.viewport.translation.y).toFixed(0)
  }
}





