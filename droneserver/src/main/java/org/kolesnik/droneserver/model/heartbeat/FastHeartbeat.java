/* */
package org.kolesnik.droneserver.model.heartbeat;

/**
 * 
 * @author mkolesnik
 *
 */
public class FastHeartbeat {
	
	private String unitId;
	
	private String gpsLatLong;		//1 Hz expected reporting
	private String gpsAlt;			//1 Hz expected reporting
	private String gpsSpeed;		//1 Hz expected reporting
	private long gpsTimestampMS;	//1 Hz expected reporting
	
	
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
	 * @return the gpsTimestampMS
	 */
	public long getGpsTimestampMS() {
		return gpsTimestampMS;
	}
	/**
	 * @param gpsTimestampMS the gpsTimestampMS to set
	 */
	public void setGpsTimestampMS(long gpsTimestampMS) {
		this.gpsTimestampMS = gpsTimestampMS;
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

