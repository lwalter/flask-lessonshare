(function () {
    'use strict';

    var deps = [
        'ngRoute',
        'ngMaterial',
        'ngStorage',
        'ngMessages'
    ];
    var lessonShareApp = angular.module('LessonShareApp', deps);

    lessonShareApp.config(function ($interpolateProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
    });

    lessonShareApp.config(['$routeProvider', '$locationProvider', '$httpProvider', function ($routeProvider, $locationProvider, $httpProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'static/views/home.html'
            })
            .when('/register', {
                templateUrl: 'static/views/user/register.html',
                controller: 'UserAuthController',
                controllerAs: 'uaCtrl'
            })
            .when('/login', {
                templateUrl: 'static/views/user/login.html',
                controller: 'UserAuthController',
                controllerAs: 'uaCtrl'
            })
            .when('/logout', {
                controller: 'UserAuthController',
                controllerAs: 'uaCtrl'
            })
            .when('/lesson-plans', {
                templateUrl: 'static/views/lesson-plans/lesson-plans.html',
                controller: 'LessonPlanController',
                controllerAs: 'lpCtrl'
            })
            .otherwise({
                templateUrl: 'static/views/404.html'
            });

        $locationProvider.html5Mode(true);

        function interceptors($q, $location, $localStorage, $injector) {
            return {
                request: function (config) {
                    config.headers = config.headers || {};

                    if ($localStorage.token) {
                        config.headers.Authorization = 'JWT ' + $localStorage.token;
                    }

                    return config;
                },
                responseError: function (response) {
                    if (!$localStorage.userFirstName && (response.status === 401 || response.status === 403)) {
                        var ToastService = $injector.get('ToastService');
                        delete $localStorage.userFirstName;
                        ToastService.setToastParams('You must be logged in to do that.', 'warning-toast', "#userLoginForm");
                        $location.path('/login');
                        return $q.reject(response);
                    }

                    return $q.resolve(response);
                }
            }
        }

        var interceptorDeps = ['$q', '$location', '$localStorage', '$injector', interceptors];
        $httpProvider.interceptors.push(interceptorDeps);
    }]);
})();