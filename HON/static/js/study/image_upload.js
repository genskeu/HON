$(document).ready(function(){
  url = location.pathname.replace(/study./,"")
  $('#file').val("")
  $.ajax({
    url: url,
    type: 'GET',
    success: function(response){
      update_study_files(response)
    },
    error: function(response) {
      alert("An unknown server error occurred")
    } 
  });
})


function update_study_files(response){
    $("#file_list").empty();
    response["image_names"].sort().forEach(element => {
      $("#file_list").append("<tr>" + 
                              "<td style='width: 8%'>" + "<input type='checkBox' class='file' id=" + element + "></td>" +
                              "<td style='width: 42%'><label>" + element + "</label></td>" + 
                              "<td style='width: 42%'><label>" + element.split("_").slice(0,3).join("_") + "</label></td>" + 
                              "<td style='width: 8%'></td>" + 
                             "</tr>")
    });
    //activate buttons
    var buttons = $(".btn,.btn-lg");
      buttons.each(function(index,button){
        $(button).prop('disabled', false);
      })
}

// Add the following code if you want the name of the first file to appear on select (source W3Schools)
$(document).ready(function(){
  $(".custom-file-input").on("change", function() {
    var fileNames = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileNames);
    $("#progress_bars").empty()
  });
})

$(document).ready(function(){
  $("#upload_files").click(function(){
    url = location.pathname.replace(/study./,"")
    var files = $('#file')[0].files;
    
    for (let index = 0; index < files.length; index++) {
      //deactivate buttons
      var buttons = $(".btn,.btn-lg");
      buttons.each(function(index,button){
        $(button).prop('disabled', true);
      })
      var fd = new FormData();
      fd.append('file',files[index]);

      // code inspired by https://www.codexworld.com/file-upload-with-progress-bar-using-jquery-ajax-php/
      $.ajax({
          xhr: function() {
            var xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", function(evt) {
                if (evt.lengthComputable) {
                    var percentComplete = Number.parseFloat((evt.loaded / evt.total) * 100).toFixed(2);
                    $("#progress_" + index).width(percentComplete + '%');
                    $("#progress_" + index).html(percentComplete+'%');
                }
            }, false);
            return xhr;
          },
          url: url,
          type: 'post',
          data: fd,
          contentType: false,
          processData: false,
          beforeSend: function(){
            $("#progress_bars").append("<div class='col-12' id=uploadStatus_" + index + "></div>")
            $("#progress_bars").append("<div class='progress w-100'><div class='progress-bar' id=progress_" + index + "></div></div>")
            $("#progress_" + index).width('0%');

            $('#uploadStatus_'+index).html('Uploading: ' + files[index].name);
          },
          error:function(){
              $('#uploadStatus_'+index).html('<p style="color:#EA4335;">File upload failed, please try again.</p>');
          },
          success: function(response){
            if(response){
              $('#files')[0].reset();
              $("#file").siblings(".custom-file-label").removeClass("selected").html("Choose files");
              $('#uploadStatus_'+index).html('<p style="color:#28A74B;">' + response["file_names"] + ' has uploaded successfully!</p>');
            }else if(response == 'err'){
              $('#uploadStatus_'+index).html('<p style="color:#EA4335;">Please select a valid file to upload.</p>');
            }
            update_study_files(response)
          } 
    })      
    }
  })
})

$(document).ready(function(){
  $("#delete_files").click(function(){
    //deactivate buttons
    var buttons = $(".btn,.btn-lg");
      buttons.each(function(index,button){
        $(button).prop('disabled', true);
      })

    url = location.pathname.replace(/study./,"")
    var file_names = [];
    $(".file").each(function(index,file){
      if(file.checked){
        file_names.push(file.id);
      }
    })
    $.ajax({
        url: url,
        type: 'DELETE',
        data: JSON.stringify(file_names),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success: function(response){
          update_study_files(response)
        },
        error: function(response) {
          alert("An unknown server error occurred")
        } 
    });
  })
})

$(document).ready(function(){
  $("#select_files").click(function(){
    $(".file").each(function(index,file){
      file.checked = true
    })  
  })
})
$(document).ready(function(){
  $("#naming_btn").click(function(){
    event.preventDefault()
    if($("#naming").is(':visible')){
      $("#naming").fadeOut()
      document.getElementById("naming_btn").innerHTML = "&#9776";
    } else {
      $("#naming").fadeIn()
      document.getElementById("naming_btn").innerHTML = "&times;";
    }
  })
})

