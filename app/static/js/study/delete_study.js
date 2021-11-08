function delete_study(name, id) {
  proceed = confirm("You are about to delete the following study: " + name + " (id = "+ id + ")." )
  var url = "/study/"+ id
  if(proceed){
    // loading animation
    $("#loader_anim_man").addClass("loader")
    $("#loader_text_man").fadeIn()
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
      $("#loader_text_man").text("Delete successful!")
       window.location = response.redirect
    }).fail(function(){
      $("#loader_text_man").text("An error occurred!")
    }).always(function(){
      $("#loader_anim_man").removeClass("loader")
      buttons.each(function (index, button) {
        $(button).prop('disabled', false);
      })
    });
  }
}

