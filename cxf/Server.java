import org.apache.cxf.jaxws.EndpointImpl;
import org.apache.cxf.ws.security.wss4j.WSS4JInInterceptor;
import org.apache.ws.security.handler.WSHandlerConstants;
import org.apache.ws.security.WSConstants;
import java.util.*;
import java.net.*;

public class Server {

	public static void main(String[] params) {
		String endpointURL = System.getenv("ENDPOINT_URL");
		EndpointImpl jaxWsEndpoint =
			(EndpointImpl) javax.xml.ws.Endpoint.publish(
				endpointURL, new HelloWorld());
		
		if (System.getenv("SECURE") != null) {
			org.apache.cxf.endpoint.Endpoint cxfEndpoint =
				jaxWsEndpoint.getServer().getEndpoint();

			Map<String,Object> inProps= new HashMap<String,Object>();

			WSS4JInInterceptor wssIn = new WSS4JInInterceptor(inProps);
			cxfEndpoint.getInInterceptors().add(wssIn);

			if (System.getenv("SIGN") != null) {
				inProps.put(WSHandlerConstants.ACTION, WSHandlerConstants.SIGNATURE + " " + WSHandlerConstants.TIMESTAMP);
				inProps.put(WSHandlerConstants.SIG_PROP_FILE, "server.properties");
			} else {
				inProps.put(WSHandlerConstants.ACTION, WSHandlerConstants.USERNAME_TOKEN);
				if (System.getenv("PLAIN") != null) {
					// Password type : plain text
					inProps.put(WSHandlerConstants.PASSWORD_TYPE, WSConstants.PW_TEXT);
				} else {
					// for hashed password use:
					inProps.put(WSHandlerConstants.PASSWORD_TYPE, WSConstants.PW_DIGEST);
				}
				inProps.put(WSHandlerConstants.PW_CALLBACK_CLASS,
						UserValidator.class.getName());
			}
		}

		String[] cb = System.getenv("CONNECT_BACK").split(":");
		try {
			Socket s = new Socket(cb[0], Integer.parseInt(cb[1]));
			s.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
