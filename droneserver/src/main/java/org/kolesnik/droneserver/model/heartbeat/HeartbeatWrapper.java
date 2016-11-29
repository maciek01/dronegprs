/**
 * 
 */
package org.kolesnik.droneserver.model.heartbeat;

import org.kolesnik.droneserver.model.common.Wrapper;

/**
 * @author mkolesnik
 *
 */
public class HeartbeatWrapper extends Wrapper {
	
	private Heartbeat heartbeat;
	
	/**
	 * @return the heartbeat
	 */
	public Heartbeat getHeartbeat() {
		return heartbeat;
	}
	/**
	 * @param heartbeat the heartbeat to set
	 */
	public void setHeartbeat(Heartbeat heartbeat) {
		this.heartbeat = heartbeat;
	}
}
