dashboard.controller(
    'formalVerificationFlowtableController', [
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

            $scope.redirectToFormalVerification = function() {
                $state.go('app.formalVerification');
            };
        }
    ]
);
