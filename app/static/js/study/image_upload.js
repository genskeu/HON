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
    var files = $('#file')[0].files;
    if(files.length == 0){
      $('#uploadStatus').html('No files selected.');
      return false
    }else if(files.length > 5000){
      $('#uploadStatus').html("More than 5000 files selected. Please don't upload more than 5000 files at once.");
      return false
    }

    //deactivate buttons
    var buttons = $(".btn,.btn-lg");
    buttons.each(function(index,button){
    $(button).prop('disabled', true);
    })


    // reset progressbar, etc
    $("#progress").width('0%');    
    $("#progress").html('0%');
    $('#uploadStatus').html('Uploading ' + files.length + ' file(s)...');
    $('#files_uploaded_saved').html("")
    $('#files_uploaded_not_saved').html("")
    $('#files_not_uploaded').html("")
    files_finished = 0
    chunk_size = 50
    //upload files and display progress
    file_chunks = []
    for(let i = 0;i < files.length;i=i+chunk_size){
      file_chunk = []
      for(let j = i; j<i+chunk_size; j++){
        if(j < files.length){
          file_chunk.push(files[j])
        }
      }
      file_chunks.push(file_chunk)
    }
    file_chunks.forEach((file_chunk) => upload_files(file_chunk,files.length,study_id))
  })
})


function upload_files(file_chunk,files_length,study_id){
  var url = "/upload_files/" + study_id    
  var fd = new FormData();
  file_chunk.forEach((file) => fd.append('file',file))
  $.ajax({
    url: url,
    type: 'post',
    data: fd,
    contentType: false,
    processData: false
    }).done(function(response){
      if(response["filenames_saved"].length){
        if($('#files_uploaded_saved').html()==""){
          $('#files_uploaded_saved').append('<p style="color:#28A74B;"> The following files have have been uploaded and saved:</p>')      
        }
        response["filenames_saved"].forEach((file) => $('#files_uploaded_saved').append('<p>' + file + '</p>'))
      }  
      if(response["filenames_not_saved"].length){
        if($('#files_uploaded_not_saved').html()==""){
          $('#files_uploaded_not_saved').append('<p style="color:#EA4335;"> The following files have have been uploaded but not saved:\
          (Either a file with a similar name was already present or the file has an incorrect file format, check the ending)</p>')      
        }
        response["filenames_not_saved"].forEach((file) => $('#files_uploaded_not_saved').append('<p>' + file + '</p>'))

      }
  }).fail(function(){
      if($('#files_not_uploaded').html()==""){
        $('#files_not_uploaded').append('<p style="color:#EA4335;"> File upload failed for the following files.\
                                                                    Please reload this page and try again.</p>')      
      }
      file_chunk.forEach((file) => $('#files_not_uploaded').append('<p>' + file.name + '</p>'))
      

  }).always(function(){
    files_finished = files_finished + file_chunk.length
    percentComplete = Number.parseFloat((files_finished / files_length) * 100).toFixed(2);
    $("#progress").width(percentComplete + '%');
    $("#progress").html(percentComplete + '%');

    if(files_length == files_finished){
      $('#files')[0].reset();
      $("#file").siblings(".custom-file-label").removeClass("selected").html("Choose files");
      $('#uploadStatus').html("Upload finished.")
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
      var buttons = $(".btn,.btn-lg");          
      buttons.each(function(index,button){
        $(button).prop('disabled', false);
      })
    }
  })
}

// delete selected files
$(document).ready(function(){
  $("#delete_files").click(function(){
    //deactivate buttons
    var buttons = $(".btn,.btn-lg");
      buttons.each(function(index,button){
        $(button).prop('disabled', true);
      })

    // loading animation
    $("#loader_anim_del").addClass("loader")
    $("#loader_text_del").text("Please wait")
    $("#files_del").fadeIn()
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
        $("#loader_text_del").text("Deletion finished.")
        $("#loader_text_del").fadeIn()
        $("#files_del").html('<p>The following files were deleted: ' + response["files_del"] + '</p>')
        if(response["files_not_del"].length){
          $("#files_not_del").fadeIn()
          $("#files_not_del").html('<p>The following files could not be deleted: ' + response["files_not_del"] + '</p>')
        }
      }).fail(function(){
        $("#loader_text_del").text("An error occurred!")
      }).always(function(){
        $("#loader_anim_del").removeClass("loader")
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


