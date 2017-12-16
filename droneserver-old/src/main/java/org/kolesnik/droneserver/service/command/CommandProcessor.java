/**
 * 
 */
package org.kolesnik.droneserver.service.command;

import org.kolesnik.droneserver.model.command.ActionRequest;
import org.kolesnik.droneserver.model.command.ActionResponse;
import org.kolesnik.droneserver.service.NotFound;

/**
 * @author mkolesnik
 *
 */
public interface CommandProcessor {
	
	
	/**
	 * post action request
	 * @param action request
	 */
	ActionResponse addActionRequest(ActionRequest actionRequest);
	
	/**
	 * 
	 * @param unitId
	 * @return action request
	 */
	ActionRequest getActionRequest(String unitId);
	
	/**
	 * list pending action requests for specified unit
	 * @param unitId
	 * @param consume if true - empty the queue
	 * @return action request
	 */
	ActionRequest[] listAllActionRequests(String unitId, boolean consume) throws NotFound;

	/**
	 * Remove command queue for specified unit
	 * @param unitId unit id
	 */
	void removeAllActionRequests(String unitId) throws NotFound;

}
