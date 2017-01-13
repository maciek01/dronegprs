/**
 * 
 */
package org.kolesnik.droneserver.model.command;

/**
 * @author mkolesnik
 *
 */
public class ActionRequest {
	
	private String unitId;
	
	private Command command;

	/**
	 * @return the command
	 */
	public Command getCommand() {
		return command;
	}

	/**
	 * @param command the command to set
	 */
	public void setCommand(Command command) {
		this.command = command;
	}

	/**
	 * @return the unitId
	 */
	public String getUnitId() {
		return unitId;
	}

	/**
	 * @param unitId the unitId to set
	 */
	public void setUnitId(String unitId) {
		this.unitId = unitId;
	}

}
