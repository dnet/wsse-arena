#!/usr/bin/env python

curl --data-binary @source.txt --header 'Soapaction: ""' \
	--header 'Content-Type: text/xml; charset=utf-8' $ENDPOINT_URL
