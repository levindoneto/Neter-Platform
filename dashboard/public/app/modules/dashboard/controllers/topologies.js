dashboard.controller(
    'topologiesController', [
        '$scope',
        '$firebaseObject',
        '$firebaseArray',
        function (
            $scope,
            $firebaseObject,
            $firebaseArray
        ) {
            const vm = this;
            
            const topologies = firebase.database().ref(`/users/${userId}/topologies/`);
            const topologiesList = $firebaseArray(topologies);
            const topologiesObj = $firebaseObject(topologies);
            
            
            // TODO: Add topology
        }
    ]
);
