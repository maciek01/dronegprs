/**
 * 
 */
import static spark.Spark.*;



/**
 * @author mkolesnik
 *
 */
public class HelloWorld {
    public static void main(String[] args) {
    	
    	
    	int maxThreads = 8;
    	int minThreads = 2;
    	int timeOutMillis = 30000;
    	
    	threadPool(maxThreads, minThreads, timeOutMillis);

    	
    	
    	port(8080);
    	
        get("/hello", (req, res) -> "Hello World");
        
        
        
        get("/hello/:name", (request, response) -> {
            return "Hello: " + request.params(":name") + " at " + request.ip();
        });
        
        
        
        
        
    }
}