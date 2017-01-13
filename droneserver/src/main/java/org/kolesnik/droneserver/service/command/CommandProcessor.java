/**
 * 
 */
package org.kolesnik.droneserver.service.command;

import org.kolesnik.droneserver.model.command.ActionRequest;
import org.kolesnik.droneserver.model.command.ActionResponse;

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
	 * 
	 * @param unitId
	 * @return action request
	 */
	ActionRequest[] getAllActionRequests(String unitId);
	

}
