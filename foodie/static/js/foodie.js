var map;
var missionList = [];
var allMyMarkers = [];
var groupbuyMarkers = [];


function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: {lat: 40.4435, lng: -79.9435},
        zoom: 16
    });
    var pos;
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            // Set a marker at current location
            var marker = new google.maps.Marker({
                position: pos,
                map: map,
                title: 'Hello World'
            });
            map.setCenter(pos);
        }, function () {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }
}


/* --------Change bubble's appearance to originator's photo ---------- */

//adapted from http://gmaps-samples-v3.googlecode.com/svn/trunk/overlayview/custommarker.html
function CustomMarker(latlng, map, imageSrc, args) {
    this.latlng_ = latlng;
    this.imageSrc = imageSrc;
    // Once the LatLng and text are set, add the overlay to the map.  This will
    // trigger a call to panes_changed which should in turn call draw.
    this.setMap(map);
    this.args = args;
}

CustomMarker.prototype = new google.maps.OverlayView();

CustomMarker.prototype.draw = function () {
    // Check if the div has been created.
    var div = this.div_;
    if (!div) {
        // Create a overlay text DIV
        div = this.div_ = document.createElement('div');
        // Create the DIV representing our CustomMarker
        div.className = "customMarker";
        div.id = this.args.marker_id;
        var img = document.createElement("img");
        img.src = this.imageSrc;
        div.appendChild(img);

        google.maps.event.addDomListener(div, "click", clickbubble);

        // Then add the overlay to the DOM
        var panes = this.getPanes();
        panes.overlayImage.appendChild(div);
    }

    // Position the overlay 
    var point = this.getProjection().fromLatLngToDivPixel(this.latlng_);
    if (point) {
        div.style.left = point.x + 'px';
        div.style.top = point.y + 'px';
    }
};

CustomMarker.prototype.remove = function () {
    // Check if the overlay was on the map and needs to be removed.
    if (this.div_) {
        this.div_.parentNode.removeChild(this.div_);
        this.div_ = null;
    }
};

CustomMarker.prototype.getPosition = function () {
    return this.latlng_;
};
/* --------------------------------------------------------------------------*/



/* --------Change bubble's appearance to originator's photo ---------- */

//adapted from http://gmaps-samples-v3.googlecode.com/svn/trunk/overlayview/custommarker.html
function CustomMarker2(latlng, map, imageSrc, args) {
    this.latlng_ = latlng;
    this.imageSrc = imageSrc;
    // Once the LatLng and text are set, add the overlay to the map.  This will
    // trigger a call to panes_changed which should in turn call draw.
    this.setMap(map);
    this.args = args;
}

CustomMarker2.prototype = new google.maps.OverlayView();

CustomMarker2.prototype.draw = function () {
    // Check if the div has been created.
    var div = this.div_;
    if (!div) {
        // Create a overlay text DIV
        div = this.div_ = document.createElement('div');
        // Create the DIV representing our CustomMarker
        div.className = "customMarker2"
        div.id = this.args.marker_id
        var img = document.createElement("img");
        img.src = this.imageSrc;
        div.appendChild(img);

        google.maps.event.addDomListener(div, "click", clickgroupbybubble);

        // Then add the overlay to the DOM
        var panes = this.getPanes();
        panes.overlayImage.appendChild(div);
    }

    // Position the overlay 
    var point = this.getProjection().fromLatLngToDivPixel(this.latlng_);
    if (point) {
        div.style.left = point.x + 'px';
        div.style.top = point.y + 'px';
    }
};

CustomMarker2.prototype.remove = function () {
    // Check if the overlay was on the map and needs to be removed.
    if (this.div_) {
        this.div_.parentNode.removeChild(this.div_);
        this.div_ = null;
    }
};

CustomMarker2.prototype.getPosition = function () {
    return this.latlng_;
};
/* --------------------------------------------------------------------------*/



