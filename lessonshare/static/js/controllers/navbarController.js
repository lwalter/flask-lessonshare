(function () {
    'use strict';

    var injectDeps = ['$scope', '$localStorage'];

    var NavbarCtrl = function ($scope, $localStorage) {
        var self = this;
        self.currentUser = $localStorage.userFirstName;

        $scope.$on('userLoggedIn', function () {
            self.currentUser = $localStorage.userFirstName;
        });

        $scope.$on('userLoggedOut', function () {
            self.currentUser = null;
        });

        self.userLoggedIn = function () {
            return !!$localStorage.userFirstName;
        }
    };

    NavbarCtrl.$inject = injectDeps;

    angular.module('LessonShareApp').controller('NavbarController', NavbarCtrl);
})();
