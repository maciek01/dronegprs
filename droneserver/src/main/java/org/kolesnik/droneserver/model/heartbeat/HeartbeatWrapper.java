/**
 * 
 */
package org.kolesnik.droneserver.model.heartbeat;

import org.kolesnik.droneserver.model.command.Command;
import org.kolesnik.droneserver.model.common.Wrapper;

/**
 * @author mkolesnik
 *
 */
public class HeartbeatWrapper extends Wrapper {
	
	private Heartbeat heartbeat;
	private Command[] commands;
	
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
	 * @return the commands
	 */
	public Command[] getCommands() {
		return commands;
	}
	/**
	 * @param commands the commands to set
	 */
	public void setCommands(Command[] commands) {
		this.commands = commands;
	}
}
