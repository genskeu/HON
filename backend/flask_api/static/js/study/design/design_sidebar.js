//sidebar
//button to open and close sidebar
function openClose_sidebar() {
  hidden = $("#sidebar").is(":hidden")

  if (hidden) {
    $("#sidebar").fadeIn();
    document.getElementById("sidebar_btn").innerHTML = "Image-Sets &times;";
  }
  else {
    $("#sidebar").fadeOut();
    document.getElementById("sidebar_btn").innerHTML = "Image-Sets &#9776;";
  }
}

//click event function sidebar buttons
//load imgset after click event
$(document).ready(function () {
  $(".imgset").click(load_imgset_on_click)
})

function load_imgset_on_click() {
  // tool display properties
  cornerstoneTools.toolColors.setToolColor("green")
  cornerstoneTools.toolColors.setActiveColor("green")
  cornerstoneTools.toolStyle.setToolWidth(3)
  // set action attr reset button
  $(".reset").attr("value", $(this).attr("action"))

  // loading animation
  $("#loader_anim").addClass("loader")
  $("#loader_text").fadeIn()
  //disable buttons
  var buttons = $(".btn");
  buttons.each(function (index, button) {
    $(button).prop('disabled', true);
  })

  //get imgset 
  $.getJSON($(this).attr("action"), function (response) {
    var image_stacks = response.imgset.image_stacks
    var promises = []
    //load images
    $.when($(".dicom_img").children().fadeOut()).done(function () {
      $(".sel_image").val("")
      image_stacks.forEach(function(image_stack) {
        promises.push(loadDicom(
          image_stack["cs_stack"],
          image_stack["div_id"],
          image_stack["viewport"],
          image_stack["tool_state"],
          image_stack["seg_data"]
          ))       
      })
      
      // after all images have been loaded   
      Promise.all(promises).then(function () {
        image_stacks.forEach(function (image_stack) {
          //select image name from dropdown menues
          $("#sel_" + image_stack["div_id"].split("_")[2] + " option").filter(function() {
            return $(this).text() == image_stack["name"];
          }).prop('selected', true); 
          
          //fade images in
          $("#" + image_stack["div_id"]).children().fadeIn()
        })
      }).catch(function(){
        //error in loading images
      })
    })
    //set selected imgset active (green)
    index = response.imgset.position
    $(".imgset_active").removeClass("imgset_active");
    $('#imgset_' + index).addClass("imgset_active");
  
  }).done(function(response){
    //update results section
    $.getJSON("/get_results_by_imgset_id/" + response.imgset.id, function (response) {
      $("#results").empty()
      response.results.forEach(function(result){
      let entry = '<div class="row mx-auto">\
                    <button class="result_btn btn btn-light col-12"' + 'id="result_' + result.id + '" action="/result/' + result.id + '">\
                      User ' + result.username + '\
                    </button>\
                  </div>'
      $("#results").append(entry)
      $("#result_" + result.id).click(load_result)
      })
    }).done(function(){

    }).fail(function(){

    }).always(function(){

    })
  
  }).fail(function(){
  
  }).always(function(){
    // loading animation
    $("#loader_anim").removeClass("loader")
    $("#loader_text").fadeOut()
    //enable buttons
    var buttons = $(".btn");
    buttons.each(function (index, button) {
      $(button).prop('disabled', false);
    })
  })
}

//load result image-set on click (right sidebar buttons)
function load_result(){
  // tool display properties
  cornerstoneTools.toolColors.setToolColor("blue")
  cornerstoneTools.toolColors.setActiveColor("blue")
  cornerstoneTools.toolStyle.setToolWidth(3)
  $(".result_btn").removeClass("result_active");
  //get selected image_stack 
  $.getJSON($(this).attr("action"), function (response) {
    var image_stack = response.result.stack_picked
    //load images
    $.when($("#" + image_stack["div_id"]).children().fadeOut()).done(function () {
        loadDicom(
          image_stack["cs_stack"],
          image_stack["div_id"],
          image_stack["viewport"],
          image_stack["tool_state"],
          ).then(function(){
            $("#" + image_stack["div_id"]).children().fadeIn()
          })      
    })
  })
  //set selected result active (blue)
  $(this).addClass("result_active"); 
} 