/**
 * 
 */
package org.kolesnik.droneserver.service.heartbeat.impl;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

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
	
	private AtomicLong idCounter = new AtomicLong(0);
	
	
	
	@Override
	public HeartbeatWrapper createHeartbeat(Heartbeat heartbeat) {
		
		HeartbeatWrapper wrapper = new HeartbeatWrapper();
		wrapper.setReceivedTimestampMS(System.currentTimeMillis());
		wrapper.setHeartbeat(heartbeat);
		wrapper.setId(idCounter.incrementAndGet());//generate request id
		
		activeUnits.put(heartbeat.getUnitId(), wrapper);
		
		return wrapper;
	}
	
	
	@Override
	public HeartbeatsWrapper listHeartbeats() {
		HeartbeatsWrapper wrapper = new HeartbeatsWrapper();
		wrapper.setHeartbeats(activeUnits.values().toArray(new HeartbeatWrapper[activeUnits.size()]));
		
		return wrapper;
	}
	

	@Override
	public HeartbeatWrapper getHeartbeat(Heartbeat key) {
		return activeUnits.get(key.getUnitId());
	}

}
