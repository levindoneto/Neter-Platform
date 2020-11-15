dashboard.controller(
    'formalVerificationController', [
        '$scope',
        '$state',
        function (
            $scope,
            $state,
        ) {
            const vm = this;

            $scope.redirectToFormalVerificationFlowtable = function() {
                $state.go('app.formalVerificationFlowtable');
            };

            $scope.redirectToFormalVerificationFirewall = function() {
                $state.go('app.formalVerificationFirewall');
            };

            $scope.redirectToFormalVerificationTopology = function() {
                $state.go('app.formalVerificationTopology');
            };

        }
    ]
);
