PUBSTORE=publicstore.jks
PRIVSTORE=privatestore.jks
PRIV12=privkey.p12
PRIVPEM=privkey.pem
PUBPEM=pubkey.pem
STOREPASS=keyStorePassword
KEYPASS=myAliasPassword
KEYTOOL=keytool
OPENSSL=openssl
ALIAS=myAlias
CN=Arena

all: $(PUBSTORE) $(PRIVPEM)

$(PRIVPEM): $(PRIV12)
	$(OPENSSL) pkcs12 -in $< -out $@ -passin pass:$(STOREPASS) -nodes

$(PRIV12): $(PRIVSTORE) # from http://www.swview.org/node/191
	$(KEYTOOL) -importkeystore -srckeystore $< -destkeystore $@ -srcstoretype JKS \
		-deststoretype PKCS12 -srcstorepass $(STOREPASS) -deststorepass $(STOREPASS) \
		-srcalias $(ALIAS) -destalias $(ALIAS) -srckeypass $(KEYPASS) \
		-destkeypass $(KEYPASS) -noprompt

$(PUBSTORE): $(PUBPEM)
	$(KEYTOOL) -import -alias $(ALIAS) -storepass $(STOREPASS) \
		-keystore $@ -file $< -rfc -noprompt

$(PUBPEM): $(PRIVSTORE)
	$(KEYTOOL) -export -alias $(ALIAS) -storepass $(STOREPASS) \
		-keystore $< -file $@ -rfc

$(PRIVSTORE):
	$(KEYTOOL) -genkey -alias $(ALIAS) -dname "CN=$(CN)" -keypass $(KEYPASS) \
		-storepass $(STOREPASS) -keystore $@
	$(KEYTOOL) -selfcert -alias $(ALIAS) -keypass $(KEYPASS) \
		-storepass $(STOREPASS) -keystore $@

clean:
	rm -f $(PUBSTORE) $(PRIVPEM) $(PRIVSTORE) $(PRIV12) $(PUBPEM)

.PHONY: clean all
