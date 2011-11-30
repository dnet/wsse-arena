import org.apache.cxf.frontend.ClientProxy;
import org.apache.cxf.ws.security.wss4j.WSS4JOutInterceptor;
import org.apache.ws.security.handler.WSHandlerConstants;
import org.apache.ws.security.WSConstants;
import java.util.*;
import hu.vsza.bme.*;
import java.io.IOException;
import javax.security.auth.callback.*;
import org.apache.ws.security.WSPasswordCallback;

public class Client implements CallbackHandler {

	public static void main(String[] params) {
		HelloWorldService hws = new HelloWorldService();
		hu.vsza.bme.HelloWorld hw = hws.getHelloWorldPort();
		if (System.getenv("SECURE") != null) {
			org.apache.cxf.endpoint.Client client = ClientProxy.getClient(hw);
			org.apache.cxf.endpoint.Endpoint cxfEndpoint = client.getEndpoint();

			Map<String,Object> outProps= new HashMap<String,Object>();

			WSS4JOutInterceptor wssOut = new WSS4JOutInterceptor(outProps);
			cxfEndpoint.getOutInterceptors().add(wssOut);

			if (System.getenv("SIGN") != null) {
				outProps.put(WSHandlerConstants.ACTION, WSHandlerConstants.SIGNATURE +
						" " + WSHandlerConstants.TIMESTAMP);
				outProps.put(WSHandlerConstants.USER, "myAlias");
				outProps.put(WSHandlerConstants.SIG_PROP_FILE, "client_sign.properties");
			} else {
				outProps.put(WSHandlerConstants.ACTION, WSHandlerConstants.USERNAME_TOKEN);
				// Specify our username
				outProps.put(WSHandlerConstants.USER, "admin");
				if (System.getenv("PLAIN") != null) {
					// Password type : plain text
					outProps.put(WSHandlerConstants.PASSWORD_TYPE, WSConstants.PW_TEXT);
				} else {
					// for hashed password use:
					outProps.put(WSHandlerConstants.PASSWORD_TYPE, WSConstants.PW_DIGEST);
				}
				// Callback used to retrieve password for given user.
			}
			outProps.put(WSHandlerConstants.PW_CALLBACK_CLASS,
				Client.class.getName());
		}
		String times_env = System.getenv("TIMES");
		int times = times_env == null ? 1 : Integer.parseInt(times_env);
		for (int i = 0; i < times; i++) {
			System.out.print("[");
			for (String s : hw.sayHello("World", 3)) {
				System.out.print(s);
				System.out.print(", ");
			}
			System.out.println("]");
		}
	}

	public void handle(Callback[] callbacks) throws IOException, 
        UnsupportedCallbackException {

        WSPasswordCallback pc = (WSPasswordCallback) callbacks[0];

        // set the password for our message.
        pc.setPassword(System.getenv("SIGN") != null ? "myAliasPassword" : "nimda");
    }

}
