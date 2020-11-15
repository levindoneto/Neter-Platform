dashboard.controller(
    'conflictsFlowtableController', [
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

            $scope.redirectToFormalVerification = function() {
                $state.go('app.formalVerification');
            };

            $scope.verifyRulesFlowtable = function() {
                var sweet_loader = '<div class="sweet_loader"><svg viewBox="0 0 140 140" width="140" height="140"><g class="outline"><path d="m 70 28 a 1 1 0 0 0 0 84 a 1 1 0 0 0 0 -84" stroke="rgba(0,0,0,0.1)" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"></path></g><g class="circle"><path d="m 70 28 a 1 1 0 0 0 0 84 a 1 1 0 0 0 0 -84" stroke="#71BBFF" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-dashoffset="200" stroke-dasharray="300"></path></g></svg></div>';
                var urlVerifyRulesFlowtable = 'http://dawntech.brazilsouth.cloudapp.azure.com8060/mininet/ping'
                $.ajax({
                    type: 'POST',
                    url:  urlVerifyRulesFlowtable,
                    data: str,
                    // here
                    beforeSend: function() {
                        swal.fire({
                            html: '<h5>Loading...</h5>',
                            showConfirmButton: false,
                            onRender: function() {
                                 // there will only ever be one sweet alert open.
                                 $('.swal2-content').prepend(sweet_loader);
                            }
                        });
                    },
                    success: function(json) {
                        try {
                            json = JSON.parse(json);
                        }
                        catch(error) {
                            swal.fire({
                                icon: 'error',
                                html: '<h5>Error!</h5>'
                            });
                            return false;
                        }
                        if(json.success) {
                            swal.fire({
                                icon: 'success',
                                html: '<h5>Success!</h5>'
                            });
                        } else {
                            swal.fire({
                                icon: 'error',
                                html: '<h5>Error!</h5>'
                            });
                        }
                    },
                    error: function() {
                        swal.fire({
                            icon: 'error',
                            html: '<h5>Error!</h5>'
                        });
                        return false;
                    }
                });
            };
        }
    ]
);
