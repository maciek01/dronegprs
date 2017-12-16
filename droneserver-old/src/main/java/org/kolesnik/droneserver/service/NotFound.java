/**
 * 
 */
package org.kolesnik.droneserver.service;

/**
 * @author mkolesnik
 *
 */
public class NotFound extends Exception {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	
	/**
	 * create exception with a message
	 * @param message
	 */
	public NotFound(String message) {
		super(message);
	}
	
	/**
	 * create exception with a message and cause
	 * @param message
	 * @param cause
	 */
	public NotFound(String message, Throwable cause) {
		super(message, cause);
	}

}
