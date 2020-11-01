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

        $stateProvider.state('app.addtopology', {
            url: '/addtopology',
            templateUrl: 'app/modules/dashboard/views/addtopology.html',
            controller: 'addtopologyController',
            controllerAs: 'vm',
            data: {
                pageTitle: 'Add Topology'
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
    }
]);
