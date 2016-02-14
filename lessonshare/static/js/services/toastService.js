(function (){
    'use strict';

    var injectDeps = ['$rootScope', '$document', '$mdToast'];

    var ToastSrvc = function ($rootScope, $document, $mdToast) {
        var self = this;
        self.showToast = false;
        self.template = '';
        self.message = '';
        self.parent = '';

        var clearToastParams = function () {
            self.showToast = false;
            self.template = '';
            self.message = '';
            self.parent = '';
        };

        var setToastParams = function (message, template, parent) {
            self.showToast = true;
            self.template = template;
            self.message = message;
            self.parent = parent;
        };

        var displayToast = function () {
            $mdToast.show({
                controller: 'ToastController',
                controllerAs: 'tCtrl',
                templateUrl: 'static/views/toasts/' + self.template + '.html',
                hideDelay: 6000,
                position: 'bottom left right',
                locals: {
                    message: self.message
                },
                parent: $document[0].querySelector(self.parent)
            });

            clearToastParams();
        };

        var setParamsAndDisplay = function (message, template, parent) {
            setToastParams(message, template, parent);
            displayToast();
        };

        $rootScope.$on('$routeChangeSuccess', function () {
            if (self.showToast) {
                displayToast();
            }
        });

        return {
            displayToast: displayToast,
            clearToastParams: clearToastParams,
            setToastParams: setToastParams,
            setParamsAndDisplay: setParamsAndDisplay
        };
    };

    ToastSrvc.$inject = injectDeps;

    angular.module('LessonShareApp').factory('ToastService', ToastSrvc);
})();