/*
 * add_activity: 
 *      Triggered when user clicks on the 'Add' button on create_event modal.
 *      Post the event information entered by user back to server.
 *      Create a new bubble to represent the event on map.
 *      Create a new event item and display the event info in the eventlist.
 */

function add_activity(){
    var restaurant_name=$("#addactivity_restaurant_name");
    var activity_name=$("#addactivity_event_name");
    var number=$("#addactivity_number");
    var time = $("#addactivity_time");
    var description=$("#addactivity_description");
    var loggedInUser = document.getElementById("loggedInUser").innerHTML.trim()
    console.log("loggedInUser:"+loggedInUser);
    var pos = {};
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
            var eventid;
            // send post request to url: activity
            $.post('addactivity',{restaurant_name:restaurant_name.val(), event_name:activity_name.val(),numbers:number.val(), time_eating:time.val(), description:description.val(),lat:pos.lat(), lng:pos.lng()})
            .done(function(data){
                if(data['errors'].length!=0) {
                    errorJson = data['errors'].replace(/&quot;/g,'\"');
                    errorJson = JSON.parse(errorJson)
                    var errorString=""
                    for (var item in errorJson) {
                        errorString = errorString+"<li>"+item+": "+errorJson[item]+"</li>";
                    }
                    console.log(errorString);
                    var error = $(errorString);
                    $("#addactivity_errors").append(error);
                }
                else {
                    console.log("add an event");
                    eventid=data['eventid'];
                    console.log("eventid:"+eventid);
                    
                    missionList.push(eventid);
                    var addactivityModal = $("#activity_form");
                    addactivityModal.modal('toggle');
                    var marker = new CustomMarker(pos, map, '/getportrait/'+loggedInUser,{marker_id:eventid});
                    allMyMarkers.push(marker);
                    var header = $("#list-group-head")
                    var newEventItem = $("<a class='list-group-item joinedeventitem' id='joinedevent_"+ eventid + "'>"+
                            "<img src='/getportrait/"+loggedInUser +"' class='img-chat img-thumbnail'>"+
                            "<span class='chat-user-name show-in-modal' alt='people'><span id='joinedEventName_"+eventid+"'>"+activity_name.val()+
                            "</span>&nbsp<span id='joinedEventOrig_"+
                            eventid+"'>"+loggedInUser+"</span></span></a>");
                    header.append(newEventItem);
                }
            });
        });
    }
    else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
      }
}


/*
 * clickbubble: 
 *      When user clicks on the bubble on map, show the event information in event modal.
 */
function clickbubble() {
    var eventid = $(this).attr('id');
    $.post('mealeventbox/' + eventid)
        .done(function (data) {
            var mymodal = $("#curEvent");
            mymodal.data('eventid', eventid)

            var event_name = document.getElementById("info_event_name");
            event_name.innerHTML = data["event_name"];
            var restaurant_name = document.getElementById("info_restaurant_name");
            restaurant_name.innerHTML = "<a href='/restaurant/" + data.restaurant_id + "'>" + data.restaurant_name + "</a>";
            var originator = document.getElementById("info_originator");
            originator.innerHTML = data["originator"];
            var description = document.getElementById("info_event_des");
            description.innerHTML = data['description'];
            var time = document.getElementById("info_event_meet");
            time.innerHTML=data['time'];
            var number = document.getElementById("info_event_number");
            number.innerHTML=data['number'];
            if (data['joined'] == 'True') {
                $("#joinmealbtn").text('Quit');
            }
            else {
                $("#joinmealbtn").text('Join');
            }

            mymodal.modal("toggle");
        });
}


/*
 * clickgroupbybubble: 
 *      When user clicks on the bubble on map, show the event information in event modal.
 */
