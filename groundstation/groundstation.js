/**
 * 
 */

var SERVER_URL = getURLParameter("local") == "true" ? "http://localhost:9090"
		: "http://home.kolesnik.org:9090";

var debug = getURLParameter("debug") == "true";
// var debug = true;

var currentUnit = "drone1";

var marker = null;

var mainMap = null;

var contextMenu = null;

var currentWPIndex = 1;

var allMarkers = [];

var fakeDroneHeartbeat = {
	heartbeat : {
		"unitId" : "drone1",
		"stateTimestampMS" : 1482972148956,
		"gpsLatLon" : "",
		"gpsLat" : 42.5227644,
		"gpsLon" : -71.186572,
		"gpsAlt" : 51.768,
		"homeLatLon" : "",
		"homeLat" : 42.52252,
		"homeLon" : -71.1867931,
		"homeAlt" : 52.515,
		"gpsSpeed" : 0.945113480091095,
		"gpsTime" : "none",
		"gpsStatus" : "none",
		"gpsLastStatusMS" : 1482972148956,
		"airSpeed" : 0.0,
		"baroAlt" : 0.0,
		"sonarAlt" : 0.0,
		"heading" : 237,
		"status" : "STANDBY",
		"gpsNumSats" : 12,
		"gpsLock" : 4,
		"gpsHError" : 91,
		"gpsVError" : 168,
		"currVolts" : 12.316,
		"currVoltsLevel" : 88.0,
		"currMah" : 0.73,
		"unitCallbackPort" : "8080",
		"unitHostAddress" : "108.49.218.135"
	}
};

var heartbeats = null;

initMapWithRemoteCoords();

/******************************** UI FUNCTION **********************************/

function initMapWithRemoteCoords() {

	getDroneLocation(initMap, currentUnit);

	getAllDrones(function(data) {
		heartbeats = data;
		var options = $("#drones");
		$.each(heartbeats.heartbeats, function() {
			options.append($("<option />").val(this.heartbeat.unitId).text(
					this.heartbeat.unitId));
		});
	});

}

function initMap(data) {
	if (!data || !data.heartbeat) {
		data = {
			heartbeat : {
				gpsLat : 0,
				gpsLon : 0,
				heading : 0
			}
		};
	}
	// if no gps lock
	if (data.heartbeat.gpsLat == null)
		data.heartbeat.gpsLat = 0;
	if (data.heartbeat.gpsLon == null)
		data.heartbeat.gpsLon = 0;

	mainMap = new GMaps({
		el : '#map',
		zoom : 20,
		lat : data.heartbeat.gpsLat,
		lng : data.heartbeat.gpsLon
	});

	// add top menu
	/*	
	 addControl("ARM", arm);
	 addControl("DISARM", disarm);
	 addControl("TAKEOFF", takeoff);	
	 addControl("LAND", land);
	 addControl("PAUSE", pause);
	 addControl("RETURN HOME", returnToHome);
	
	 var controlDiv = document.createElement('div');
	 */

	mainMap.setContextMenu({
		control : 'map',
		options : [ {
			title : 'Add Waypoint',
			name : 'add_waypoint',
			style : {
				margin : '7px',
				padding : '10px 10px',
				border : 'solid 1px #717B87',
				fontFamily : 'Roboto, sans-serif',
				background : '#fff'
			},
			action : function(e) {

				var waypoint = this.addMarker({
					lat : e.latLng.lat(),
					lng : e.latLng.lng(),
					title : 'WP ' + currentWPIndex++
				});

				allMarkers.push(waypoint);

			}
		}, {
			title : 'Go here',
			name : 'go_here',
			action : function(e) {

				gotoXYZ(e.latLng.lat(), e.latLng.lng());

			}
		} ]
	});

	// every 1 second
	window.setInterval(updateMarkers, 1000);

}

function addControl(name, callback) {
	mainMap.addControl({
		position : 'bottom_center',
		content : name,
		style : {
			margin : '7px',
			padding : '10px 10px',
			border : 'solid 1px #717B87',
			fontFamily : 'Roboto, sans-serif',
			background : '#fff'
		},
		events : {
			click : callback
		}
	});
}

function removeMarkers() {
	for (i = 0; i < allMarkers.length; i++) {
		allMarkers[i].setMap(null);
	}
	allMarkers = [];
}

function isInBounds(aMarker) {
	return mainMap.getBounds().contains(aMarker.getPosition());
}

function updateMarkers() {

	// a.forEach(function(element) {
	// console.log(element);
	// });

	getDroneLocation(function(data) {

		if (!data || !data.heartbeat) {
			data = {
				heartbeat : {
					gpsLat : 0,
					gpsLon : 0,
					heading : 0
				}
			};
		}
		// if no GPS Lock
		if (data.heartbeat.gpsLat == null)
			data.heartbeat.gpsLat = 0;
		if (data.heartbeat.gpsLon == null)
			data.heartbeat.gpsLon = 0;

		if (marker == null) {

			marker = mainMap.addMarker({
				lat : data.heartbeat.gpsLat,
				lng : data.heartbeat.gpsLon,
				title : data.heartbeat.unitId,
				label : data.heartbeat.unitId,
				icon : {
					path : google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
					scale : 10,
					strokeColor : "red",
					rotation : data.heartbeat.heading
				},
				click : function(e) {
					alert('You clicked in this marker');
				}
			});

		} else {
			marker.setPosition({
				lat : data.heartbeat.gpsLat,
				lng : data.heartbeat.gpsLon
			});
			marker.setIcon({
				path : google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
				scale : 10,
				strokeColor : "red",
				rotation : data.heartbeat.heading
			});
		}
		updateInfo(data);
	}, currentUnit);
}

