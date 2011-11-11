CLASSES=$(shell ls *.java | sed s/java/class/)
CXF=$(shell stat --format %n apache-cxf-*)
JARS=$(shell ls $(CXF)/lib{/endorsed,}/*.jar | tr '\n' ' ')
CLASSPATH=$(shell echo '$(JARS)' | tr ' ' ':').
JAVAC=javac -cp $(CLASSPATH)
JAVA=java -cp $(CLASSPATH)
ALLCLASS=*.class

all: $(CLASSES)

%.class: %.java
	$(JAVAC) $<

runserver: Server.class
	$(JAVA) Server

runclient: Client.class
	$(JAVA) Client

service:
	JAVA_HOME=$(shell readlink -f $(shell which javac) | sed 's/bin.*$$//') \
		$(CXF)/bin/wsdl2java -frontend jaxws21 'http://localhost:8080/ur/?wsdl'

clean:
	rm -rf $(ALLCLASS) hu

.PHONY: clean all runserver runclient service
