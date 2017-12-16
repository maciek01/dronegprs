/* */
package org.kolesnik.droneserver.model.heartbeat;

/**
 * This class is a model of the current UAV state. UAV transmits its state in 3 different reporting intervals
 * 1 sec - position critical data
 * 5 sec - general status data
 * 30 sec - "relatively" static data TODO: needs more precise specification
 * @author mkolesnik
 *
 */
public class Heartbeat {
	
	/** assigned id */
	private String unitId;			//1 Hz expected reporting

	//1 sec reporting
	/** */
	private long stateTimestampMS;
	private String gpsLatLon;
	private Double gpsLat;
	private Double gpsLon;
	private Double gpsAlt;
	
	private String homeLatLon;
	private Double homeLat;
	private Double homeLon;
	private Double homeAlt;	
	
	private Integer operatingAlt;
	private Integer operatingSpeed;
	
	private Double gpsSpeed;
	private String gpsTime;
	private String gpsStatus;
	private long gpsLastStatusMS;
	
	private Double airSpeed;
	private Double baroAlt;
	private Double sonarAlt;
	
	private Integer heading;
	private String status;
	
	//5 sec reporting
	private Integer gpsNumSats;
	private Integer gpsLock;
	private Integer gpsHError;
	private Integer gpsVError;
	
	
	private Double currVolts;
	private Double currVoltsLevel;
	private Double currMah;
	
	//30 sec reporting
	private String unitCallbackPort;

	//server calculated
	private String unitHostAddress;
	
	/**
	 * Update this object
	 * @param heartbeat
	 */
	public void update(Heartbeat heartbeat) {
		if (heartbeat.unitId != null) {
			this.unitId = heartbeat.unitId;
		}
		if (heartbeat.gpsLatLon != null) {
			this.gpsLatLon = heartbeat.gpsLatLon;
		}
		if (heartbeat.gpsLat != null) {
			this.gpsLat = heartbeat.gpsLat;
		}
		if (heartbeat.gpsLon != null) {
			this.gpsLon = heartbeat.gpsLon;
		}
		if (heartbeat.gpsAlt != null) {
			this.gpsAlt = heartbeat.gpsAlt;
		}
		if (heartbeat.homeLatLon != null) {
			this.homeLatLon = heartbeat.homeLatLon;
		}
		if (heartbeat.homeLat != null) {
			this.homeLat = heartbeat.homeLat;
		}
		if (heartbeat.homeLon != null) {
			this.homeLon = heartbeat.homeLon;
		}
		if (heartbeat.homeAlt != null) {
			this.homeAlt = heartbeat.homeAlt;
		}		
		if (heartbeat.operatingAlt != null) {
			this.operatingAlt = heartbeat.operatingAlt;
		}		
		if (heartbeat.operatingSpeed != null) {
			this.operatingSpeed = heartbeat.operatingSpeed;
		}		
		if (heartbeat.gpsSpeed != null) {
			this.gpsSpeed = heartbeat.gpsSpeed;
		}
		if (heartbeat.gpsNumSats != null) {
			this.gpsNumSats = heartbeat.gpsNumSats;
		}
		if (heartbeat.gpsLock != null) {
			this.gpsLock = heartbeat.gpsLock;
		}
		if (heartbeat.gpsHError != null) {
			this.gpsHError = heartbeat.gpsHError;
		}
		if (heartbeat.gpsVError != null) {
			this.gpsVError = heartbeat.gpsVError;
		}
		if (heartbeat.stateTimestampMS != 0) {
			this.stateTimestampMS = heartbeat.stateTimestampMS;
		}
		if (heartbeat.baroAlt != null) {
			this.baroAlt = heartbeat.baroAlt;
		}
		if (heartbeat.airSpeed != null) {
			this.airSpeed = heartbeat.airSpeed;
		}
		if (heartbeat.sonarAlt != null) {
			this.sonarAlt = heartbeat.sonarAlt;
		}
		if (heartbeat.heading != null) {
			this.heading = heartbeat.heading;
		}
		if (heartbeat.status != null) {
			this.status = heartbeat.status;
		}
		if (heartbeat.currVolts != null) {
			this.currVolts = heartbeat.currVolts;
		}
		if (heartbeat.currVoltsLevel != null) {
			this.currVoltsLevel = heartbeat.currVoltsLevel;
		}
		if (heartbeat.currMah != null) {
			this.currMah = heartbeat.currMah;
		}
		if (heartbeat.unitCallbackPort != null) {
			this.unitCallbackPort = heartbeat.unitCallbackPort;
		}
		if (heartbeat.unitHostAddress != null) {
			this.unitHostAddress = heartbeat.unitHostAddress;
		}
		if (heartbeat.gpsTime != null) {
			this.gpsTime = heartbeat.gpsTime;
		}
		if (heartbeat.gpsStatus != null) {
			this.gpsStatus = heartbeat.gpsStatus;
		}
		if (heartbeat.gpsLastStatusMS != 0) {
			this.gpsLastStatusMS = heartbeat.gpsLastStatusMS;
		}
	}
	
