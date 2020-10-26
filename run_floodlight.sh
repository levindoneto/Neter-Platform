echo "RUNNING FLOODLIGHT CONTROLLER ON PORT 8110";
cd sdn-controller/;
#nohup java -jar target/floodlight.jar &
ant;
java -jar target/floodlight.jar;
cd ..;
