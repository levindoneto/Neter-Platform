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
            
            // const topologies = firebase.database().ref(`/users/${userId}/topologies/`);
            // const topologiesList = $firebaseArray(topologies);
            // const topologiesObj = $firebaseObject(topologies);
            // topologiesList.$loaded().then(() => {
            //     $scope.userTopologies = topologiesList;
            // });

            $scope.addTopology = function (hosts, switches, links, isDefault) {
                alert('addTopology to db and start it if isDefault==true');
            };
        }
    ]
);
