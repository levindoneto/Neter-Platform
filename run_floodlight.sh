echo "RUNNING FLOODLIGHT CONTROLLER ON PORT 8110";
cd sdn-controller/;
#nohup java -jar target/floodlight.jar &
java -jar target/floodlight.jar;
cd ..;
