dashboard.controller(
    'topologiesController', [
        '$scope',
        '$state',
        function (
            $scope,
            $state
        ) {
            const vm = this;

            $scope.redirectToSavedTopologies = function() {
                $state.go('app.savedTopologies');
            };

            $scope.redirectToCurrentTopology = function() {
                $state.go('app.currentTopology');
            };

            $scope.redirectToAddTopology = function() {
                $state.go('app.addTopology');
            };
        }
    ]
);
