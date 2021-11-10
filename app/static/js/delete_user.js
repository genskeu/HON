function delete_user(name, id) {
  proceed = confirm("You are about to delete the following user: " + name + " (id = "+ id + ")." )
  var url = "/user/delete/"+ id
  if(proceed){
    // loading animation
    $("#loader_anim").addClass("loader")
    $("#loader_text").fadeIn()
    //disable buttons
    var buttons = $(".btn-danger");
    buttons.each(function (index, button) {
      $(button).prop('disabled', true);
    })

    // ajax request
    $.ajax({
      url: url,
      type: 'DELETE',
    }).done(function(response){
       window.location = response.redirect
       $("#loader_text").text("Delete successful!")
    }).fail(function(response){
      if(response.responseJSON.error){
        $("#loader_text").text(response.responseJSON.error)
      } else {
        $("#loader_text").text("An error occurred!")
      }
    }).always(function(){
      $("#loader_anim_man").removeClass("loader")
      buttons.each(function (index, button) {
        $(button).prop('disabled', false);
      })
    });
  }
}

