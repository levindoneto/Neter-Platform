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
                $scope.topologiesObj = topologiesObj;
            });

            $scope.modal = function(id) {
                $scope.currentTopology = $scope.topologiesObj[id];
            }

            $scope.getLinks = function(links) {
                return JSON.stringify(links);
            }

            $scope.redirectToTopologies = function() {
                $state.go('app.topologies');
            };

            $scope.deploy = function(id) {
                $scope.currentTopology = $scope.topologiesObj[id];
                swal({
                    title: 'Are you sure you want to deploy topology '.concat($scope.currentTopology.fullName, '?'),
                    showCancelButton: true,
                    confirmButtonText: 'Yes',
                    cancelButtonText: 'Cancel',
                    showLoaderOnConfirm: true,
                    preConfirm: function(result) {
                        return new Promise(function(resolve, reject) {
                            if (result) {
                                axios.post('http://localhost:8060/mininet/start', {data:$scope.currentTopology})
                                .then(function(response) {
                                    var refTopology = firebase.database().ref(`users/${$scope.userId}/topologies`);
                                    var auxTopology = {};
                                    auxTopology.currentTopology = id;
                                    refTopology.update(auxTopology); // update current topology
                                    swal({
                                        title: 'The topology '.concat($scope.currentTopology.fullName, ' has been deployed successfully 😃'),
                                        text: 'To check it out, please click Ok',
                                        icon: 'success',
                                        showCancelButton: true,
                                        confirmButtonText: 'Ok',
                                        cancelButtonText: 'Cancel',
                                        timer: 5000
                                    }).then(function(ok) {
                                        $state.go('app.currentTopology');
                                    });
                                })
                                .catch(function(error){
                                    swal({
                                        title: 'Error on deploying topology '.concat($scope.currentTopology.fullName, ' 😞'),
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
            }
        }
    ]
);
