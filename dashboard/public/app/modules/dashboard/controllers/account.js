dashboard.controller(
    'accountController', [
        '$scope',
        function (
            $scope,
        ) {
            const vm = this;

            $scope.showAccountinfo = function (user) {
                $scope.show = true;
                $scope.Username = user.Username;
                $scope.Email = user.Email;
                $scope.addr = user.addr;
                $scope.id = user.$id;
            };
            $scope.editFormSubmit = function (userId, username) {
                const refUser = firebase.database().ref(`users/${userId}`);
                const auxUserUsername = {}; // isAdmin: Boolean
                auxUserUsername.Username = username;
                refUser.update(auxUserUsername);
                swal({
                    title: 'Your username has been modified successfully',
                    icon: 'success',
                    timer: 3000,
                    button: false
                });
            };
        }
    ]
);