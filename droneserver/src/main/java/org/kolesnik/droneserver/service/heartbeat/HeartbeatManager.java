/**
 * 
 */
package org.kolesnik.droneserver.service.heartbeat;

import org.kolesnik.droneserver.model.heartbeat.Heartbeat;
import org.kolesnik.droneserver.model.heartbeat.HeartbeatWrapper;
import org.kolesnik.droneserver.model.heartbeat.HeartbeatsWrapper;

/**
 * @author mkolesnik
 *
 */
public interface HeartbeatManager {
	/**
	 * 
	 * @param heartbeat
	 * @return
	 */
	public HeartbeatWrapper createHeartbeat(Heartbeat heartbeat);
	
	/**
	 * 
	 * @return
	 */
	public HeartbeatsWrapper listHeartbeats();

	/**
	 * 
	 * @param heartbeat
	 * @return
	 */
	public HeartbeatWrapper getHeartbeat(Heartbeat heartbeat);
}
