var count = 0;
function addtodishlist() {
    var id = $(this).attr("id");
    var dishlist = $("#dishlist");
    var dishname = document.getElementById("dishname_" + id).innerHTML;
    var dishprice = document.getElementById("dishprice_" + id).innerHTML.trim();
    var html = "<tr id='dishitem_%d'><td><span class='glyphicon glyphicon-remove' id='del_%d'></span></td><td id='listitem_%d'>" + dishname + "</td><td>" + dishprice + "</td></tr>"
    var list_item = $(html.replace(/%d/g, id));
    var amountE = document.getElementById("totalsum")
    var amount = parseFloat(amountE.innerHTML.split(" ")[1])
    count = count + 1;
    console.log(amount)
    amountE.innerHTML = "$ " + (amount + parseFloat(dishprice.split(" ")[1])).toString()
    dishlist.append(list_item);
    document.getElementById(id).disabled = true;
}
function delfromdishlist() {
    var id = $(this).attr("id");
    var idnum = id.split("_")[1];

    var dishprice = parseFloat(document.getElementById("dishprice_" + idnum).innerHTML.trim().split(" ")[1]);
    var amountE = document.getElementById("totalsum")
    var amount = parseFloat(amountE.innerHTML.split(" ")[1])
    amountE.innerHTML = "$ " + (amount - dishprice).toString()
    count = count - 1;
    $("#dishitem_" + idnum).remove();
    document.getElementById(idnum).disabled = false;
}
function order() {
    var dishlist = $("#dishlist")
    var resName = document.getElementById("resName").innerHTML.trim()
    var amountE = document.getElementById("totalsum");
    var amount = parseFloat(amountE.innerHTML.split(" ")[1]);
    console.log("resname:" + resName);
    dishes = [];
    if (count != 0) {
        orderitemS = "<li> $" + amount + ":    ";
        dishlist.children().each(function (index) {
            var idnum = ($(this).attr("id")).split("_")[1];
            dishes.push(idnum);
            orderitemS = orderitemS + document.getElementById("listitem_" + idnum).innerHTML.trim() + " ";
            $(this).remove();
            document.getElementById(idnum).disabled = false;
        });
        $.post("/order", {dishes: dishes, res_name: resName, totalSum: amount})
            .done(function (data) {
                // $('#portfolioModal1').modal('toggle');

                orderitemS = (orderitemS + "</li>").trim();
                var orderitem = $(orderitemS);
                var myorder = $("#myorder");
                myorder.append(orderitem);
                amountE.innerHTML = "$ 0";
                count = 0;
            });
    }

    console.log(dishes);
    // First, clear the modal. Second, quit the modal
}

function res_joinmealevent() {
    var idnum = $(this).attr("id").split("_")[2]
    var joinBtn = $("#res_joineventbtn_" + idnum)
    console.log(joinBtn.text())
    console.log("idnum:" + idnum);
    if (joinBtn.text() == 'Quit') {
        $.post("/quitmealevent", {eventid: idnum})
            .done(function (data) {
                console.log("quitmeal");
                if ($("#curUsername").val() == document.getElementById("res_originatorname_" + idnum).innerHTML.trim()) {
                    var delevent = $("#res_event_" + idnum);
                    delevent.remove();
                    console.log("quit")
                }
                else {
                    console.log("quit");
                    joinBtn.text('Join');
                }
            });
    }
    else {
        console.log("joinmeal");
        $.post("/joinmealevent", {eventid: idnum})
            .done(function (data) {
                console.log("join")
                joinBtn.text('Quit');
            });
    }
}

$(document).ready(function () {
    $("#modal-menu").on("click", ".addbtn", addtodishlist);
    $("#modal-menu").on("click", ".glyphicon-remove", delfromdishlist);
    $("#order").click(order);
    $("#userEventList").on("click", ".joineventbtn", res_joinmealevent);
    console.log("hello");

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
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
});
