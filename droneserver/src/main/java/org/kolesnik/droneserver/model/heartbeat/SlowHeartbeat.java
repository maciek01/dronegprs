/* */
package org.kolesnik.droneserver.model.heartbeat;

/**
 * 
 * @author mkolesnik
 *
 */
public class SlowHeartbeat {
	
	private String unitId;
	
	private String unitHostAddress;	//server side
	private String unitCallbackPort;//1/30 Hz expected reporting
	
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
		this.unitId = unitId;			//1 Hz expected reporting
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

}

