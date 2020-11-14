dashboard.controller(
    'currentTopologyController', [
        '$scope',
        '$state',
        function (
            $scope,
            $state
        ) {
            const vm = this;

            $scope.redirectToTopologies = function() {
                $state.go('app.topologies');
            };
        }
    ]
);
