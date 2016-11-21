/* */
package org.kolesnik.droneserver.model.heartbeat;

/**
 * 
 * @author mkolesnik
 *
 */
public class MediumHeartbeat {
	
	private String unitId;
	
	private String gpsNumSats;		//1/5 Hz expected reporting
	private String gpsLock;			//1/5 Hz expected reporting
	private String gpsHError;		//1/5 Hz expected reporting
	private String gpsVError;		//1/5 Hz expected reporting
	
	private String baroAlt;			//1/5 Hz expected reporting
	private String sonarAlt;		//1/5 Hz expected reporting
	
	private String currVolts;		//1/5 Hz expected reporting
	private String currMah;			//1/5 Hz expected reporting
	
	private String unitHostAddress;	//server side
	
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
}

