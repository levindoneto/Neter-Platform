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
            const verifications = firebase.database().ref(`/users/${$scope.userId}/verifications/flowtable/conflicts`);
            const verificationsList = $firebaseArray(verifications);
            const verificationsObj = $firebaseObject(verifications);
            verificationsList.$loaded().then(() => {
                $scope.verifications = verificationsList;
                $scope.verificationsObj = verificationsObj;
            });

            const topologies = firebase.database().ref(`/users/${$scope.userId}/topologies/`);
            const topologiesList = $firebaseArray(topologies);
            const topologiesObj = $firebaseObject(topologies);
            topologiesList.$loaded().then(() => {
                $scope.topologies = topologiesObj;
                $scope.currentTopologyId = topologiesObj.currentTopologyId;
                $scope.currentTopology = topologiesObj[$scope.currentTopologyId];
            });

            $scope.modal = function(id) {
                $scope.currentVerification = $scope.verificationsObj[id];
            };

            $scope.redirectToFormalVerification = function() {
                $state.go('app.formalVerification');
            };

            $scope.redirectToFormalVerificationFlowtable = function() {
                $state.go('app.formalVerificationFlowtable');
            };

            $scope.verifyRulesFlowtable = function() {
                swal({
                    title: "Name the Verification",
                    text: "The name is used as a verification identifier",
                    input: 'text',
                    showCancelButton: true,
                    inputPlaceholder: 'Verification '.concat(verificationsList.length + 1)
                }).then(function(inputValue) {
                    swal({
                        title: 'Are you sure you want to verify conflicts in the flowtables of the topology '.concat($scope.currentTopology.fullName, '?'),
                        showCancelButton: true,
                        confirmButtonText: 'Yes',
                        cancelButtonText: 'Cancel',
                        showLoaderOnConfirm: true,
                        preConfirm: function(result) {
                            return new Promise(function(resolve, reject) {
                                if (result) {
                                    axios.get('http://dawntech.brazilsouth.cloudapp.azure.com:8060/rules/flowtable/conflicts')
                                    .then(function(response){
                                        // save db
                                        response.data.name = inputValue;
                                        verificationsList.$add(response.data).then((verificationId) => {
                                            auxVid = verificationId.toString().split('/');
                                            verificationId = auxVid[auxVid[auxVid.length-1]];
                                            swal({
                                                title: 'The flowtables from the topology '.concat($scope.currentTopology.fullName, ' have been successfully verified!'),
                                                text: (response.data.status).concat('\n', 'To check out the details, please check the verification history'),
                                                icon: 'success',
                                                showCancelButton: true,
                                                confirmButtonText: 'Ok',
                                                cancelButtonText: 'Cancel',
                                                timer: 10000
                                            }).then(function(ok) {
                                                $scope.modal(verificationId);
                                            });
                                        });
                                    })
                                    .catch(function(error){
                                        swal({
                                            title: 'Error on verifying conflicts in the flowtables of the topology '.concat($scope.currentTopology.fullName),
                                            text: 'Please check its details and try again.',
                                            icon: 'error',
                                            button: false,
                                            timer: 5000
                                        });
                                    })
                                }
                            });
                        },
                        allowOutsideClick: () => !swal.isLoading(),
                    });
                });
            };
        }
    ]
);
