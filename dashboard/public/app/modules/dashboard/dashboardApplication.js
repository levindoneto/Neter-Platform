var dashboard = angular.module('dashboard', [
    'ui.router',
    'ngAnimate',
    'ngMaterial',
    'firebase',
]);
dashboard.factory('notification', ($firebaseArray, $firebaseObject) => ({
    send: function (message, user) {
        const ref = firebase.database().ref(`users/${user}`);
        const userDB = $firebaseObject(ref);
        userDB.$loaded().then(() => {
            userDB.haveNotification = true;
            userDB.$save().then(
                ref => {},
                error => {
                    console.log('Error:', error);
                }
            );
        });
    }
}));

dashboard.config([
    '$stateProvider',
    function ($stateProvider) {
        $stateProvider.state('app.account', {
            url: '/account',
            templateUrl: 'app/modules/dashboard/views/account.html',
            controller: 'accountController',
            controllerAs: 'vm',
            data: {
                pageTitle: 'Account'
            }
        });

        $stateProvider.state('app.controller', {
            url: '/controller',
            templateUrl: 'app/modules/dashboard/views/controller.html',
            controller: 'controllerController',
            controllerAs: 'vm',
            data: {
                pageTitle: 'SDN Controller'
            }
        });

        $stateProvider.state('app.firewall', {
            url: '/firewall',
            templateUrl: 'app/modules/dashboard/views/firewall.html',
            controller: 'firewallController',
            controllerAs: 'vm',
            data: {
                pageTitle: 'Firewall'
            }
        });

        $stateProvider.state('app.topologies', {
            url: '/topologies',
            templateUrl: 'app/modules/dashboard/views/topologies.html',
            controller: 'topologiesController',
            controllerAs: 'vm',
            data: {
                pageTitle: 'Topologies'
            }
        });

        $stateProvider.state('app.savedTopologies', {
            url: '/savedtopologies',
            templateUrl: 'app/modules/dashboard/views/savedTopologies.html',
            controller: 'savedTopologiesController',
            controllerAs: 'vm',
            data: {
                pageTitle: 'Saved Topologies'
            }
        });

        $stateProvider.state('app.currentTopology', {
            url: '/currenttopology',
            templateUrl: 'app/modules/dashboard/views/currentTopology.html',
            controller: 'currentTopologyController',
            controllerAs: 'vm',
            data: {
                pageTitle: 'Current Topology'
            }
        });

        $stateProvider.state('app.addTopology', {
            url: '/addTopology',
            templateUrl: 'app/modules/dashboard/views/addTopology.html',
            controller: 'addTopologyController',
            controllerAs: 'vm',
            data: {
                pageTitle: 'Add Topology'
            }
        });

        $stateProvider.state('app.formalVerification', {
            url: '/formalVerification',
            templateUrl: 'app/modules/dashboard/views/formalVerification.html',
            controller: 'formalVerificationController',
            controllerAs: 'vm',
            data: {
                pageTitle: 'Formal Verification'
            }
        });

        $stateProvider.state('app.conflictsRedundanciesFlowtable', {
            url: '/conflictsredundanciesflowtable',
            templateUrl: 'app/modules/dashboard/views/conflictsRedundanciesFlowtable.html',
            controller: 'conflictsRedundanciesFlowtableController',
            controllerAs: 'vm',
            data: {
                pageTitle: 'Formal Verification | Conflicts and Redundancies | Flowtable'
            }
        });

        $stateProvider.state('app.conflictsRedundanciesFirewall', {
            url: '/conflictsredundanciesfirewall',
            templateUrl: 'app/modules/dashboard/views/conflictsRedundanciesFirewall.html',
            controller: 'conflictsRedundanciesFirewallController',
            controllerAs: 'vm',
            data: {
                pageTitle: 'Formal Verification | Conflicts and Redundancies | Firewall'
            }
        });

        $stateProvider.state('app.reachability', {
            url: '/reachability',
            templateUrl: 'app/modules/dashboard/views/reachability.html',
            controller: 'reachabilityController',
            controllerAs: 'vm',
            data: {
                pageTitle: 'Reachability'
            }
        });
    }
]);
