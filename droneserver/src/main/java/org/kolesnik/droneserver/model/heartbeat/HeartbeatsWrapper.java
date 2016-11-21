/**
 * 
 */
package org.kolesnik.droneserver.model.heartbeat;

import org.kolesnik.droneserver.model.common.Wrapper;

/**
 * @author mkolesnik
 *
 */
public class HeartbeatsWrapper extends Wrapper {
	
	private HeartbeatWrapper[] heartbeats;
	
	/**
	 * @return the heartbeats
	 */
	public HeartbeatWrapper[] getHeartbeats() {
		return heartbeats;
	}
	/**
	 * @param heartbeats the heartbeats to set
	 */
	public void setHeartbeats(HeartbeatWrapper[] heartbeats) {
		this.heartbeats = heartbeats;
	}
}
