(function () {
    'use strict';

    var injectDeps = ['$mdToast', 'message'];

    var ToastCtrl = function ($mdToast, message) {
        var self = this;

        self.message = message;

        self.messageExists = function () {
            return !!self.message;
        };

        self.closeToast = function () {
            $mdToast.hide();
        }
    };

    ToastCtrl.$inject = injectDeps;

    angular.module('LessonShareApp').controller('ToastController', ToastCtrl);
})();