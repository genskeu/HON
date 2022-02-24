function delete_result(study_id, user_id) {
    proceed = confirm("You are about to delete the results of user "  + user_id  + " from study " + study_id + "." )
    var url = "/result/" + study_id + "/" + user_id
    if(proceed){
      // loading animation
      $("#loader_anim_" + study_id).addClass("loader")
      $("#loader_text_" + study_id).fadeIn()
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
        $("#loader_text_" + study_id).text("Delete successful!")
          window.location = response.redirect
      }).fail(function(){
        $("#loader_text_" + study_id).text("An error occurred!")
      }).always(function(){
        $("#loader_anim_" + study_id).removeClass("loader")
        buttons.each(function (index, button) {
          $(button).prop('disabled', false);
        })
      });
    }
  }
  
  