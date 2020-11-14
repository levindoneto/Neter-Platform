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
                $scope.Photo = user.Photo;
                $scope.id = user.$id;
            };
            $scope.editFormSubmit = function (userId, username, photo) {
                const refUser = firebase.database().ref(`users/${userId}`);
                const auxUserUsername = {};
                auxUserUsername.Username = username;
                auxUserUsername.Photo = photo;
                refUser.update(auxUserUsername);
                swal({
                    title: 'Your profile information has been successfully modified!',
                    icon: 'success',
                    timer: 3000,
                    button: false
                });
            };
        }
    ]
);
