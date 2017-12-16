/**
 * 
 */
package org.kolesnik.droneserver.model.common;

/**
 * @author mkolesnik
 *
 */
public class Wrapper {
	
	private long id;
	private long receivedTimestampMS;
	
	
	/**
	 * @return the receivedTimestampMS
	 */
	public long getReceivedTimestampMS() {
		return receivedTimestampMS;
	}
	/**
	 * @param receivedTimestampMS the receivedTimestampMS to set
	 */
	public void setReceivedTimestampMS(long receivedTimestampMS) {
		this.receivedTimestampMS = receivedTimestampMS;
	}
	/**
	 * @return the id
	 */
	public long getId() {
		return id;
	}
	/**
	 * @param id the id to set
	 */
	public void setId(long id) {
		this.id = id;
	}
	

}
