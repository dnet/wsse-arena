import javax.jws.WebMethod;
import javax.jws.WebService;
import java.util.*;

@WebService(targetNamespace = "http://vsza.hu/bme")
public class HelloWorld {

	@WebMethod()
	public String[] say_hello(String name, int times) {
		Collection<String> retval = new ArrayList<String>(times);
		String hello = "Hello, " + name;
		for (int i = 0; i < times; i++) {
			retval.add(hello);
		}
		return retval.toArray(new String[0]);
	}

}
