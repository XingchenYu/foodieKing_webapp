function adddish(evt) {	 
	evt.preventDefault();
	var formData = new FormData($(this)[0]); 
	$.ajax({
		url: 'adddish',
		type: 'POST',
		data: formData,
		async: true,
		cache: false,
		contentType: false,
		enctype: 'multipart/form-data',
		processData: false,
		success: function (data) {
			if(data['errors'].length!=0) {
                    errorJson = data['errors'].replace(/&quot;/g,'\"');
                    errorJson = JSON.parse(errorJson)
                    var errorString=""
                    for (var item in errorJson) {
                    	errorString = errorString+"<li>"+item+": "+errorJson[item]+"</li>";
                    }
                    console.log(errorString);
                    var error = $(errorString);
                    $("#adddish_errors").append(error);
            } 
            else {
				console.log("success add new dish")
				var dishName = $("#dishName")
				console.log("dishName"+dishName)
				var isspec = $("#dishIsSpec");
				console.log(isspec.val());
				var source=$("#dishSource")
				var price=$("#dishPrice")
				var type=$("#dishType")
				var pungency=$("#dishPungency")
				var dishList = $("#dishList")
				var dishItem = $("<div class='col-lg-6'><div class='service1' id='dishdiv_"+data.id+"'><div class='icon-holder1'>" +
						"<img src=\"/getdishphoto/"+ dishName.val() +"\" class='img-responsive icon' alt='portrait'></div>"+
			            "<h4 class='heading1' id='dishname_"+ data.id+"'>"+ dishName.val()+"</h4>"+
			            "<p class='description1' id='dishsource_"+data.id+"'>"+source.val()+"</p>"+
			            "<p class='description1' id='dishprice_"+ data.id+"'>$ "+ price.val()+"</p>"+
			            "<button type='button' class='btn btn-default addbtn description1' id='delbtn_"+data.id+"'>Delete</button></div></div>");
			    dishList.append(dishItem);
			    dishName.val("");
			    isspec.val("1");
			    source.val("");
			    price.val("");
			    type.val("");
			    pungency.val("");
			}
		}
	});
	
	return false;
}
function deletedish() {
	var idnum = $(this).attr('id').split('_')[1]
	$.post('deletedish',{id:idnum})
	.done(function(data){
		console.log("successfully delete");
		var delItem = $("#dishdiv_"+idnum);
		delItem.remove()
	});
}

function finishorder() {
	var idnum = $(this).attr('id').split('_')[1]
	$.post('finishorder',{id:idnum})
	.done(function(data){
		var delItem = $("#order_"+idnum);
		delItem.remove();
	});
}

function delete_groupbuy() {
	console.log("delete_groupbuy");
	var idnum = $(this).attr('id').split('_')[1];
	$.post('delete_groupbuy',{id:idnum})
		.done(function(data){
			var delItem = $("#groupbuy_div_"+idnum);
			delItem.remove()
		});
}


$(document).ready(function() {
	
	$("#addDishForm").on('submit', adddish);
	$("#dishList").on('click','button',deletedish);
	$("#groupbuyList").on('click','button',delete_groupbuy);
	$("#res_orderlist").on('click','button',finishorder);
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
