$(document).ready(function(){
    $("#create_study").click(function(){
        //collect data
        data = {}
        data["title"] = $("#title").val()
        data["password"] = $("#password").val()
        data["description"] = $("#description").val()
        if(!data["title"] | !data["password"]){
            alert("Title and Password need to be defined!")
            return
        }
        // loading animation
        $("#loader_anim").addClass("loader")
        $("#loader_text").fadeIn()        
        var buttons = $(".btn");
        buttons.each(function (index, button) {
          $(button).prop('disabled', true);
        })        
        
        // ajax request
        $.ajax({
            url: "/study",
            type: 'POST',
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
          }).done(function(response){
            $("#loader_text").text("Study created successfully!")
            //show and update study setup navbar
            $("#study_setup_navbar").fadeIn()
            $("#nav_image_upload").attr("href",response["image_upload"])
            $("#nav_study_design").attr("href",response["study_design"])

          }).fail(function(response){
            $("#loader_text").text("An error occurred! " + response.responseJSON.error)
          }).always(function(){
            $("#loader_anim").removeClass("loader")
            buttons.each(function (index, button) {
              $(button).prop('disabled', false);
            })
          });
    })
})

$(document).ready(function(){
    $("#update_study").click(function(){
        id=$(this).data("study_id")
        //collect data
        data = {}
        data["title"] = $("#title").val()
        data["password"] = $("#password").val()
        data["description"] = $("#description").val()
        // loading animation
        $("#loader_anim").addClass("loader")
        $("#loader_text").fadeIn()        
        var buttons = $(".btn");
        buttons.each(function (index, button) {
          $(button).prop('disabled', true);
        })        
        
        // ajax request
        $.ajax({
            url: "/study/" + id,
            type: 'PUT',
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: 'application/json; charset=utf-8',
          }).done(function(response){
            $("#loader_text").text("Study updated successfully!")
          }).fail(function(response){
            $("#loader_text").text("An error occurred! " + response.responseJSON.error)
          }).always(function(){
            $("#loader_anim").removeClass("loader")
            buttons.each(function (index, button) {
              $(button).prop('disabled', false);
            })
          });
    })
})