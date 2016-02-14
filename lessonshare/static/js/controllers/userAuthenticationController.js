(function () {
    'use strict';

    var injectDeps = ['$location', '$localStorage', '$rootScope', 'UserAuthService', 'ToastService'];

    var UserAuthCtrl = function ($location, $localStorage, $rootScope, UserAuthService, ToastService) {
        var self = this;
        self.user = {
            firstName: '',
            lastName: '',
            email: '',
            password: ''
        };

        self.register = function () {
            UserAuthService.registerUser({
                first_name: self.user.firstName,
                last_name: self.user.lastName,
                email: self.user.email,
                password: self.user.password
            })
                .then(function (result) {
                    $location.path('/');
                })
                .catch(function (error) {
                    ToastService.setParamsAndDisplay(error.data.description, 'warning-toast', '#userRegisterForm');
                });
        };

        self.login = function () {
            UserAuthService.loginUser({
                email: self.user.email,
                password: self.user.password
            })
                .then(function (result) {
                    var parsedToken = UserAuthService.parseToken(result.data.access_token);

                    $localStorage.token = result.data.access_token;
                    $localStorage.userFirstName = parsedToken.first_name;
                    $rootScope.$broadcast('userLoggedIn');
                    $location.path('/');
                })
                .catch(function (error) {
                    ToastService.setParamsAndDisplay(error.data.description, 'warning-toast', '#userLoginForm');
                });
        };

        self.logout = function () {
            delete $localStorage.token;
            delete $localStorage.userFirstName;
            $rootScope.$broadcast('userLoggedOut');
            $location.path('/');
        };
    };

    UserAuthCtrl.$inject = injectDeps;

    angular.module('LessonShareApp').controller('UserAuthController', UserAuthCtrl);
})();
