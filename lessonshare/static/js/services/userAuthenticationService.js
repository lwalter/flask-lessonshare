(function () {
    'use strict';

    var injectDeps = ['$http', '$q', '$window'];

    var UserAuthSrvc = function ($http, $q, $window) {
        return {
            registerUser: registerUser,
            loginUser: loginUser,
            parseToken: parseToken
        };

        function registerUser(newUser) {
            var deferred = $q.defer();

            $http.post('/api/user', newUser)
                .then(function (result) {
                    if (result.status === 201) {
                        deferred.resolve(result);
                    } else {
                        deferred.reject(result);
                    }
                })
                .catch(function (error) {
                    deferred.reject(error);
                });

            return deferred.promise;
        }

        function loginUser(user) {
            var deferred = $q.defer();

            $http.post('/auth', user)
                .then(function (result) {
                    if (result.status === 200 && result.data.access_token) {
                        deferred.resolve(result);
                    } else {
                        deferred.reject(result);
                    }
                })
                .catch(function (error) {
                    deferred.reject(error);
                });

            return deferred.promise;
        }

        function parseToken(token) {
            var base64Url = token.split('.')[1];
            var base64 = base64Url.replace('-', '+').replace('_', '/');
            return JSON.parse($window.atob(base64));
        }
    };

    UserAuthSrvc.$inject = injectDeps;

    angular.module('LessonShareApp').factory('UserAuthService', UserAuthSrvc);

})();
