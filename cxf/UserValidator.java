import java.io.IOException;
import javax.security.auth.callback.*;
import org.apache.ws.security.WSPasswordCallback;

public class UserValidator implements CallbackHandler {

	public void handle(Callback[] callbacks) throws IOException, 
        UnsupportedCallbackException {

	    WSPasswordCallback pc = (WSPasswordCallback) callbacks[0];
		String username = pc.getIdentifier();
		if (username.equals("admin")) {
			pc.setPassword("nimda");
		}
	}

}