function updateInfo(data) {

	if (currentUnit == data.heartbeat.unitId) {

		$("#unit").html(data.heartbeat.unitId);
		$("#heading").html(data.heartbeat.heading);
		$("#gps-speed").html(data.heartbeat.gpsSpeed.toFixed(2) + " m/s");
		$("#alt-baro").html(data.heartbeat.baroAlt.toFixed(2) + " m");
		$("#alt-gps").html(data.heartbeat.gpsAlt.toFixed(2) + " m");
		$("#gps-sats").html(data.heartbeat.gpsNumSats);
		$("#gps-lock").html(data.heartbeat.gpsLock);
		$("#bat").html(
				data.heartbeat.currVolts + "V " + data.heartbeat.currVoltsLevel
						+ "%");
		$("#curr").html(data.heartbeat.currMah * 1000 + " mAh");

		//update command list
		listActions(currentUnit, function(commands) {
			
			var html = "";
			if (commands) {
				$.each(commands, function() {
					html += "<div id=\"command-list-item\">"+this.command.name+"</div>";
				});
			}
			$("#command-list").html(html);
		});
	}
}

/********************* DATA FUNCTIONS ******************************************/

function getURLParameter(sParam) {
	var sPageURL = window.location.search.substring(1);
	var sURLVariables = sPageURL.split('&');
	for (var i = 0; i < sURLVariables.length; i++) {
		var sParameterName = sURLVariables[i].split('=');
		if (sParameterName[0] == sParam) {
			return sParameterName[1];
		}
	}

	return "";
}

function getDroneLocationURL(unitId) {
	return SERVER_URL + "/heartbeat/" + unitId;
}

function getComandsURL(unitId) {
	return SERVER_URL + "/actions/" + unitId;
}

function getAllDronesURL() {
	return SERVER_URL + "/heartbeats";
}

function getActionURL() {
	return SERVER_URL + "/action";
}

function getDroneLocation(callback, unitId) {
	if (debug) {
		// make it rotate a bit with every refresh

		fakeDroneHeartbeat.heartbeat.heading += 10;

		if (fakeDroneHeartbeat.heartbeat.heading > 360)
			fakeDroneHeartbeat.heartbeat.heading -= 360;

		callback(fakeDroneHeartbeat);

		return;
	}
	// $.getJSON(getDroneLocationURL(unitId), callback);
	$.get(getDroneLocationURL(unitId), {}, callback).fail(function() {
		// Handle error here
		callback(null);
	});
}

function listActions(unitId, callback) {
	$.get(getComandsURL(unitId), {}, callback).fail(function() {
		// Handle error here
		callback(null);
	});	
}

function deleteActions(unitId, callback) {
	
	$.get(getComandsURL("delete/" + unitId), {}, callback).fail(function() {
		// Handle error here
		callback(null);
	});	
	
	/*
	$.ajax({
		url : getComandsURL(unitId),
		type : 'DELETE',
		data : '',
		dataType : 'text',
		success : callback
	});
	*/
}

function getAllDrones(callback) {
	if (debug) {
		// make it rotate a bit with every refresh

		fakeDroneHeartbeat.heartbeat.heading += 10;

		if (fakeDroneHeartbeat.heartbeat.heading > 360)
			fakeDroneHeartbeat.heartbeat.heading -= 360;

		heartbeats = {
			heartbeats : [ fakeDroneHeartbeat ]
		}

		callback(fakeDroneHeartbeat);

		return;
	}
	$.get(getAllDronesURL(), {}, callback).fail(function() {
		// Handle error here
		callback(null);
	});
}

function sendAction(data, callback) {

	$.ajax({
		url : getActionURL(),
		type : 'post',
		dataType : 'json',
		success : callback,
		data : JSON.stringify(data)
	});
}

function buildActionRequest(unitId, command, parameters) {

	var action = {
		unitId : unitId,
		command : {
			name : command,
			parameters : parameters
		}

	};

	return action;
}

/******************* MENU HANDLERS *********************************************/

/** clear unsent command queue for current unit */
function clearQueue() {

	if (!currentUnit)
		return;

	deleteActions(currentUnit, function(data) {});
	$("#command-list").html("");

}

function handleActionResponse(data) {
	// ???
}

function arm() {
	sendAction(buildActionRequest(currentUnit, "ARM"), function() {

	});
}
function disarm() {
	sendAction(buildActionRequest(currentUnit, "DISARM"), function() {

	});
}
function takeoff() {
	sendAction(buildActionRequest(currentUnit, "TAKEOFF"), function() {

	});
}
function land() {
	sendAction(buildActionRequest(currentUnit, "LAND"), function() {

	});
}
function returnToHome() {
	sendAction(buildActionRequest(currentUnit, "RTL"), function() {

	});
}
function pause() {
	sendAction(buildActionRequest(currentUnit, "POSITION"), function() {

	});
}

function gotoXYZ(lat, lon) {

	var parameters = [ {
		name : "lat",
		value : lat
	}, {
		name : "lon",
		value : lon
	} ];

	sendAction(buildActionRequest(currentUnit, "GOTO", parameters),
			function() {

			});
}