function clickgroupbybubble() {
    var eventid = $(this).attr('id');
    $.post('groupbuyinfo/' + eventid)
        .done(function (data) {
            var mymodal = $("#groubuyModal");
            mymodal.data('eventid', eventid)

            var groupbuy_name = document.getElementById("groupbuy_event_name");
            groupbuy_name.innerHTML = data["name"];
            var groupbuy_res_name = document.getElementById("groupbuy_restaurant_name");
            groupbuy_res_name.innerHTML = "<a href='/restaurant/" + data.res_id + "'>" + data.resName + "</a>";

            var groupbuy_start = document.getElementById("groupbuy_start");
            groupbuy_start.innerHTML = data["start"];
            var groupbuy_end = document.getElementById("groupbuy_end");
            groupbuy_end.innerHTML = data["end"];
            var groupbuy_desp = document.getElementById("groupbuy_des");
            groupbuy_desp.innerHTML=data['description'];
            
            var groupbuy_

            if (data['joined'] == 'True') {
                $("#joingroupbuybtn").text('Quit');
            }
            else {
                $("#joingroupbuybtn").text('Join');
            }
            mymodal.modal("toggle");
        });
}


/*
 * clickgroupbybubble: 
 *      When user clicks on the bubble on map, show the event information in event modal.
 */
function clickjoinedgroupbuy() {
    console.log("click joined groupbuy");
    var joinedGroupbuyId = $(this).attr('id');
    var eventid = joinedGroupbuyId.split("_")[1];
    var joinedGroupbuyModal = $("#joinedGroupbuy");
    joinedGroupbuyModal.data('eventid', eventid);
    $.post('groupbuyinfo/' + eventid)
        .done(function (data) {
            console.log("groupbuy info");
            joinedGroupbuyModal.data('eventid', eventid)
            var groupbuy_name = document.getElementById("joined_gb_event_name");
            groupbuy_name.innerHTML = data["name"];
            var groupbuy_res_name = document.getElementById("joined_gb_restaurant_name");
            groupbuy_res_name.innerHTML = "<a href='/restaurant/" + data.res_id + "'>" + data.resName + "</a>";

            var groupbuy_start = document.getElementById("joined_gb_start");
            groupbuy_start.innerHTML = data["start"];
            var groupbuy_end = document.getElementById("joined_gb_end");
            groupbuy_end.innerHTML = data["end"];
            var groupbuy_desp = document.getElementById("joined_gb_des");
            groupbuy_desp.innerHTML=data['description'];

            joinedGroupbuyModal.modal("show");
        });
}

/*
 * joingroupbuy: 
 *      When user clicks on the Join/Quit button on event modal,
 *      Join: add the user to the event's member set, and create a new event item in the event list.
 *      Quit: remove the user from the event's member set and remove the corresponding event item 
 *            from event list.
 *      Revised@11.30, fix the bug when viewing newly joined meal
 *             @12.1, add/delete element in missionList
 */
function joingroupbuy() {
    console.log("joingroupbuy");
    var groubuyModal = $('#groubuyModal');
    var joinBtn = $("#joingroupbuybtn")
    var idnum = groubuyModal.data('eventid')

    if (joinBtn.text().trim() == 'Quit') {
        $.post("/quitgroupbuy", {eventid: idnum})
            .done(function (data) {
                var joinedGroupbuyItem = $("#joinedgroupbuy_" + idnum);
                joinedGroupbuyItem.remove();
                joinBtn.text('Join');
            });
    }
    else {
        var groupbuyName = document.getElementById("groupbuy_event_name").innerHTML.trim();
        $.post("/joingroupbuy", {eventid: idnum})
            .done(function (data) {
                var eventListHeader = $("#list-group-head")
                var newEventItem = $("<a class='list-group-item joinedgroupbuyitem' id='joinedgroupbuy_" + idnum + "'>" +
                    // "<i class='fa fa-check-circle joinedGroupbuy'></i>"+
                    "<img src='../../static/img/portfolio/groupbuy.jpg' class='img-chat img-thumbnail'>" +
                    "<span class='chat-user-name show-in-modal' alt='people'><span id='joinedGroupbuyName_" + idnum + "'>" + groupbuyName +
                    "</span></span></a>");
                eventListHeader.append(newEventItem);
            });
        joinBtn.text('Quit');
    }
    groubuyModal.modal('toggle');
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
        'We can use this to post the news' :
        'Error: Your browser doesn\'t support geolocation.');
}

