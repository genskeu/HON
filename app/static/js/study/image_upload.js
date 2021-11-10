// get list of uploaded files
$(document).ready(function(){
  study_id = location.pathname.match(/\d+/)[0]
  url = "/get_filenames/" + study_id
  $.ajax({
    url: url,
    type: 'GET'
  }).done(function(response){
      update_study_files(response)
  }).fail(function(){
      alert("An unknown server error occurred")
  }).always(function(){
  })
});

// after fileupload, del .... update the list of files already uploaded
function update_study_files(response){
    $("#file_list").empty();
    response["filenames_db"].sort().forEach(element => {
      $("#file_list").append("<tr>" + 
                              "<td style='width: 8%'>" + "<input type='checkBox' class='file' id=" + element + "></td>" +
                              "<td style='width: 42%'><label>" + element + "</label></td>" + 
                              "<td style='width: 42%'><label>" + element.split("_").slice(0,3).join("_") + "</label></td>" + 
                              "<td style='width: 8%'></td>" + 
                             "</tr>")
    });
}

// Add the following code if you want the name of the first file to appear on select (source W3Schools)
$(document).ready(function(){
  $(".custom-file-input").on("change", function() {
    var fileNames = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileNames);
  });
})


// upload files
$(document).ready(function(){
  $("#upload_files").click(function(){
    //get request data
    var study_id = location.pathname.match(/\d+/)[0]
    var url = "/upload_files/" + study_id    
    var files = $('#file')[0].files;
    if(files.length == 0){
      $('#uploadStatus').html('No files selected.');
      return false
    }

    //deactivate buttons
    var buttons = $(".btn,.btn-lg");
    buttons.each(function(index,button){
    $(button).prop('disabled', true);
    })

    //upload files and display progress
    var fd = new FormData();
    $(files).each(function(index){
      fd.append('file',files[index]);
    }) 
    // code inspired by https://www.codexworld.com/file-upload-with-progress-bar-using-jquery-ajax-php/
    $.ajax({
      xhr: function() {
        var xhr = new window.XMLHttpRequest();
        xhr.upload.addEventListener("progress", function(evt) {
          if (evt.lengthComputable) {
            var percentComplete = Number.parseFloat((evt.loaded / evt.total) * 100).toFixed(2);
            $("#progress").width(percentComplete + '%');
            $("#progress").html(percentComplete+'%');
          }
        }, false );
        return xhr;
      },
      url: url,
      type: 'post',
      data: fd,
      contentType: false,
      processData: false,
      beforeSend: function(){
        $("#progress").width('0%');
        $('#uploadStatus').html('Uploading ' + files.length + ' file(s)...');
        $('#files_uploaded').html("")
        $('#files_not_uploaded').html("")
      }
    }).done(function(response){
        update_study_files(response)
        $('#files')[0].reset();
        $("#file").siblings(".custom-file-label").removeClass("selected").html("Choose files");
        $('#uploadStatus').html("Upload finished.")
        $('#files_uploaded').html('<p style="color:#28A74B;">  The following files have been uploaded successfully:'  + response["filenames_saved"] + '</p>');
        if(response["filenames_not_saved"].length){
          $('#files_not_uploaded').html('<p style="color:#EA4335;"> The following files have have not been uploaded: (Either a file with a similar name was already present or the file has an incorrect file format, check the ending) ' + response["filenames_not_saved"] + '</p>');
        }
    }).fail(function(){
      $('#uploadStatus').html('<p style="color:#EA4335;">File upload failed, please try again.</p>');
    }).always(function(response){
      buttons.each(function(index,button){
        $(button).prop('disabled', false);
        })
    })
  })
})



// delete selected files
$(document).ready(function(){
  $("#delete_files").click(function(){
    //deactivate buttons
    var buttons = $(".btn,.btn-lg");
      buttons.each(function(index,button){
        $(button).prop('disabled', true);
      })

    // loading animation
    $("#loader_anim_man").addClass("loader")
    $("#loader_text_man").fadeIn()
    $("#loader_text_man").text("Please wait")

    var study_id = location.pathname.match(/\d+/)[0]
    var url = "/delete_files/" + study_id        
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
        contentType: 'application/json; charset=utf-8'
      }).done(function(response){
        update_study_files(response)
        $("#loader_text_man").text("Files deleted!")
      }).fail(function(){
        $("#loader_text_man").text("An error occurred!")
      }).always(function(){
        $("#loader_anim_man").removeClass("loader")
        //activate buttons
        var buttons = $(".btn,.btn-lg");
        buttons.each(function(index,button){
            $(button).prop('disabled', false);
      })
    })
  });
})

// select all files already uploaded for del
$(document).ready(function(){
  $("#select_files").click(function(){
    $(".file").each(function(index,file){
      file.checked = true
    })  
  })
})


