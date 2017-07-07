/**
 * Created by yuxingchen on 11/19/16.
 */
function joinGroup() {
    var id = $(this).attr("id");
    var idnum = id.split("_")[1];
    var countE = document.getElementById("membercount")
    var count = parseInt(countE.innerHTML.trim());
    console.log($(this).text().trim())
    if ($(this).text().trim()=='Quit') {
        $.post("/quitgroup", {id: idnum})
        .done(function(data){
            countE.innerHTML=(count-1).toString();
        });
        $(this).text('Join');
    }
    else {
        $.post("/joingroup", {id: idnum})
        .done(function(data){
            countE.innerHTML=(count+1).toString();
        });
        $(this).text('Quit');
    }
}

$(document).ready(function() {
    $(document).on("click",".joinbtn",joinGroup);
    
    // $(document).on("click",".unjoinbtn",quitGroup);
    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });

});