/* 
 * populate_bubble: 
 *      Populate all the bubble when the page is ready.
 *      Revised@12.1 Change bubble style
 */
function populate_bubble() {
    console.log("populatebubble");
    $.get("get_allbubbles")
        .done(function (data) {
            for (var i = 0; i < data.bubbles.length; i++) {
                bubble = data.bubbles[i]
                var pos = new google.maps.LatLng(bubble['x'], bubble['y']);
                console.log("bubble['originator']:" + bubble['originator']);
                var marker = new CustomMarker(pos, map, '/getportrait/' + bubble['originator'], {marker_id: bubble['id']});
                allMyMarkers.push(marker);
            }
        });
}

/*
 * populate_list:
 *      Populate all the entries in mission list
 *      Added@12.1
 */
function populate_list() {
    var username = document.getElementById("loggedInUser").innerHTML.trim()
    var header = $("#list-group-head")

    $.get("getallitems", {username: username})
        .done(function (data) {
            for (var i = 0; i < data.items.length; i++) {
                item = data.items[i];
                missionList.push(item['id']);
                console.log("item['originator']" + item['originator']);
                if (username == item['originator']) {
                    var newEventItem = $("<a class='list-group-item joinedeventitem' id='joinedevent_" + item['id'] + "'>" +
                        "<img src='/getportrait/" + item['originator'] + "' class='img-chat img-thumbnail'>" +
                        "<span class='chat-user-name show-in-modal' alt='people'><span id='joinedEventName_" + item['id'] + "'>" + item['event_name'] +
                        "</span>&nbsp<span id='joinedEventOrig_" +
                        item['id'] + "'>" + item['originator'] + "</span></span></a>");
                }

                else {
                    var newEventItem = $("<a class='list-group-item joinedeventitem' id='joinedevent_" + item['id'] + "'>" +
                        "<img src='/getportrait/" + item['originator'] + "' class='img-chat img-thumbnail'>" +
                        "<span class='chat-user-name show-in-modal' alt='people'><span id='joinedEventName_" + item['id'] + "'>" + item['event_name'] +
                        "</span>&nbsp<span id='joinedEventOrig_" +
                        item['id'] + "'>" + item['originator'] + "</span></span></a>");
                }

                header.append(newEventItem);
            }
        });

}

function populate_group_buy_bubble() {
    $.get("get_group_buy_allbubbles")
        .done(function (data) {
            console.log("populate groupbuy bubble");
            for (var i = 0; i < data.groupbuy_bubbles.length; i++) {
                groupbuy_bubble = data.groupbuy_bubbles[i];
                var pos = new google.maps.LatLng(groupbuy_bubble['x'], groupbuy_bubble['y']);
                var marker = new CustomMarker2(pos, map, "../../static/img/portfolio/groupbuy.jpg", {marker_id: groupbuy_bubble['id']});
                groupbuyMarkers.push(marker);
            }
        });

}

function populate_group_buy_list() {
    var username = document.getElementById("loggedInUser").innerHTML.trim()
    var eventListHeader = $("#list-group-head")
    $.get("get_all_groupbuy_items", {username: username})
        .done(function (data) {
            for (var i = 0; i < data.items.length; i++) {
                item = data.items[i];
                var newEventItem = $("<a class='list-group-item joinedgroupbuyitem' id='joinedgroupbuy_" + item['id'] + "'>" +
                    "<img src='../../static/img/portfolio/groupbuy.jpg' class='img-chat img-thumbnail'>" +
                    "<span class='chat-user-name show-in-modal' alt='people'><span id='joinedGroupbuyName_" + item['id'] + "'>" + item['name'] +
                    "</span></span></a>");
                eventListHeader.append(newEventItem);
            }
        });
}

