dashboard.controller(
    'formalVerificationTopologyController', [
        '$scope',
        '$state',
        function (
            $scope,
            $state,
        ) {
            const vm = this;

            $scope.redirectToReachability = function() {
                $state.go('app.reachability');
            };

            $scope.redirectToFormalVerification = function() {
                $state.go('app.formalVerification');
            };
        }
    ]
);
