//add or update imgSet
$(document).ready(function () {
  $("#add_imgset,#upd_imgset,#insert_imgset,#del_imgset").click(function () {
    start = Math.floor(Date.now() / 1000)
    // create url for request
    // either a imgset is selected or not
    var study_id = $("#content").attr("study_id");

    // insert or update
    if (this.id != "add_imgset") {
      try{
        $(".imgset_active")[0]
        var imgset = $(".imgset_active")[0];
        var position = Number(imgset.id.split("_")[1]);
      } catch {
        alert("No imgset selected.")
        return
      }
    //add to the end
    } else {
      var position = $(".imgset").length;

    }

    if (this.id == "add_imgset" || this.id == "insert_imgset") {
      var type = "POST"
      var url = "/study/imgset/" + study_id;
    } else if(this.id == "del_imgset") {
      var type = "DELETE"
      var url = "/study/imgset/" + study_id + "/" + position;
    } else {
      var type = "PUT"
      var url = "/study/imgset/" + study_id + "/" + position;
    }

    // get request data
    var imgset = {};
    data = {};
    data["button"] = this.id;
    data["imgset"] = {};
    data["imgset"]["stacks"] = get_imgset_data();
    data["imgset"]["position"] = position
    $("#loader_anim_man").addClass("loader")
    $("#loader_text_man").fadeIn()

    //deactivate all other buttons to avoid conflicts/errors
    var buttons = $(".imgset_btn");
    buttons.each(function (index, button) {
      $(button).prop('disabled', true);
    })


    //request
    $.ajax({
      type: type,
      url: url,
      data: JSON.stringify(data),
      dataType: 'json',
      contentType: 'application/json; charset=utf-8',
      success: function () {
        $.ajax({
          type: 'GET',
          url: "/study/imgsets/" + study_id,
          dataType: 'json',
          contentType: 'application/json; charset=utf-8',
          success: function (response) {
            //on success reload sidebar entries
            $("#sidebar").empty();
            response["imgsets"].forEach(function (imgset) {
              add_sidebar_entry(imgset.position, imgset.study_id);
              $('#imgset_' + imgset.position).click(load_imgset_on_click);
            });
            $('#imgset_' + position).addClass("imgset_active");
            $('#imgset_' + position).click()
            // show sidebar (navigation between imgsets) if closed
            var sidebar_width = $("#sidebar").width();
            if (sidebar_width == 0) {
              $("#sidebar_btn").click();
            };
            //reactivate all buttons
            buttons.each(function (index, button) {
              $(button).prop('disabled', false);
            })
            $("#loader_text_man").fadeOut()
            $("#loader_anim_man").removeClass("loader")
            console.log(Math.floor(Date.now() / 1000) - start)

          },
          error: function(response) {
            alert("An unknown server error occurred")
            //reactivate all buttons
            buttons.each(function(index,button){
              $(button).prop('disabled', false);
            })
            $("#loader_text_auto").fadeOut()
            $("#loader_anim_auto").removeClass("loader")
          }
        })
      }
    });
  });
});

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


