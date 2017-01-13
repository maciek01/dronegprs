/**
 * 
 */

//var SERVER_URL = "http://home.kolesnik.org:9090";
var SERVER_URL = "http://localhost:9090";

var debug = false;
//var debug = true;

var marker = null;

var mainMap = null;

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

function getDroneLocationURL(unitId) {
	return SERVER_URL + "/heartbeat/" + unitId;
}

function getAllDronesURL() {
	return SERVER_URL + "/heartbeats";
}

function getActionURL() {
	return SERVER_URL + "/action";
}

function getDroneLocation(callback, unitId) {
	if (debug) {
		//make it rotate a bit with every refresh

		fakeDroneHeartbeat.heartbeat.heading += 10;

		if (fakeDroneHeartbeat.heartbeat.heading > 360)
			fakeDroneHeartbeat.heartbeat.heading -= 360;

		callback(fakeDroneHeartbeat);

		return;
	}
	//$.getJSON(getDroneLocationURL(unitId), callback);
	$.get(getDroneLocationURL(unitId), {}, callback).fail(function() {
		// Handle error here
		callback(null);
	});
}

function getAllDrones(callback) {
	if (debug) {
		//make it rotate a bit with every refresh

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

function sendCommand(data, callback) {
	
    $.ajax({
        url: getActionURL(),
        type: 'post',
        dataType: 'json',
        success: callback,
        data: JSON.stringify(data)
    });
}

function initMapWithRemoteCoords() {
	getDroneLocation(initMap, "drone1");

	getAllDrones(function(data) {
		heartbeats = data;
		var options = $("#drones");
		$.each(heartbeats.heartbeats, function() {
			options.append($("<option />").val(this.heartbeat.unitId).text(
					this.heartbeat.unitId));
		})
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
	//if no gps lock
	if (data.heartbeat.gpsLat == null)
		data.heartbeat.gpsLat = 0;
	if (data.heartbeat.gpsLon == null)
		data.heartbeat.gpsLon = 0;

	//center the map
	mainMap = new google.maps.Map(document.getElementById('map'), {
		zoom : 20,
		center : {
			lat : data.heartbeat.gpsLat,
			lng : data.heartbeat.gpsLon
		},
	});

	// every 1 second
	window.setInterval(updateMarker, 1000);
}

function isInBounds(aMarker) {
	return mainMap.getBounds().contains(aMarker.getPosition());
}

function updateMarker() {

	//		a.forEach(function(element) {
	//		    console.log(element);
	//		});

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
		//if no GPS Lock
		if (data.heartbeat.gpsLat == null)
			data.heartbeat.gpsLat = 0;
		if (data.heartbeat.gpsLon == null)
			data.heartbeat.gpsLon = 0;

		if (marker == null) {
			marker = new google.maps.Marker({
				position : {
					lat : data.heartbeat.gpsLat,
					lng : data.heartbeat.gpsLon
				},
				icon : {
					path : google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
					scale : 10,
					strokeColor : "red",
					rotation : data.heartbeat.heading
				},
				draggable : false,
				map : mainMap
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
	}, "drone1");
}

function buildActionRequest(unitId, command) {

	var action = {
		unitId : unitId,
		command : {
			name : command
		}

	};
	
	return action;
}

function handleActionResponse(data) {
	//???
}

function arm() {
	sendCommand(buildActionRequest("drone1", "ARM"), function() {
		
		
	});
}
function disarm() {
	sendCommand(buildActionRequest("drone1", "DISARM"), function() {
		
		
	});
}
function takeoff() {
	sendCommand(buildActionRequest("drone1", "TAKEOFF"), function() {
		
		
	});
}
function land() {
	sendCommand(buildActionRequest("drone1", "LAND"), function() {
		
		
	});
}
function returnToHome() {
	sendCommand(buildActionRequest("drone1", "RTL"), function() {
		
		
	});
}
function pause() {
	sendCommand(buildActionRequest("drone1", "POSITION"), function() {
		
		
	});
}






