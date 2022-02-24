//add imgSet
$(document).ready(function () {
  $("#add_imgset, #insert_imgset").click(function () {
    // create url for request
    var study_id = $("#content").attr("study_id");
    var type = "POST"
    var url = "/study/imgset/" + study_id;
    
    // insert or append
    var imgset = $(".imgset_active")[0];
    if(imgset && this.id == "insert_imgset"){
      var position = Number(imgset.id.split("_")[1]);
    } else {
    //add to the end{
      var position = $(".imgset").length;
    }

    // get data
    var data = {}
    data["imgset"] = {};
    var imgset_data = get_imgset_data();
    if(imgset_data.length){
      data["imgset"]["stacks"] = imgset_data
    } else {
      return
    }
    data["imgset"]["position"] = position
    
    //loading anim
    $("#loader_anim").addClass("loader")
    $("#loader_text").fadeIn()
    //deactivate all other buttons to avoid conflicts/errors
    var buttons = $(".btn");
    buttons.each(function (index, button) {
      $(button).prop('disabled', true);
    })

    //request
    $.ajax({
      type: type,
      url: url,
      data: JSON.stringify(data),
      dataType: 'json',
      contentType: 'application/json; charset=utf-8'
    }).done(function(reponse){

    }).fail(function(){
      $("#error_msg").fadeIn()
      $("#error_msg").append("<p>An unknown server error occurred</p>")  
    }).always(function(){
      reload_sidebar(study_id,position)
    })
  });
});


//update imgSet
$(document).ready(function () {
  $("#upd_imgset").click(function () {
    // create url for request
    var study_id = $("#content").attr("study_id");
    var type = "PUT"
    // insert or append
    var imgset = $(".imgset_active")[0];
    if(imgset){
      var position = Number(imgset.id.split("_")[1]);
    } else {
      alert("No imgset selected.")
      return
    }
    var url = "/study/imgset/" + study_id + "/" + position;

    // get request data
    data = {};
    data["imgset"] = {};
    imgset_data = get_imgset_data();
    if(imgset_data.length){
      data["imgset"]["stacks"] = imgset_data
    } else {
      return
    }
    data["imgset"]["position"] = position
    $("#loader_anim").addClass("loader")
    $("#loader_text").fadeIn()

    //deactivate all other buttons to avoid conflicts/errors
    var buttons = $(".btn");
    buttons.each(function (index, button) {
      $(button).prop('disabled', true);
    })

    //request
    $.ajax({
      type: type,
      url: url,
      data: JSON.stringify(data),
      dataType: 'json',
      contentType: 'application/json; charset=utf-8'
    }).done(function(){
      $('#imgset_' + position).click()
    }).fail(function(){
      $("#error_msg").fadeIn()
      $("#error_msg").append("<p>An unknown server error occurred</p>")  
    }).always(function(){
      $("#loader_text").fadeOut()
      $("#loader_anim").removeClass("loader")
      //reactivate all buttons
      buttons.each(function(index,button){
        $(button).prop('disabled', false);
      })
    })
  });
});


//del imgset
$(document).ready(function () {
  $("#del_imgset").click(function () {
    // create url for request
    // either a imgset is selected or not
    var study_id = $("#content").attr("study_id");
    var type = "DELETE"
    var imgset = $(".imgset_active")[0];
    if(imgset){
      var position = Number(imgset.id.split("_")[1]);
    } else {
      alert("No imgset selected.")
      return
    }
    var url = "/study/imgset/" + study_id + "/" + position;

    $("#loader_anim").addClass("loader")
    $("#loader_text").fadeIn()

    //deactivate all other buttons to avoid conflicts/errors
    var buttons = $(".btn");
    buttons.each(function (index, button) {
      $(button).prop('disabled', true);
    })


    //request
    $.ajax({
      type: type,
      url: url,
      dataType: 'json',
      contentType: 'application/json; charset=utf-8',
    }).done(function(){

    }).fail(function(response){
      $("#error_msg").fadeIn()
      $("#error_msg").append("<p>" + response.responseJSON["error_msg"] + "</p>")  
    }).always(function(){
      reload_sidebar(study_id,position)
    })
  });
});


// after an imgset has been added the sidebar needs to be updated
function add_sidebar_entry(position, study_id) {
  $("#sidebar").append(
    '<div class="row">' +
    '<button class="imgset btn btn-light col-lg-12" id="imgset_' + position +
    '" action="/study/imgset/' + study_id + '/' + position + '">' +
    'Image Set ' + (position + 1) +
    '</button>' +
    '</div>'
  )
}

