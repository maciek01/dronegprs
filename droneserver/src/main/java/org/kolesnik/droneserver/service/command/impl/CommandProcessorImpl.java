/**
 * 
 */
package org.kolesnik.droneserver.service.command.impl;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentLinkedQueue;

import org.kolesnik.droneserver.model.command.ActionRequest;
import org.kolesnik.droneserver.model.command.ActionResponse;
import org.kolesnik.droneserver.service.command.CommandProcessor;

/**
 * simple command queue
 * @author mkolesnik
 *
 */
public class CommandProcessorImpl implements CommandProcessor {
	
	//TODO process to cleanup dead queues
	private Map<String, ConcurrentLinkedQueue<ActionRequest>> requestQueues = new HashMap<>();

	@Override
	public ActionResponse addActionRequest(ActionRequest actionRequest) {
		
		if (actionRequest == null || actionRequest.getUnitId() == null) {
			return null;//TODO return action response with a code
		}

		ConcurrentLinkedQueue<ActionRequest> queue = requestQueues.get(actionRequest.getUnitId());
		
		if (queue == null) {
			queue = new ConcurrentLinkedQueue<>();
			requestQueues.put(actionRequest.getUnitId(), queue);
		}
		
		queue.add(actionRequest);
		
		return null;
	}
	
	@Override
	public ActionRequest getActionRequest(String unitId) {
		ConcurrentLinkedQueue<ActionRequest> queue = requestQueues.get(unitId);
		if (queue == null) {
			return null;
		}
		
		return queue.poll();
	}
	
	@Override
	public synchronized ActionRequest[] listAllActionRequests(String unitId, boolean consume) {

		ConcurrentLinkedQueue<ActionRequest> queue = requestQueues.get(unitId);
		if (queue == null) {
			return null;
		}
		
		ActionRequest[] array = queue.toArray(new ActionRequest[queue.size()]);
		if (consume) {
			requestQueues.remove(unitId);
		}
		return array;
	}

}
