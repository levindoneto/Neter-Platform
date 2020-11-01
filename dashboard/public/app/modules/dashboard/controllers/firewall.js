dashboard.controller(
    'firewallController', [
        '$scope',
        '$firebaseObject',
        '$firebaseArray',
        function (
            $scope,
            $firebaseObject,
            $firebaseArray
        ) {
            const vm = this;
            
            const firewall = firebase.database().ref(`/users/${userId}/firewall/`);
            const firewallList = $firebaseArray(topologies);
            const firewallObj = $firebaseObject(topologies);
            firewallList.$loaded().then(() => {
                $scope.userFirewall = firewallList;
            });
        }
    ]
);
