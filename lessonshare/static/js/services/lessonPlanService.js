(function () {
    'use strict';

    var injectDeps = ['$http', '$q'];

    var LessonPlanSrvc = function ($http, $q) {
        return {
            createLessonPlan: createLessonPlan,
            getLessonPlans: getLessonPlans,
            deleteLessonPlan: deleteLessonPlan,
            editLessonPlan: editLessonPlan,
            insertLessonItem: insertLessonItem,
            getLessonItems: getLessonItems,
            deleteLessonItem: deleteLessonItem
        };

        function getLessonPlans() {
            var deferred = $q.defer();

            $http.get('/api/lessonplans')
                .then(function (result) {
                    if (result.status === 200 && result.data) {
                        deferred.resolve(result)
                    } else {
                        deferred.reject(result)
                    }
                })
                .catch(function (error) {
                    deferred.reject(error);
                });

            return deferred.promise;
        }

        function createLessonPlan(newLessonPlan) {
            var deferred = $q.defer();

            $http.post('/api/lessonplans', newLessonPlan)
                .then(function (result) {
                    if (result.status === 201 && result.data) {
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

        function deleteLessonPlan(lessonPlanId) {
            var deferred = $q.defer();

            $http.delete('/api/lessonplans/' + lessonPlanId)
                .then(function (result) {
                    if (result.status === 200 && result.data) {
                        deferred.resolve(result);
                    } else {
                        deferred.reject(result);
                    }
                })
                .catch(function (error) {
                    deferred.reject(error)
                });

            return deferred.promise;
        }

        function editLessonPlan(lessonPlan) {
            var deferred = $q.defer();

            $http.put('/api/lessonplans/' + lessonPlan.id, lessonPlan)
                .then(function (result) {
                    if (result.status === 200 && result.data) {
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

        function getLessonItems(lessonPlanId) {
            // TODO(lnw) these deferred really need to be refactored...

            var deferred = $q.defer();

            $http.get('/api/lessonitems/' + lessonPlanId)
                .then(function (result) {
                    if (result.status === 200 && result.data) {
                        deferred.resolve(result);
                    } else {
                        deferred.reject(result);
                    }
                })
                .catch(function (error) {
                    deferred.reject(error)
                });

            return deferred.promise;
        }

        function insertLessonItem(newLessonItem, lessonPlanId) {
            var deferred = $q.defer();

            $http.post('/api/lessonitems/' + lessonPlanId, newLessonItem)
                .then(function (result) {
                    if (result.status === 201 && result.data) {
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

        function deleteLessonItem(lessonItemId) {
            var deferred = $q.defer();

            $http.delete('/api/lessonitems/' + lessonItemId)
                .then(function (result) {
                    if (result.status === 200 && result.data) {
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

    };

    LessonPlanSrvc.$inject = injectDeps;

    angular.module('LessonShareApp').factory('LessonPlanService', LessonPlanSrvc);
})();