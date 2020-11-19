dashboard.controller(
    'savedTopologiesController', [
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
            const topologies = firebase.database().ref(`/users/${$scope.userId}/topologies/`);
            const topologiesList = $firebaseArray(topologies);
            const topologiesObj = $firebaseObject(topologies);
            topologiesList.$loaded().then(() => {
                $scope.topologies = topologiesList;
            });

            $scope.getLinks = function(links) {
                return JSON.stringify(links);
            }

            $scope.redirectToTopologies = function() {
                $state.go('app.topologies');
            };
        }
    ]
);