	//auto gen getters setters
	
	/**
	 * @return the unitId
	 */
	public String getUnitId() {
		return unitId;
	}
	/**
	 * @param unitId the unitId to set
	 */
	public void setUnitId(String unitId) {
		this.unitId = unitId;
	}
	
	/**
	 * @return the gpsLatLon
	 */
	public String getGpsLatLon() {
		return gpsLatLon;
	}
	/**
	 * @param gpsLatLon the gpsLatLon to set
	 */
	public void setGpsLatLon(String gpsLatLon) {
		this.gpsLatLon = gpsLatLon;
	}
	/**
	 * @return the gpsAlt
	 */
	public Double getGpsAlt() {
		return gpsAlt;
	}
	/**
	 * @param gpsAlt the gpsAlt to set
	 */
	public void setGpsAlt(Double gpsAlt) {
		this.gpsAlt = gpsAlt;
	}
	/**
	 * @return the gpsSpeed
	 */
	public Double getGpsSpeed() {
		return gpsSpeed;
	}
	/**
	 * @param gpsSpeed the gpsSpeed to set
	 */
	public void setGpsSpeed(Double gpsSpeed) {
		this.gpsSpeed = gpsSpeed;
	}
	/**
	 * @return the gpsNumSats
	 */
	public Integer getGpsNumSats() {
		return gpsNumSats;
	}
	/**
	 * @param gpsNumSats the gpsNumSats to set
	 */
	public void setGpsNumSats(Integer gpsNumSats) {
		this.gpsNumSats = gpsNumSats;
	}
	/**
	 * @return the gpsLock
	 */
	public Integer getGpsLock() {
		return gpsLock;
	}
	/**
	 * @param gpsLock the gpsLock to set
	 */
	public void setGpsLock(Integer gpsLock) {
		this.gpsLock = gpsLock;
	}
	/**
	 * @return the gpsHError
	 */
	public Integer getGpsHError() {
		return gpsHError;
	}
	/**
	 * @param gpsHError the gpsHError to set
	 */
	public void setGpsHError(Integer gpsHError) {
		this.gpsHError = gpsHError;
	}
	/**
	 * @return the gpsVError
	 */
	public Integer getGpsVError() {
		return gpsVError;
	}
	/**
	 * @param gpsVError the gpsVError to set
	 */
	public void setGpsVError(Integer gpsVError) {
		this.gpsVError = gpsVError;
	}
	/**
	 * @return the baroAlt
	 */
	public Double getBaroAlt() {
		return baroAlt;
	}
	/**
	 * @param baroAlt the baroAlt to set
	 */
	public void setBaroAlt(Double baroAlt) {
		this.baroAlt = baroAlt;
	}
	/**
	 * @return the sonarAlt
	 */
	public Double getSonarAlt() {
		return sonarAlt;
	}
	/**
	 * @param sonarAlt the sonarAlt to set
	 */
	public void setSonarAlt(Double sonarAlt) {
		this.sonarAlt = sonarAlt;
	}
	/**
	 * @return the currVolts
	 */
	public Double getCurrVolts() {
		return currVolts;
	}
	/**
	 * @param currVolts the currVolts to set
	 */
	public void setCurrVolts(Double currVolts) {
		this.currVolts = currVolts;
	}
	/**
	 * @return the currMah
	 */
	public Double getCurrMah() {
		return currMah;
	}
	/**
	 * @param currMah the currMah to set
	 */
	public void setCurrMah(Double currMah) {
		this.currMah = currMah;
	}
	/**
	 * @return the gpsTimestampMS
	 */
	public long getStateTimestampMS() {
		return stateTimestampMS;
	}
	/**
	 * @param gpsTimestampMS the gpsTimestampMS to set
	 */
	public void setStateTimestampMS(long stateTimestampMS) {
		this.stateTimestampMS = stateTimestampMS;
	}
	/**
	 * @return the unitHostAddress
	 */
	public String getUnitHostAddress() {
		return unitHostAddress;
	}
	/**
	 * @param unitHostAddress the unitHostAddress to set
	 */
	public void setUnitHostAddress(String unitHostAddress) {
		this.unitHostAddress = unitHostAddress;
	}
	/**
	 * @return the unitCallbackPort
	 */
	public String getUnitCallbackPort() {
		return unitCallbackPort;
	}
	/**
	 * @param unitCallbackPort the unitCallbackPort to set
	 */
	public void setUnitCallbackPort(String unitCallbackPort) {
		this.unitCallbackPort = unitCallbackPort;
	}