function removemealbubble() {
    var joinMealModal = $('#curEvent');   
    var idnum = joinMealModal.data('eventid');
    for(var i=0;i<allMyMarkers.length;i++){
        if(allMyMarkers[i].args.marker_id == idnum){
            allMyMarkers[i].setMap(null);
            break;
        }
    }
    joinMealModal.modal("toggle")
}

function removegroupbuybubble() {
    console.log("removebubble");
    var groupbuyModal = $('#groubuyModal');   
    var idnum = groupbuyModal.data('eventid');
    for(var i=0;i<groupbuyMarkers.length;i++){
        if(groupbuyMarkers[i].args.marker_id == idnum){
            groupbuyMarkers[i].setMap(null);
            break;
        }
    }
    groupbuyModal.modal("toggle");
}


/*
 * quitgroupbuy:
 *      When user clicks on the 'Quit' button on joinedgroupbuy modal,
 *      remove the user from groupbuy's member set as well as remove the groupbuy item from eventlist.
 */
function quitgroupbuy() {
    var mymodal = $("#joinedGroupbuy")

    // remove the event from mission list
    var id = mymodal.data('eventid')

    var groupbuydiv = $("#joinedgroupbuy_" + id);
    groupbuydiv.remove();

    // remove the event from database
    $.post("/quitgroupbuy", {eventid: id});
    mymodal.modal("toggle");
}


/*
 * joinmeal: 
 *      When user clicks on the Join/Quit button on event modal,
 *      Join: add the user to the event's member set, and create a new event item in the event list.
 *      Quit: remove the user from the event's member set and remove the corresponding event item 
 *            from event list.
 *      Revised@11.30, fix the bug when viewing newly joined meal
 *             @12.1, add/delete element in missionList
 */
function joinmeal() {
    var joinMealModal = $('#curEvent');
    var joinBtn = $("#joinmealbtn")
    var idnum = joinMealModal.data('eventid')

    if (joinBtn.text().trim() == 'Quit') {
        $.post("/quitmealevent", {eventid: idnum})
            .done(function (data) {
                var index = missionList.indexOf(idnum);
                if (index > -1) {
                    missionList.splice(index, 1);
                }
                else {
                    console.log("delete item from mission list error");
                }
            });
        var name1 = document.getElementById("loggedInUser").innerHTML.trim()
        var name2 = document.getElementById("joinedEventOrig_" + idnum).innerHTML.trim();
        if (name1 == name2) {
            for (var i = 0; i < allMyMarkers.length; i++) {
                if (allMyMarkers[i].args.marker_id == idnum) {
                    allMyMarkers[i].setMap(null);
                    break;
                }
            }
        }
        var joinedEventItem = $("#joinedevent_" + idnum);
        joinedEventItem.remove();
        $(this).text('Join');
    }

    else {
        var eventName = document.getElementById("info_event_name").innerHTML.trim();
        var resName = document.getElementById("info_restaurant_name").innerHTML.trim();
        var originatorName = document.getElementById("info_originator").innerHTML.trim();
        var eventListHeader = $("#list-group-head")
        console.log("originatorName:" + originatorName);
        var newEventItem = $("<a class='list-group-item joinedeventitem' id='joinedevent_" + idnum + "'>" +
            "<img src='/getportrait/" + originatorName + "' class='img-chat img-thumbnail'>" +
            "<span class='chat-user-name show-in-modal' alt='people'><span id='joinedEventName_" + idnum + "'>" + eventName +
            "</span>&nbsp<span id='joinedEventOrig_" +
            idnum + "'>" + originatorName + "</span></span></a>");
        eventListHeader.append(newEventItem);
        $.post("/joinmealevent", {eventid: idnum})
            .done(function (data) {
                missionList.push(idnum);
            });
        $(this).text('Quit');
    }
    joinMealModal.modal('toggle');
}

