//activate tools after they have been selected in the dropdown menu
$(document).ready(function () {
    var old_tool;
    $(".tool_select").on("focus", function () {
        old_tool = $(this).val();
    }).change(function () {
        var new_tool = $(this).val();
        let mouse_btn = $(this).attr("data-mouseButtonMask")
        //disable and enable tools
        if(old_tool){
            cornerstoneTools.setToolDisabled(old_tool)
        }
        cornerstoneTools.setToolActive(new_tool, { mouseButtonMask: Number(mouse_btn) })
        //if annotation tool selected show rois menue
        if(new_tool.includes("Roi")){
            $("#roi_settings_container").show()
            $("#results_container").show()
        } else {
            $("#roi_settings_container").hide()
            $("#results_container").hide()
        }

        //redraw image to hide annotations created with other tools no longer active
        cornerstone.getEnabledElements().forEach(function (enabled_element) {
            if (enabled_element.image) {
                cornerstone.updateImage(enabled_element.element)
            }
        })
    })
})

// combine images to stacks, according to the naming scheme
$("document").ready(function () {
    $("#stack_mode").click(function () {
        var study_id = $("#content").attr("study_id");
        var group_info = "single_images"
        if ($("#stack_mode").val() == "Stackmode Off") {
            group_info = "stacks"
        }
        $.ajax({
            url: '/study/get_cs_stacks/'+study_id+'/'+group_info,
            type: 'GET',
            success: function (response) {
                    //set select menus to stacks
                    $(".sel_image,#ref_image_auto").each((index, sel) => {
                        $(sel).empty()
                        $(sel).append(new Option("", ""));
                        response["cs_stacks"].forEach((cs_stack) => {
                            op_temp = new Option(cs_stack["name"], cs_stack["image_ids"])
                            $(sel).append(op_temp);
                        })
                        $(sel).val("")
                        $(sel).change()
                    })

                    // change button
                    if ($("#stack_mode").val() == "Stackmode Off") {
                        $("#stack_mode").val("Stackmode On")
                        $("#stack_mode").removeClass("btn-danger")
                        $("#stack_mode").addClass("btn-success")
                    } else {
                        $("#stack_mode").val("Stackmode Off")
                        $("#stack_mode").removeClass("btn-success")
                        $("#stack_mode").addClass("btn-danger")
                    }
            },
            error: function(response) {
                alert("An unknown server error occurred")
              }
        })
    })
})
