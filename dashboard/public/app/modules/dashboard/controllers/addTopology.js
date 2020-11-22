dashboard.controller(
    'addTopologyController', [
        '$scope',
        '$firebaseObject',
        '$firebaseArray',
        '$rootScope',
        '$state',
        function (
            $scope,
            $firebaseObject,
            $firebaseArray,
            $rootScope,
            $state
        ) {
            const vm = this;
            $scope.userId = $rootScope.userDB?$rootScope.userDB.uid: localStorage.loggedUser;
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

            $scope.getCurrentOptions = function(currentDevice) {
                var auxOptions = {};
                for (var i=0; i < Object.keys($scope.topology.availableOptions).length; i++) {
                    device = Object.keys($scope.topology.availableOptions)[i];
                    if(device != currentDevice)
                        auxOptions[device] = device;
                }
                
                return 0 !== Object.keys(auxOptions).length?auxOptions:undefined;
            };

            const topologies = firebase.database().ref(`/users/${$scope.userId}/topologies/`);
            const topologiesList = $firebaseArray(topologies);
            const topologiesObj = $firebaseObject(topologies);
            console.log('topologies: ', topologiesList);
            // topologiesList.$loaded().then(() => {
            //     $scope.userTopologies = topologiesList;
            // });

            $scope.addTopology = function () {
                swal({
                    title: "Name the Topology",
                    text: "The name is used as a topology identifier",
                    input: 'text',
                    showCancelButton: true,
                    inputPlaceholder: 'Topology '.concat(topologiesList.length)
                }).then(function(inputValue) {
                    $scope.topology.fullName = inputValue;
                    $scope.topology.name = inputValue.substr(0,24);
                    $scope.topology.when = (new Date()).toString();
                    topologiesList.$loaded().then(() => {
                        /* $add function:
                         * It creates a new record in the database and it adds the record to a 
                         * local synchronized array.
                         * This method returns a promise, which is resolved after the data has been 
                         * saved to the server. The promise resolves to the Firebase reference 
                         * for the newly added record, providing an easy access to its key. */
                        swal({
                            title: 'The topology '.concat(inputValue, ' has been added successfully 😃'),
                            text: 'To deploy it, please access the topologies page.',
                            icon: 'success',
                            button: false,
                            timer: 5000
                        });
                        topologiesList.$add($scope.topology).then(ref => {
                            console.log('Reference of the added to the db:\n', ref.toString());
                        });
                    });
                })
            };

            $scope.addHost = function() {
                swal({
                  title: 'Add Link for Host ' + $scope.currentHostNumber,
                  input: 'select',
                  inputOptions: $scope.getCurrentOptions(),
                  inputPlaceholder: 'Select Device',
                  showCancelButton: true
                }).then(function (link) {
                    $scope.topology.hosts.push($scope.currentHostNumber);
                    $scope.topology.links['h'.concat(String($scope.currentHostNumber))] = [link];
                    $scope.topology.availableOptions['h'.concat(String($scope.currentHostNumber))]
                        = 'h'.concat(String($scope.currentHostNumber));
                  swal({
                    type: 'success',
                    title: 'Host '.concat($scope.currentHostNumber, ' has been added'),
                    text: 'Please click Ok to confirm.',
                    showCancelButton: true
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
                  inputOptions: $scope.getCurrentOptions(),
                  inputPlaceholder: 'Select Device',
                  showCancelButton: true
                }).then(function (link) {
                    $scope.topology.switches.push($scope.currentSwitchNumber);
                    $scope.topology.links['s'.concat(String($scope.currentSwitchNumber))] = [link];
                    $scope.topology.availableOptions['s'.concat(String($scope.currentSwitchNumber))]
                        = 's'.concat(String($scope.currentSwitchNumber));
                    swal({
                        type: 'success',
                        title: 'Switch '.concat($scope.currentSwitchNumber, ' has been added'),
                        text: 'Please click Ok to confirm.',
                        showCancelButton: true
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
                  inputOptions: $scope.getCurrentOptions(host),
                  inputPlaceholder: 'Select Device',
                  showCancelButton: true
                }).then(function (link) {
                    $scope.topology.links[host].push(link);
                    swal({
                        type: 'success',
                        title: 'Device '.concat(link, ' has been added as a link to host ', host),
                        text: 'Please click Ok to confirm.',
                        showCancelButton: true
                    }).then(function() {
                        $scope.$apply(); // start digestion
                    })
                })
            };

            $scope.addNewLinkSwitch = function(switchDevice) {
                swal({
                  title: 'Add Link for Switch ' + switchDevice,
                  input: 'select',
                  inputOptions: $scope.getCurrentOptions(switchDevice),
                  inputPlaceholder: 'Select Device',
                  showCancelButton: true
                }).then(function (link) {
                    $scope.topology.links[switchDevice].push(link);
                    swal({
                        type: 'success',
                        title: 'Device '.concat(link, ' has been added as a link to switch ', switchDevice),
                        text: 'Please click Ok to confirm.',
                        showCancelButton: true
                    }).then(function() {
                        $scope.$apply(); // start digestion
                    })
                })
            };

            $scope.redirectToTopologies = function() {
                $state.go('app.topologies');
            };
        }
    ]
);