/*
 * updateList:
 *      Update mission list at a set interval.
 *      Remove the event that has been cancelled by its originator
 *      Added@12.1
 */
function updateList() {
    var username = document.getElementById("loggedInUser").innerHTML.trim()
    var header = $("#list-group-head")
    var eventListHeader = $("#list-group-head")
    $.get("getallitems", {username: username})
        .done(function (data) {
            var list = data['list'].trim().split(" ");
            for (var i = 0; i < missionList.length; i++) {
                if ($.inArray(missionList[i], list) == -1) {
                    var delItem = $("#joinedevent_" + missionList[i]);
                    delItem.remove();
                }
            }
        });
}

/*
 * quitmeal:
 *      When user clicks on the 'Quit' button on joinedevent modal,
 *      remove the user from event's member set as well as remove the event item from eventlist.
 */
function quitmeal() {
    var mymodal = $("#joinedEvent")

    // remove the event from mission list
    var id = mymodal.data('eventid')
    var index = missionList.indexOf(id);
    if (index > -1) {
        missionList.splice(index, 1);
    }
    else {
        console.log("delete item from mission list error");
    }

    // Remove the marker from map if the originator cancels an event
    var name1 = document.getElementById("loggedInUser").innerHTML.trim()
    var name2 = document.getElementById("joinedEventOrig_" + id).innerHTML.trim();
    if (name1 == name2) {
        for (var i = 0; i < allMyMarkers.length; i++) {
            if (allMyMarkers[i].args.marker_id == id) {
                allMyMarkers[i].setMap(null);
                break;
            }
        }
    }
    var eventdiv = $("#joinedevent_" + id);
    eventdiv.remove();

    // remove the event from database
    $.post("/quitmealevent", {eventid: id});
    mymodal.modal("toggle");
}

/*
 * clickjoinedevent:
 *      When user clicks on the event item in eventlist,
 *      open event modal and display the current event's infomation.
 */
function clickjoinedevent() {
    var joinedEventId = $(this).attr('id');
    var eventid = joinedEventId.split("_")[1];
    var joinedEventModal = $("#joinedEvent");
    joinedEventModal.data('eventid', eventid);

    $.post('mealeventbox/' + eventid)
        .done(function (data) {
            var eventModalName = document.getElementById("joined_event_name");
            eventModalName.innerHTML = data['event_name'];
            var resModalName = document.getElementById("joined_restaurant_name");
            resModalName.innerHTML = "<a href='/restaurant/" + data.restaurant_id + "'>" + data.restaurant_name + "</a>";
            var origModalName = document.getElementById("joined_orig_name");
            origModalName.innerHTML = data["originator"];
            var despModalName = document.getElementById("joined_event_des");
            despModalName.innerHTML=data['description'];
            var time = document.getElementById("joined_event_meet");
            time.innerHTML=data['time'];
            var number=document.getElementById("joined_event_number");
            number.innerHTML=data['number'];
            joinedEventModal.modal('show');
        });
}

function getprofile() {
    var proname = $(this).html();
    console.log(proname);
    $.post("/getprofile", {name: proname})
        .done(function (data) {
            var usernameItem = document.getElementById("username_info");
            usernameItem.innerHTML = data.username;
            var firstnameItem = document.getElementById("firstname_info");
            firstnameItem.innerHTML = "First name:" + " " + data.firstname;
            var lastnameItem = document.getElementById("lastname_info");
            lastnameItem.innerHTML = "Last name:" + " " + data.lastname;
            var emailItem = document.getElementById("email_info");
            emailItem.innerHTML = "Email:" + " " + data.email;
            var gendernageItem = document.getElementById("gender_info");
            gendernageItem.innerHTML = "Gender:" + " " + data.gender + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspAge: " + data.age;
            var foodItem = document.getElementById("food_info");
            foodItem.innerHTML = "Favourite food:" + " " + data.food;
            var photoItem = document.getElementById("info_userphoto");
            if (data.hasphoto == "True") {
                photoItem.innerHTML = "<img class='marginleft round-borderim float-left' src='photo" + data.id + "' alt='photo' " +
                    "height='120' width='120'/>";
            }
            else {
                photoItem.innerHTML = "<img class='marginleft float-left' src='../../static/images/default_img.png' alt='photo' " +
                    "height='120' width='120'/>";
            }
        });
}

