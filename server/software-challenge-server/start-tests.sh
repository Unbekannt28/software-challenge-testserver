#!/bin/sh
java -Dfile.encoding=UTF-8 -Dlogback.configurationFile=logback-tests.xml -jar test-client.jar "$@"