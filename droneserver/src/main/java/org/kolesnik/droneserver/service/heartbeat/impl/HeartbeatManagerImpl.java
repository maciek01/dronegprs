/**
 * 
 */
package org.kolesnik.droneserver.service.heartbeat.impl;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

import org.kolesnik.droneserver.Main;
import org.kolesnik.droneserver.model.heartbeat.Heartbeat;
import org.kolesnik.droneserver.model.heartbeat.HeartbeatWrapper;
import org.kolesnik.droneserver.model.heartbeat.HeartbeatsWrapper;
import org.kolesnik.droneserver.service.heartbeat.HeartbeatManager;

/**
 * @author mkolesnik
 *
 */
public class HeartbeatManagerImpl implements HeartbeatManager {
	
	
	private Map<String, HeartbeatWrapper> activeUnits= new HashMap<>();
	
	//TODO replace with database
	private AtomicLong idCounter = new AtomicLong(0);
	
	
	@Override
	public HeartbeatWrapper createHeartbeat(Heartbeat heartbeat) {

		spark.Request request = (spark.Request)Main.SERVICE_CONTEXT.get().getAttribute(Main.ATTR_HTTP_REQUEST);
		heartbeat.setUnitHostAddress(request.ip());
		
		HeartbeatWrapper lastHeartbeat = activeUnits.get(heartbeat.getUnitId());
		
		
		if (lastHeartbeat == null) {
			lastHeartbeat = new HeartbeatWrapper();
			lastHeartbeat.setId(idCounter.incrementAndGet());//generate request id
			lastHeartbeat.setReceivedTimestampMS(System.currentTimeMillis());
			lastHeartbeat.setHeartbeat(heartbeat);
			
			
			activeUnits.put(heartbeat.getUnitId(), lastHeartbeat);
		} else {
			Heartbeat currentHeartbeat = new Heartbeat();
			
			currentHeartbeat.update(lastHeartbeat.getHeartbeat());
			currentHeartbeat.update(heartbeat);
			
			lastHeartbeat.setId(idCounter.incrementAndGet());//generate request id
			lastHeartbeat.setReceivedTimestampMS(System.currentTimeMillis());
			lastHeartbeat.setHeartbeat(currentHeartbeat);
		}
		
		//fetch commands from the command queue
		lastHeartbeat.setActionRequests(Main.commandProcessorInstance.getAllActionRequests(heartbeat.getUnitId()));
		
		return lastHeartbeat;
	}
	
	
	@Override
	public HeartbeatsWrapper listHeartbeats() {
		HeartbeatsWrapper wrapper = new HeartbeatsWrapper();
		wrapper.setHeartbeats(activeUnits.values().toArray(new HeartbeatWrapper[activeUnits.size()]));
		
		return wrapper;
	}
	

	@Override
	public HeartbeatWrapper getHeartbeat(String key) {
		return activeUnits.get(key);
	}

}
