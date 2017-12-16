/**
 * This class models commands passed to UAV FC unit
 */
package org.kolesnik.droneserver.model.command;

/**
 * @author mkolesnik
 *
 */
public class Command {
	
	
	private String name;
	private CommandParameter[] parameters;
	/**
	 * @return the name
	 */
	public String getName() {
		return name;
	}
	/**
	 * @param name the name to set
	 */
	public void setName(String name) {
		this.name = name;
	}
	/**
	 * @return the parameters
	 */
	public CommandParameter[] getParameters() {
		return parameters;
	}
	/**
	 * @param parameters the parameters to set
	 */
	public void setParameters(CommandParameter[] parameters) {
		this.parameters = parameters;
	}
	

}
