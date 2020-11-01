login.controller(
    'loginCtrl', [
        '$rootScope',
        '$scope',
        '$state',
        '$location',
        'loginService',
        'Flash',
        'apiService',
        '$firebaseAuth',
        '$firebaseObject',
        '$firebaseArray',
        function (
            $rootScope,
            $scope,
            $state,
            $location,
            loginService,
            Flash,
            apiService,
            $firebaseAuth,
            $firebaseObject,
            $firebaseArray
        ) {
            var vm = this;
            var auth = $firebaseAuth();
            vm.getUser = {};
            vm.setUser = {};
            vm.signIn = true;

            vm.login = function (data) {
                auth
                    .$signInWithEmailAndPassword(data.Email, data.Password)
                    .then(firebaseUser => {})
                    .catch(error => {
                        swal({
                            title: 'Incorrect login information, please try again',
                            text: "Wrong informed email or password",
                            icon: 'error',
                            button: true
                        });
                    });
            };

            //get registration details
            vm.register = function () {
                var refUsers = firebase.database().ref('users/');
                var userList = $firebaseArray(refUsers);
                var alreadyExist = false;

                userList.$loaded().then(() => {
                    if (!alreadyExist)
                        auth
                        .$createUserWithEmailAndPassword(
                            vm.setUser.Email,
                            vm.setUser.Password
                        )
                        .then(firebaseUser => {
                            var ref = firebase.database().ref(`users/${firebaseUser.uid}`);
                            var obj = $firebaseObject(ref);
                            obj.$bindTo($rootScope, 'user').then(() => {
                                vm.setUser.isAdmin = Boolean(false | vm.setUser.isAdmin);
                                $rootScope.user = vm.setUser;
                            });
                        })
                        .catch(error => {
                            Flash.create(
                                `Danger: Error with the register ->${error}`,
                                'large-text'
                            );
                        });
                });
            };

            auth.$onAuthStateChanged(firebaseUser => {
                if (firebaseUser) {
                    $state.go('app.account'); // Go to my account when the user is allowed to access the platform
                }
            });
        }
    ]
);
