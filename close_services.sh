echo "CLOSE MININET";
sudo mn -c;

echo "CLOSE FLOODLIGHT";
lsof -i :8010; # Find PID where Floodlight is running
#kill -9 <PID>
