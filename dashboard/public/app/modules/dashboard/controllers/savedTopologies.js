dashboard.controller(
    'savedTopologiesController', [
        '$scope',
        '$firebaseObject',
        '$firebaseArray',
        '$rootScope',
        function (
            $scope,
            $firebaseObject,
            $firebaseArray,
            $rootScope
        ) {
            const vm = this;
            $scope.userId = $rootScope.userDB?$rootScope.userDB.uid: localStorage.loggedUser;
            const topologies = firebase.database().ref(`/users/${$scope.userId}/topologies/`);
            const topologiesList = $firebaseArray(topologies);
            const topologiesObj = $firebaseObject(topologies);
            topologiesList.$loaded().then(() => {
                $scope.topologies = topologiesList;
            });

            
            // TODO: Add topology
        }
    ]
);
