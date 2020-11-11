dashboard.controller(
    'addtopologyController', [
        '$scope',
        '$firebaseObject',
        '$firebaseArray',
        function (
            $scope,
            $firebaseObject,
            $firebaseArray
        ) {
            const vm = this;
            $scope.currentHostNumber = $scope.currentHostNumber? $scope.currentHostNumber: 1;
            $scope.currentSwitchNumber = $scope.currentSwitchNumber? $scope.currentSwitchNumber: 1;
            $scope.topology = $scope.topology? $scope.topology: {
                hosts: [], // numbers
                switches: [], // numbers
                autoSetMacs: false,
                ip: '127.0.0.1',
                links: {}, // 'h1': ['s1'],
                availableOptions: {} // 's1': 's1'
            };

            $scope.getCurrentOptionsHosts = function(hostNumber) {
                var auxOptions = $scope.topology.availableOptions;
                delete auxOptions['h'.concat(String(hostNumber))]; // to avoid link from hostY to hostY
                
                return 0 !== Object.keys(auxOptions).length?auxOptions:undefined;
            };

            $scope.getCurrentOptionsSwitch = function(switchNumber) {
                var auxOptions = $scope.topology.availableOptions;
                delete auxOptions['s'.concat(String(switchNumber))]; // to avoid link from switchY to switchY
                
                return 0 !== Object.keys(auxOptions).length?auxOptions:undefined;
            };
            
            $scope.getNewLinkOptionsHosts = function(host) {
                var auxOptions = $scope.topology.availableOptions;
                delete auxOptions[host]; // to avoid link from hostY to hostY
                for (var i = 0; i < $scope.topology.links[host].length; i++) {
                    delete auxOptions[$scope.topology.links[host][i]];
                }
                
                return 0 !== Object.keys(auxOptions).length?auxOptions:undefined;
            };
            
            $scope.getNewLinkOptionsSwitches = function(switchDevice) {
                var auxOptions = $scope.topology.availableOptions;
                delete auxOptions[switchDevice]; // to avoid link from hostY to hostY
                for (var i = 0; i < $scope.topology.links[switchDevice].length; i++) {
                    delete auxOptions[$scope.topology.links[switchDevice][i]];
                }
                
                return 0 !== Object.keys(auxOptions).length?auxOptions:undefined;
            };

            // const topologies = firebase.database().ref(`/users/${userId}/topologies/`);
            // const topologiesList = $firebaseArray(topologies);
            // const topologiesObj = $firebaseObject(topologies);
            // topologiesList.$loaded().then(() => {
            //     $scope.userTopologies = topologiesList;
            // });

            $scope.addTopology = function (hosts, switches, links, isDefault) {
                alert('addTopology to db and start it if isDefault==true');
            };

            $scope.addHost = function() {
                swal({
                  title: 'Add Link for Host ' + $scope.currentHostNumber,
                  input: 'select',
                  inputOptions: $scope.getCurrentOptionsHosts(),
                  inputPlaceholder: 'Select Device',
                  showCancelButton: true
                }).then(function (link) {
                    $scope.topology.hosts.push($scope.currentHostNumber);
                    $scope.topology.links['h'.concat(String($scope.currentHostNumber))] = [link];
                    $scope.topology.availableOptions['h'.concat(String($scope.currentHostNumber))] = 'h'.concat(String($scope.currentHostNumber));
                  swal({
                    type: 'success',
                    html: 'Host '.concat($scope.currentHostNumber, ' has been added'),
                  }).then(function() {
                    $scope.currentHostNumber += 1;
                    $scope.$apply(); // start digestion
                    console.log($scope.topology);
                })
                })
            };

            $scope.addSwitch = function() {
                swal({
                  title: 'Add Link for Switch ' + $scope.currentSwitchNumber,
                  input: 'select',
                  inputOptions: $scope.getCurrentOptionsSwitch(),
                  inputPlaceholder: 'Select Device',
                  showCancelButton: true
                }).then(function (link) {
                    $scope.topology.switches.push($scope.currentSwitchNumber);
                    $scope.topology.links['s'.concat(String($scope.currentSwitchNumber))] = [link];
                    $scope.topology.availableOptions['s'.concat(String($scope.currentSwitchNumber))] = 's'.concat(String($scope.currentSwitchNumber));
                    swal({
                        type: 'success',
                        html: 'Switch '.concat($scope.currentSwitchNumber, ' has been added'),
                    }).then(function() {
                        $scope.currentSwitchNumber += 1;
                        $scope.$apply(); // start digestion
                    })
                })
            };

            $scope.addNewLink = function(device) {
                if ('h' == device.charAt(0).toLowerCase()) {
                    $scope.addNewLinkHost(device);
                } else {
                    $scope.addNewLinkSwitch(device);
                }
            };

            $scope.addNewLinkHost = function(host) {
                swal({
                  title: 'Add Link for Host ' + host,
                  input: 'select',
                  inputOptions: $scope.getNewLinkOptionsHosts(host),
                  inputPlaceholder: 'Select Device',
                  showCancelButton: true
                }).then(function (link) {
                    $scope.topology.links[host].push(link);
                    swal({
                        type: 'success',
                        html: 'Device '.concat(link, ' has been added as a link to host ', host),
                    }).then(function() {
                        $scope.$apply(); // start digestion
                    })
                })
            };

            $scope.addNewLinkSwitch = function(switchDevice) {
                swal({
                  title: 'Add Link for Switch ' + switchDevice,
                  input: 'select',
                  inputOptions: $scope.getNewLinkOptionsSwitches(switchDevice),
                  inputPlaceholder: 'Select Device',
                  showCancelButton: true
                }).then(function (link) {
                    $scope.topology.links[switchDevice].push(link);
                    swal({
                        type: 'success',
                        html: 'Device '.concat(link, ' has been added as a link to switch ', switchDevice),
                    }).then(function() {
                        $scope.$apply(); // start digestion
                    })
                })
            };
        }
    ]
);
