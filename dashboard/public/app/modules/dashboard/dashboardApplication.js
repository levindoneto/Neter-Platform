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
        $stateProvider.state('app.myaccount', {
            url: '/myaccount',
            templateUrl: 'app/modules/dashboard/views/myaccount.html',
            controller: 'myaccountController',
            controllerAs: 'vm',
            data: {
                pageTitle: 'My Account'
            }
        });

        $stateProvider.state('app.mybelongings', {
            url: '/evaluations',
            templateUrl: 'app/modules/dashboard/views/mybelongings.html',
            controller: 'mybelongingsController',
            controllerAs: 'vm',
            data: {
                pageTitle: 'My Topologies'
            }
        });
    }
]);
