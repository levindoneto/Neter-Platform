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
                links: {} // 'h1': ['s1']
            };

            $scope.getCurrentOptionsHosts = function() {
                return {
                    's1': 's1',
                    's2': 's2'
                }
            };

            $scope.getCurrentOptionsSwitch = function() {
                return {
                    's1': 's1',
                    's2': 's2'
                }
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
                  title: 'Add Link for the Host ' + $scope.currentHostNumber,
                  input: 'select',
                  inputOptions: $scope.getCurrentOptionsHosts(),
                  inputPlaceholder: 'Select Device',
                  showCancelButton: true
                }).then(function (link) {
                    $scope.topology.hosts.push($scope.currentHostNumber);
                    $scope.topology.links['h'.concat(String($scope.currentHostNumber))] = [link];
                  swal({
                    type: 'success',
                    html: 'Host '.concat($scope.currentHostNumber, ' has been added'),
                  }).then(function() {
                    $scope.currentHostNumber += 1;
                    console.log($scope.topology);
                })
                })
            };

            $scope.addSwitch = function() {
                swal({
                  title: 'Add Link for the Switch ' + $scope.currentSwitchNumber,
                  input: 'select',
                  inputOptions: $scope.getCurrentOptionsSwitch(),
                  inputPlaceholder: 'Select Device',
                  showCancelButton: true
                }).then(function (link) {
                    $scope.topology.switches.push($scope.currentSwitchNumber);
                    $scope.topology.links['s'.concat(String($scope.currentSwitchNumber))] = [link];
                    swal({
                        type: 'success',
                        html: 'Switch '.concat($scope.currentSwitchNumber, ' has been added'),
                    }).then(function() {
                        $scope.currentSwitchNumber += 1;

                    })
                })
            };
        }
    ]
);
