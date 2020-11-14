dashboard.controller(
    'formalVerificationController', [
        '$scope',
        '$state',
        function (
            $scope,
            $state,
        ) {
            const vm = this;

            $scope.redirectToConflictsFlowtable = function() {
                $state.go('app.conflictsFlowtable');
            };

            $scope.redirectToRedundanciesFlowtable = function() {
                $state.go('app.redundanciesFlowtable');
            };

            $scope.redirectToConflictsFirewall = function() {
                $state.go('app.conflictsFirewall');
            };

            $scope.redirectToRedundanciesFirewall = function() {
                $state.go('app.redundanciesFirewall');
            };

            $scope.redirectToReachability = function() {
                $state.go('app.reachability');
            };
        }
    ]
);
