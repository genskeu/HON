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

        if(new_tool == "StackScrollMouseWheel" || new_tool == "StackScroll"){
            // add sync for stack scrolling
            var synchronizer = new cornerstoneTools.Synchronizer("cornerstonetoolsstackscroll", cornerstoneTools.stackScrollSynchronizer)
            cornerstone.getEnabledElements().forEach(function (enabled_element) {
                if (enabled_element.image) {
                    synchronizer.add(enabled_element.element);
                }
            })
            cornerstoneTools.setToolActive(new_tool, { mouseButtonMask: Number(mouse_btn), synchronizationContext: synchronizer })
        } else [
            cornerstoneTools.setToolActive(new_tool, { mouseButtonMask: Number(mouse_btn) })
        ]
        //if annotation tool selected show rois menue
        if(new_tool.includes("Roi")){
            $("#roi_settings_container").show()
            $("#results_container").show()
        } 
        if(new_tool.includes("Brush")){
            $("#seg_settings_container").show()
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

        //disable buttons
        var buttons = $(".btn");
        buttons.each(function (index, button) {
            $(button).prop('disabled', true);
        })
        // loading animation
        $("#loader_anim").addClass("loader")
        $("#loader_text").fadeIn()
        $.ajax({
            url: '/study/get_cs_stacks/'+study_id+'/'+group_info,
            type: 'GET'
        }).done(function(response){
            sel_options = []
            response["cs_stacks"].forEach((cs_stack) => {
                op_temp = new Option(cs_stack["name"], cs_stack["image_ids"])
                sel_options.push(op_temp);
            })
            //set select menus to stacks
            $(".sel_image,#ref_image_auto").each((index, sel) => {
                $(sel).empty()
                $(sel).append(new Option("", ""));
                sel_options.forEach((option) =>  $(sel).append( $(option).clone() ))
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
            $("#loader_anim").removeClass("loader")
            $("#loader_text").fadeOut()
        }).fail(function(response){
            $("#error_msg").fadeIn()
            $("#error_msg").append("<p>An unknown server error occurred</p>")
        }).always(function(){
            $("#loader_anim").removeClass("loader")
            $("#loader_text").fadeOut()
            //enable buttons
            var buttons = $(".btn");
            buttons.each(function (index, button) {
                $(button).prop('disabled', false);
            })
        })
    })
})

// when page is loaded 
$("document").ready(function () {
    $("#stack_mode").click()
})
