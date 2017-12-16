/**
 * 
 */
package org.kolesnik.droneserver.model.common;

import java.util.HashMap;
import java.util.Map;

/**
 * @author mkolesnik
 *
 */
public class ServiceContext {
	
	
	private Map<String, Object> attributes = new HashMap<>(); 
	

	/**
	 * get context attribute
	 * @param name attribute name
	 * @return attribute value
	 */
	public Object getAttribute(String name) {
		return attributes.get(name);
	}
	
	/**
	 * put context attribute
	 * @param name attribute name
	 * @param value attribute value
	 * @return previous attribute value or null if none
	 */
	public Object putAttribute(String name, Object value) {
		return attributes.put(name, value);
	}
}