function reload_sidebar(study_id, active_position=null){
    //loading anim
    $("#loader_anim").addClass("loader")
    $("#loader_text").fadeIn()
    //deactivate all other buttons to avoid conflicts/errors
    var buttons = $(".btn");
    buttons.each(function (index, button) {
      $(button).prop('disabled', true);
    })
    $.ajax({
      type: 'GET',
      url: "/study/imgsets/" + study_id,
      dataType: 'json',
      contentType: 'application/json; charset=utf-8',
    }).done(function(response){
      $("#sidebar").empty();
      response["imgsets"].forEach(function (imgset) {
        add_sidebar_entry(imgset.position, imgset.study_id);
        $('#imgset_' + imgset.position).click(load_imgset_on_click);
      });
      if(active_position != null){
        $('#imgset_' + active_position).addClass("imgset_active");
        $('#imgset_' + active_position).click()
      }
      // show sidebar (navigation between imgsets) if closed
      var sidebar_width = $("#sidebar").width();
      if (sidebar_width == 0) {
        $("#sidebar_btn").click();
      };
    }).fail(function(){
      $("#error_msg").fadeIn()
      $("#error_msg").append("<p>An unknown server error occurred</p>")  
    }).always(function(){
      $("#loader_text").fadeOut()
      $("#loader_anim").removeClass("loader")
      //reactivate all buttons
      buttons.each(function(index,button){
        $(button).prop('disabled', false);
      })
    })
}



//del all imgsets
$(document).ready(function () {
  $("#del_all_imgsets").click(function () {

    var study_id = $("#content").attr("study_id");
    let url = "/study/imgsets/" + study_id

    //deactivate all other buttons to avoid conflicts/errors
    var buttons = $(".btn");
    buttons.each(function (index, button) {
      $(button).prop('disabled', true);
    })
    $("#loader_anim").addClass("loader")
    $("#loader_text").fadeIn()
    
    $.ajax({
      url: url,
      type: 'DELETE',
    }).done(function(){

    }).fail(function(response){
      $("#error_msg").fadeIn()
      $("#error_msg").append("<p>" + response.responseJSON["error_msg"] + "</p>")  
    }).always(function(){
      reload_sidebar(study_id)
    })
  })
})


//img sets
//image load on select (dropdown menu below images)
$(document).ready(function () {
  $(".sel_image").change(function () {
    var image_ids = $(this).val();
    var div_id = "dicom_img_" + this.id.split("_")[1]
    var study_id = $("#content").attr("study_id");
    if (image_ids) {
      // loading animation
      $("#loader_anim").addClass("loader")
      $("#loader_text").fadeIn()
      //disable buttons
      var buttons = $(".btn");
      buttons.each(function (index, button) {
        $(button).prop('disabled', true);
      })
      $.ajax({
        url: '/study/cs_stack/'+study_id+'/'+image_ids,
        type: 'GET',
      }).done(function(cs_stack){
          $.when($("#" + div_id).children().fadeOut()).done(function () {
            loadDicom(cs_stack, div_id = div_id, viewport = null, tool_state = null).then(function () {
              var element = document.getElementById(div_id)
              var viewport = cornerstone.getViewport(element)
              viewport = set_viewport_defaults(viewport)
              cornerstone.setViewport(element, viewport)
              $("#" + div_id).children().fadeIn()
              $("#" + div_id).trigger("ImageDisplayComplete");
            },function(){
              $("#" + div_id).trigger("ImageDisplayFailed");
            })
          })
          //special case if two ref images should be present
          if (this.id == "sel0" & $("#dicom_img_1").is(':visible')) {
            $("#sel1").val(image_ids).change()
          }
        }).fail(function(response){
          $("#error_msg").fadeIn()
          $("#error_msg").append("An unknown server error occurred")
        }).always(function(){
          $("#loader_text").fadeOut()
          $("#loader_anim").removeClass("loader")
          //reactivate all buttons
          buttons.each(function(index,button){
            $(button).prop('disabled', false);
          })
        })
    } else {
      $("#" + div_id).children().fadeOut()
      $("#" + div_id).trigger("ImageDisplayFailed");
    }
  }
  )
})

// viewport defaults can be defined via the viewport menu
// function needed to apply defaults before images are loaded
function set_viewport_defaults(viewport) {
  var ww = $("#def_ww").val()
  var wc = $("#def_wc").val()
  var zoom = $("#def_zoom").val()
  var pos_x = $("#def_pos_x").val()
  var pos_y = $("#def_pos_y").val()

    if(ww != ""){
      viewport.voi.windowWidth = Number(ww.match(/-*\d+/)[0])
    }
    if(wc != ""){
      viewport.voi.windowCenter = Number(wc.match(/-*\d+/)[0])
    }
    if(zoom != ""){
      viewport.scale = Number(zoom.match(/\d+\.*\d*/)[0])
    }
    if(pos_x != ""){
      viewport.translation.x = Number(pos_x.match(/-*\d+\.*\d*/)[0])
    }
    if(pos_y != ""){
      viewport.translation.y = Number(pos_y.match(/-*\d+\.*\d*/)[0])
    }
    return viewport
  }