	/**
	 * @return the airSpeed
	 */
	public Double getAirSpeed() {
		return airSpeed;
	}

	/**
	 * @param airSpeed the airSpeed to set
	 */
	public void setAirSpeed(Double airSpeed) {
		this.airSpeed = airSpeed;
	}

	/**
	 * @return the gpsTime
	 */
	public String getGpsTime() {
		return gpsTime;
	}

	/**
	 * @param gpsTime the gpsTime to set
	 */
	public void setGpsTime(String gpsTime) {
		this.gpsTime = gpsTime;
	}

	/**
	 * @return the gpsStatus
	 */
	public String getGpsStatus() {
		return gpsStatus;
	}

	/**
	 * @param gpsStatus the gpsStatus to set
	 */
	public void setGpsStatus(String gpsStatus) {
		this.gpsStatus = gpsStatus;
	}

	/**
	 * @return the gpsLastStatusMS
	 */
	public long getGpsLastStatusMS() {
		return gpsLastStatusMS;
	}

	/**
	 * @param gpsLastStatusMS the gpsLastStatusMS to set
	 */
	public void setGpsLastStatusMS(long gpsLastStatusMS) {
		this.gpsLastStatusMS = gpsLastStatusMS;
	}

	/**
	 * @return the currVoltsLevel
	 */
	public Double getCurrVoltsLevel() {
		return currVoltsLevel;
	}

	/**
	 * @param currVoltsLevel the currVoltsLevel to set
	 */
	public void setCurrVoltsLevel(Double currVoltsLevel) {
		this.currVoltsLevel = currVoltsLevel;
	}

	/**
	 * @return the homeLatLon
	 */
	public String getHomeLatLon() {
		return homeLatLon;
	}

	/**
	 * @param homeLatLon the homeLatLon to set
	 */
	public void setHomeLatLon(String homeLatLon) {
		this.homeLatLon = homeLatLon;
	}

	/**
	 * @return the homeAlt
	 */
	public Double getHomeAlt() {
		return homeAlt;
	}

	/**
	 * @param homeAlt the homeAlt to set
	 */
	public void setHomeAlt(Double homeAlt) {
		this.homeAlt = homeAlt;
	}

	/**
	 * @return the heading
	 */
	public Integer getHeading() {
		return heading;
	}

	/**
	 * @param heading the heading to set
	 */
	public void setHeading(Integer heading) {
		this.heading = heading;
	}

	/**
	 * @return the gpsLat
	 */
	public Double getGpsLat() {
		return gpsLat;
	}

	/**
	 * @param gpsLat the gpsLat to set
	 */
	public void setGpsLat(Double gpsLat) {
		this.gpsLat = gpsLat;
	}

	/**
	 * @return the gpsLon
	 */
	public Double getGpsLon() {
		return gpsLon;
	}

	/**
	 * @param gpsLon the gpsLon to set
	 */
	public void setGpsLon(Double gpsLon) {
		this.gpsLon = gpsLon;
	}

	/**
	 * @return the homeLat
	 */
	public Double getHomeLat() {
		return homeLat;
	}

	/**
	 * @param homeLat the homeLat to set
	 */
	public void setHomeLat(Double homeLat) {
		this.homeLat = homeLat;
	}

	/**
	 * @return the homeLon
	 */
	public Double getHomeLon() {
		return homeLon;
	}

	/**
	 * @param homeLon the homeLon to set
	 */
	public void setHomeLon(Double homeLon) {
		this.homeLon = homeLon;
	}

	/**
	 * @return the status
	 */
	public String getStatus() {
		return status;
	}

	/**
	 * @param status the status to set
	 */
	public void setStatus(String status) {
		this.status = status;
	}

	/**
	 * @return the operatingAlt
	 */
	public Integer getOperatingAlt() {
		return operatingAlt;
	}

	/**
	 * @param operatingAlt the operatingAlt to set
	 */
	public void setOperatingAlt(Integer operatingAlt) {
		this.operatingAlt = operatingAlt;
	}

	/**
	 * @return the operatingSpeed
	 */
	public Integer getOperatingSpeed() {
		return operatingSpeed;
	}

	/**
	 * @param operatingSpeed the operatingSpeed to set
	 */
	public void setOperatingSpeed(Integer operatingSpeed) {
		this.operatingSpeed = operatingSpeed;
	}

}

