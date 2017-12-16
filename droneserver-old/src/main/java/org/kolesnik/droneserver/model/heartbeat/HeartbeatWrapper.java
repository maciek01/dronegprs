/**
 * 
 */
package org.kolesnik.droneserver.model.heartbeat;

import org.kolesnik.droneserver.model.command.ActionRequest;
import org.kolesnik.droneserver.model.common.Wrapper;

/**
 * @author mkolesnik
 *
 */
public class HeartbeatWrapper extends Wrapper {
	
	private Heartbeat heartbeat;
	private ActionRequest[] actionRequests;
	
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
	/**
	 * @return the actionRequests
	 */
	public ActionRequest[] getActionRequests() {
		return actionRequests;
	}
	/**
	 * @param actionRequests the actionRequests to set
	 */
	public void setActionRequests(ActionRequest[] actionRequests) {
		this.actionRequests = actionRequests;
	}
}
