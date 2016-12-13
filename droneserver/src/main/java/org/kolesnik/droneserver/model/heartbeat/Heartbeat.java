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
	private String gpsLatLong;
	private String gpsAlt;
	private String gpsSpeed;
	private String gpsTime;
	private String gpsStatus;
	private long gpsLastStatusMS;
	private String airSpeed;
	private String baroAlt;
	private String sonarAlt;
	
	//5 sec reporting
	private String gpsNumSats;
	private String gpsLock;
	private String gpsHError;
	private String gpsVError;
	
	
	private String currVolts;
	private String currMah;
	
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
		if (heartbeat.gpsLatLong != null) {
			this.gpsLatLong = heartbeat.gpsLatLong;
		}
		if (heartbeat.gpsAlt != null) {
			this.gpsAlt = heartbeat.gpsAlt;
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
		if (heartbeat.sonarAlt != null) {
			this.sonarAlt = heartbeat.sonarAlt;
		}
		if (heartbeat.currVolts != null) {
			this.currVolts = heartbeat.currVolts;
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
	 * @return the gpsLatLong
	 */
	public String getGpsLatLong() {
		return gpsLatLong;
	}
	/**
	 * @param gpsLatLong the gpsLatLong to set
	 */
	public void setGpsLatLong(String gpsLatLong) {
		this.gpsLatLong = gpsLatLong;
	}
	/**
	 * @return the gpsAlt
	 */
	public String getGpsAlt() {
		return gpsAlt;
	}
	/**
	 * @param gpsAlt the gpsAlt to set
	 */
	public void setGpsAlt(String gpsAlt) {
		this.gpsAlt = gpsAlt;
	}
	/**
	 * @return the gpsSpeed
	 */
	public String getGpsSpeed() {
		return gpsSpeed;
	}
	/**
	 * @param gpsSpeed the gpsSpeed to set
	 */
	public void setGpsSpeed(String gpsSpeed) {
		this.gpsSpeed = gpsSpeed;
	}
	/**
	 * @return the gpsNumSats
	 */
	public String getGpsNumSats() {
		return gpsNumSats;
	}
	/**
	 * @param gpsNumSats the gpsNumSats to set
	 */
	public void setGpsNumSats(String gpsNumSats) {
		this.gpsNumSats = gpsNumSats;
	}
	/**
	 * @return the gpsLock
	 */
	public String getGpsLock() {
		return gpsLock;
	}
	/**
	 * @param gpsLock the gpsLock to set
	 */
	public void setGpsLock(String gpsLock) {
		this.gpsLock = gpsLock;
	}
	/**
	 * @return the gpsHError
	 */
	public String getGpsHError() {
		return gpsHError;
	}
	/**
	 * @param gpsHError the gpsHError to set
	 */
	public void setGpsHError(String gpsHError) {
		this.gpsHError = gpsHError;
	}
	/**
	 * @return the gpsVError
	 */
	public String getGpsVError() {
		return gpsVError;
	}
	/**
	 * @param gpsVError the gpsVError to set
	 */
	public void setGpsVError(String gpsVError) {
		this.gpsVError = gpsVError;
	}
	/**
	 * @return the baroAlt
	 */
	public String getBaroAlt() {
		return baroAlt;
	}
	/**
	 * @param baroAlt the baroAlt to set
	 */
	public void setBaroAlt(String baroAlt) {
		this.baroAlt = baroAlt;
	}
	/**
	 * @return the sonarAlt
	 */
	public String getSonarAlt() {
		return sonarAlt;
	}
	/**
	 * @param sonarAlt the sonarAlt to set
	 */
	public void setSonarAlt(String sonarAlt) {
		this.sonarAlt = sonarAlt;
	}
	/**
	 * @return the currVolts
	 */
	public String getCurrVolts() {
		return currVolts;
	}
	/**
	 * @param currVolts the currVolts to set
	 */
	public void setCurrVolts(String currVolts) {
		this.currVolts = currVolts;
	}
	/**
	 * @return the currMah
	 */
	public String getCurrMah() {
		return currMah;
	}
	/**
	 * @param currMah the currMah to set
	 */
	public void setCurrMah(String currMah) {
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
	public String getAirSpeed() {
		return airSpeed;
	}

	/**
	 * @param airSpeed the airSpeed to set
	 */
	public void setAirSpeed(String airSpeed) {
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

}

