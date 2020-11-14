dashboard.controller(
    'conflictsRedundanciesFlowtableController', [
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
            const verifications = firebase.database().ref(`/users/${$scope.userId}/verifications/`);
            const verificationsList = $firebaseArray(verifications);
            const verificationsObj = $firebaseObject(verifications);
            verificationsList.$loaded().then(() => {
                $scope.verifications = verificationsList;
            });

            $scope.verifyRulesFlowtable = function() {
                return true;
            };
        }
    ]
);