function getprofile_misson() {
    var proname = $(this).html();
    $.post("/getprofile", {name: proname})
        .done(function (data) {
            var usernameItem = document.getElementById("username_info_c");
            usernameItem.innerHTML = data.username;
            var firstnameItem = document.getElementById("firstname_info_c");
            firstnameItem.innerHTML = "First name:" + " " + data.firstname;
            var lastnameItem = document.getElementById("lastname_info_c");
            lastnameItem.innerHTML = "Last name:" + " " + data.lastname;
            var emailItem = document.getElementById("email_info_c");
            emailItem.innerHTML = "Email:" + " " + data.email;
            var gendernageItem = document.getElementById("gender_info_c");
            gendernageItem.innerHTML = "Gender:" + " " + data.gender + "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspAge: " + data.age;
            var foodItem = document.getElementById("food_info_c");
            foodItem.innerHTML = "Favourite food:" + " " + data.food;
            var photoItem = document.getElementById("info_userphoto_c");
            if (data.hasphoto == "True") {
                photoItem.innerHTML = "<img class='marginleft round-borderim float-left' src='photo" + data.id + "' alt='photo' " +
                    "height='120' width='120'/>";
            }
            else {
                photoItem.innerHTML = "<img class='marginleft float-left' src='../../static/images/default_img.png' alt='photo' " +
                    "height='120' width='120'/>";
            }
        });
}

$(document).ready(function () {
    // Add event-handlers

    $(".fancybox1").fancybox({
        'titlePosition': 'over',
        openEffect: 'none',
        closeEffect: 'none',
        // 'type':'iframe',

        'titleFormat': function (title, currentArray, currentIndex, currentOpts) {
            return '<span id="fancybox-title-over">' + (currentIndex + 1) +
                ' / ' + currentArray.length + (title.length ? '   ' + title : '') + '</span>';
        }
    });

    initMap();
    $("#edit-btn").click(function () {
        $.fancybox.close();
    });
    $(document).on("click", "#info_originator", getprofile);
    $(document).on("click", "#joined_orig_name", getprofile_misson);
    $("#add_activity").click(add_activity);
    $("#map").on("click", ".bubble", clickbubble);

    // join meal event, quit meal event
    $("#joinmealbtn").click(joinmeal);
    $(".chat-sidebar").on("click", ".joinedeventitem", clickjoinedevent);
    $("#quitmealbtn").click(quitmeal);

    // join groupbuy, quit groupbuy
    $("#joingroupbuybtn").click(joingroupbuy);
    $(".chat-sidebar").on("click", ".joinedgroupbuyitem", clickjoinedgroupbuy);
    $("#quitgroupbuybtn").click(quitgroupbuy);

    $("#removemealbubble").click(removemealbubble);
    $("#removegroupbuybubble").click(removegroupbuybubble);

    //clear field data when hide the modal
    $('#activity_form').on('hidden.bs.modal', function (e) {
        $("#addactivity_restaurant_name").val("");
        $("#addactivity_event_name").val("");
        $("#addactivity_number").val("");
        $("#addactivity_time").val("");
        $("#addactivity_description").val("");
        document.getElementById("addactivity_errors").innerHTML = "";
    });

    populate_bubble();
    populate_list();
    populate_group_buy_bubble();
    populate_group_buy_list();
    window.setInterval(updateList, 5000);

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
