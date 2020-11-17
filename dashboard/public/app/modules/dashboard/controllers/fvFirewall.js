dashboard.controller(
    'formalVerificationFirewallController', [
        '$scope',
        '$state',
        function (
            $scope,
            $state,
        ) {
            const vm = this;

            $scope.redirectToConflictsFirewall = function() {
                $state.go('app.conflictsFirewall');
            };

            $scope.redirectToRedundanciesFirewall = function() {
                $state.go('app.redundanciesFirewall');
            };

            $scope.redirectToFormalVerification = function() {
                $state.go('app.formalVerification');
            };
        }
    ]
);
