dashboard.controller(
    'redundanciesFirewallController', [
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
            const verifications = firebase.database().ref(`/users/${$scope.userId}/verifications/firewall/redundancies`);
            const verificationsList = $firebaseArray(verifications);
            const verificationsObj = $firebaseObject(verifications);
            verificationsList.$loaded().then(() => {
                $scope.verifications = verificationsList;
            });

            const topologies = firebase.database().ref(`/users/${$scope.userId}/topologies/`);
            const topologiesList = $firebaseArray(topologies);
            const topologiesObj = $firebaseObject(topologies);
            topologiesList.$loaded().then(() => {
                $scope.topologies = topologiesObj;
                console.log($scope.topologies);
            });

            $scope.verifyRulesFirewall = function() {
                return true;
            };

            $scope.redirectToFormalVerification = function() {
                $state.go('app.formalVerification');
            };

            $scope.redirectToFormalVerificationFirewall = function() {
                $state.go('app.formalVerificationFirewall');
            };
        }
    ]
);
