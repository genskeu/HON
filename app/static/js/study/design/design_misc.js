//button to test overlap feature
$(document).ready(function(){
  $(".overlap").click(function(){
    id = this.id.match(/\d+$/)
    id = Number(id)
    div_id = cornerstone.getEnabledElements()[id].element.id
    image = get_img_data(div_id)
    $.ajax({
      type: 'POST',
      url: '/overlap',
      data: JSON.stringify(image),
      dataType: 'json',
      contentType: 'application/json; charset=utf-8',
      success: function(response) {
        alert(response)
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

//button to show preview of participant view
$(document).ready(function(){
  $("#participant_view").click(function(){
  })
})