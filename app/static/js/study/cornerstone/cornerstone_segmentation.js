$(document).ready(function() {
    $("#seg_label").change(function(){
        var seg = cornerstoneTools.getModule("segmentation")
        var elements = document.getElementsByClassName("dicom_img")
        for(i=0;i<elements.length;i++){
            if(cornerstone.getEnabledElement(elements[i]).image){
                seg.setters.activeSegmentIndex(elements[i],$(this).val())
            }
        }
    })
})

$(document).ready(function() {
    $("#brush_size").change(function(){
        var seg = cornerstoneTools.getModule("segmentation")
        seg.configuration.radius = $(this).val()
    })
})

$(document).ready(function() {
    $("#brush_size").val(10)
    $("#seg_label").val(1)
})