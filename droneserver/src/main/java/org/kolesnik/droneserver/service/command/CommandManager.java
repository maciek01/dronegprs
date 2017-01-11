/**
 * 
 */
package org.kolesnik.droneserver.service.command;

import org.kolesnik.droneserver.model.command.Command;

/**
 * @author mkolesnik
 *
 */
public interface CommandManager {
	
	
	/**
	 * post command
	 * @param command
	 */
	void createCommand(Command command);
	

}
