dashboard.controller(
    'formalVerificationController', [
        '$scope',
        '$state',
        function (
            $scope,
            $state,
        ) {
            const vm = this;

            $scope.redirectToConflictsRedundanciesFlowtable = function() {
                $state.go('app.conflictsRedundanciesFlowtable');
            };

            $scope.redirectToConflictsRedundanciesFirewall = function() {
                $state.go('app.conflictsRedundanciesFirewall');
            };

            $scope.redirectToReachability = function() {
                $state.go('app.reachability');
            };
        }
    ]
);
