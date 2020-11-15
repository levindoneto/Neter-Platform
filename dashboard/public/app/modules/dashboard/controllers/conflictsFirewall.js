dashboard.controller(
    'conflictsFirewallController', [
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
            const verifications = firebase.database().ref(`/users/${$scope.userId}/verifications/`);
            const verificationsList = $firebaseArray(verifications);
            const verificationsObj = $firebaseObject(verifications);
            verificationsList.$loaded().then(() => {
                $scope.verifications = verificationsList;
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
