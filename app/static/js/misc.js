function delete_db_entry(type, name, id) {
  if(type == "result"){
    proceed = confirm("You are about to delete the following " + type +" from study: " + name + " (user id =" + id + ")." )
    var url = "/" + type + "/" + name + "/" + id
  } else {
    proceed = confirm("You are about to delete the following " + type +": " + name + " (id = "+ id + ")." )
    var url = "/" + type + "/" + id
  }
  if(proceed){
    $.ajax({
      url: url,
      type: 'DELETE',
      success: function(response) {
        window.location = response.redirect
      }
    });
  }
}

