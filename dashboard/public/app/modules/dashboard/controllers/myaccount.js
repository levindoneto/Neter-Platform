dashboard.controller(
    'myaccountController', [
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

            $scope.updateAdminInfoDB = function (userId, isAdmin) {
                const refUser = firebase.database().ref(`users/${userId}`);
                const auxUserAdmin = {}; // isAdmin: Boolean
                auxUserAdmin.isAdmin = isAdmin;
                refUser.update(auxUserAdmin);
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
