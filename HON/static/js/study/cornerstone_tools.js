//activate after they have been selected in the dropdown menu
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

        //redraw image to hide annotations created with other tools no longer active
        cornerstone.getEnabledElements().forEach(function (enabled_element) {
            if (enabled_element.image) {
                cornerstone.updateImage(enabled_element.element)
            }
        })
    })
})

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