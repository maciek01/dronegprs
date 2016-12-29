/**
 * 
 */
package org.kolesnik.droneserver;

import static spark.Spark.get;
import static spark.Spark.port;
import static spark.Spark.post;
import static spark.Spark.threadPool;

import java.io.IOException;
import java.io.StringWriter;

import org.kolesnik.droneserver.model.common.ServiceContext;
import org.kolesnik.droneserver.model.heartbeat.Heartbeat;
import org.kolesnik.droneserver.service.heartbeat.HeartbeatManager;
import org.kolesnik.droneserver.service.heartbeat.impl.HeartbeatManagerImpl;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import spark.Response;


/**
 * 
 * Starts the server, defines and dispatches http requests
 * 
 * @author mkolesnik
 *
 */
public class Main {
	
	public static final String ATTR_HTTP_REQUEST = "HTTP_REQUEST";
	public static final String ATTR_HTTP_RESPONSE = "HTTP_RESPONSE";
	
	private static final int HTTP_REQUEST_OK = 200;
	private static final int HTTP_REQUEST_CLIENT_ERROR = 400;
	private static final int HTTP_REQUEST_NOT_FOUND = 404;
	private static final int HTTP_REQUEST_SERVER_ERROR = 500;
	
	public static HeartbeatManager heartbeatManagerInstance = new HeartbeatManagerImpl();
	
	/** TLS context */
	public static final ThreadLocal<ServiceContext> SERVICE_CONTEXT = new ThreadLocal<ServiceContext>() {
		@Override
		protected ServiceContext initialValue() {
			return new ServiceContext();
		}
	};
	

	/**
	 * @param args
	 */
	public static void main(String[] args) {

    	//setup server
    	configure();

    	
        get("/ping", (req, res) -> "pong");
        
        
        /**
         * define heartbeat post handling
         */
        post("/heartbeat", (request, response) -> {
        	SERVICE_CONTEXT.get().putAttribute(ATTR_HTTP_REQUEST, request);
        	SERVICE_CONTEXT.get().putAttribute(ATTR_HTTP_RESPONSE, response);
            try {
				return processResponse(response, heartbeatManagerInstance.createHeartbeat(jsonToData(request.body(), Heartbeat.class)).getCommands());
            } catch (JsonParseException jpe) {
            	jpe.printStackTrace();
                response.status(HTTP_REQUEST_CLIENT_ERROR);
                return "BAD REQUEST";
            } catch (Exception ex) {
            	ex.printStackTrace();
            	response.status(HTTP_REQUEST_SERVER_ERROR);
            	return "SERVER ERROR";
            } finally {
            	SERVICE_CONTEXT.remove();
            }
            
        });
        
        /**
         * define heartbeats get handling - return active heartbeats from all units
         */
        get("/heartbeats", (request, response) -> {
            try {
            	response.header("Access-Control-Allow-Origin", "*");
        		return processResponse(response, heartbeatManagerInstance.listHeartbeats());
            } catch (Exception ex) {
            	ex.printStackTrace();
            	response.status(HTTP_REQUEST_SERVER_ERROR);
            	return "SERVER ERROR";
            }
        });     
        
        
        /**
         * define heartbeat get handling - for a specific unit
         */
        get("/heartbeat/:unitId", (request, response) -> {

            try {
            	response.header("Access-Control-Allow-Origin", "*");
            	
            	//TODO - dont leak model, base not found on an exception
        		Object heartbeat = heartbeatManagerInstance.getHeartbeat(request.params(":unitId"));
        		
        		if (heartbeat == null) {
        			response.status(HTTP_REQUEST_NOT_FOUND);
                	return "";
        		}
        		
				return processResponse(response, heartbeat);
            } catch (Exception ex) {
            	ex.printStackTrace();
            	response.status(HTTP_REQUEST_SERVER_ERROR);
            	return "SERVER ERROR";
            }
        });
        
        
        
	}



	/**
	 * @param response
	 * @param result
	 * @return
	 */
	private static <T> String processResponse(Response response, T data) {
		response.status(HTTP_REQUEST_OK);
		response.type("application/json");
		return dataToJson(data);
	}
	


	/**
	 * Generic string to object converter
	 * @param json
	 * @param type
	 * @return
	 * @throws IOException 
	 * @throws JsonMappingException 
	 * @throws JsonParseException 
	 */
	public static <T> T jsonToData(String json, Class<T> type) throws JsonParseException, JsonMappingException, IOException {
		
		ObjectMapper mapper = new ObjectMapper();
        T obj = mapper.readValue(json, type);
		
		return obj; 
	}
	
    public static <T> String dataToJson(T data) {
        try {
            ObjectMapper mapper = new ObjectMapper();
            mapper.enable(SerializationFeature.INDENT_OUTPUT);
            StringWriter sw = new StringWriter();
            mapper.writeValue(sw, data);
            return sw.toString();
        } catch (IOException e){
        	e.printStackTrace();
            throw new RuntimeException("IOException from a StringWriter?");
        }
    }

    /**
     * configure the server
     */
	private static void configure() {
		int maxThreads = 8;
    	int minThreads = 2;
    	int timeOutMillis = 30000;
    	
    	port(9090);
    	
    	threadPool(maxThreads, minThreads, timeOutMillis);
	}

}