//del all imgsets
$(document).ready(function () {
  $("#del_all_imgsets").click(function () {
    start = Math.floor(Date.now() / 1000)
    //deactivate all other buttons to avoid conflicts/errors
    var buttons = $(".imgset_btn");
    buttons.each(function (index, button) {
      $(button).prop('disabled', true);
    })
    var study_id = $("#content").attr("study_id");
    let url = "/study/imgsets/" + study_id

    $("#loader_anim_man").addClass("loader")
    $("#loader_text_man").fadeIn()
    $.ajax({
      url: url,
      type: 'DELETE',
      success: function (response) {
        //on success reload sidebar entries
        $("#sidebar").empty();
        response["imgsets"].forEach(function (imgset) {
          add_sidebar_entry(imgset.position, imgset.study_id);
          $('#imgset_' + imgset.position).click(load_imgset_on_click);
        });
        // show sidebar (navigation between imgsets) if closed
        var sidebar_width = $("#sidebar").width();
        if (sidebar_width == 0) {
          $("#sidebar_btn").click()
        };
        //reactivate all buttons
        buttons.each(function (index, button) {
          $(button).prop('disabled', false);
        });
        $("#loader_text_man").fadeOut()
        $("#loader_anim_man").removeClass("loader")
        console.log(Math.floor(Date.now() / 1000) - start)
      },
      error: function(response) {
        alert("An unknown server error occurred")
        //reactivate all buttons
        buttons.each(function(index,button){
          $(button).prop('disabled', false);
        })
        $("#loader_text_auto").fadeOut()
        $("#loader_anim_auto").removeClass("loader")
      }
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
      $.ajax({
        url: '/study/cs_stack/'+study_id+'/'+image_ids,
        type: 'GET',
        success: function (cs_stack) {
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
        },
        error: function(response) {
          alert("An unknown server error occurred")
          //reactivate all buttons
          buttons.each(function(index,button){
            $(button).prop('disabled', false);
          })
          $("#loader_text_auto").fadeOut()
          $("#loader_anim_auto").removeClass("loader")
        }
      })
    } else {
      $("#" + div_id).children().fadeOut()
      $("#" + div_id).trigger("ImageDisplayFailed");
    }
  }
  )
})

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



//shuffle button to shuffle the options of the select dropdown menue
//shuffle HTMLoptionscollection (idea from https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array)
function shuffle(HTMLoptionscollection) {
  var currentIndex = HTMLoptionscollection.length, temporaryValue, randomIndex;
  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue1 = HTMLoptionscollection[currentIndex];
    temporaryValue2 = HTMLoptionscollection[randomIndex];
    HTMLoptionscollection[currentIndex] = new Option(temporaryValue2.text, temporaryValue2.value)
    HTMLoptionscollection[randomIndex] = new Option(temporaryValue1.text, temporaryValue1.value);
  }

  return HTMLoptionscollection;
}

function shuffleOptions() {
  //get and shuffle Options
  var sel0 = document.getElementById("sel0")
  //remove none selection
  var noneOption = sel0.options[0]
  sel0.options[0].remove()
  shuffle(sel0.options)
  sel0.options.add(noneOption, 0)

  //copy shuffled options to all sel
  var selIds = ["sel1", "sel2", "sel3", "sel4", "sel5"]
  selIds.forEach(function (sel) {
    var sel = document.getElementById(sel)
    sel.innerHTML = sel0.innerHTML
  })
}

//shuffle
$(document).ready(function () {
  $("#shuffleSel").click(function () {
    shuffleOptions()
  })
})


$(document).ready(function(){
  $("#randomize_imgsets").click(function(){
      study_id = $("#content").attr("study_id");
      $.ajax({
        type: 'POST',
        url: "/study/"+study_id+"/randomize",
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
          $("#sidebar").empty()
          imgsets = response["imgsets"]
          imgsets.forEach(function(imgset){
            add_sidebar_entry(imgset.position,imgset.study_id)
            $('#imgset_'+imgset.position).click(load_imgset_on_click)
          })
          if(response["error"]){
            alert(response["error"])
          }
          $('#imgset_'+0).addClass("imgset_active");
          $('#imgset_'+0).click()
          // show sidebar (navigation between imgsets) if closed
          var sidebar_width = $("#sidebar").width();
          if(sidebar_width == 0){
            $("#sidebar_btn").click();
          };
          //reactivate all buttons
          buttons.each(function(index,button){
            $(button).prop('disabled', false);
          })
          $("#loader_text_auto").fadeOut()
          $("#loader_anim_auto").removeClass("loader")
        },
        error: function(response) {
          alert("An unknown server error occurred")
          //reactivate all buttons
          buttons.each(function(index,button){
            $(button).prop('disabled', false);
          })
          $("#loader_text_auto").fadeOut()
          $("#loader_anim_auto").removeClass("loader")
        }
    })
  })
})
