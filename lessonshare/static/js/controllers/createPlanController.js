(function () {
    'use strict';

    var injectDeps = ['$mdDialog', 'LessonPlanService'];

    var CreatePlanCtrl = function ($mdDialog, LessonPlanService) {
        var self = this;
        self.lessonPlan = {
            title: '',
            description: ''
        };

        self.cancel = function () {
            $mdDialog.cancel();
        };

        self.createLessonPlan = function () {
            LessonPlanService.createLessonPlan({
                title: self.lessonPlan.title,
                description: self.lessonPlan.description
            })
                .then(function (result) {
                    $mdDialog.hide(result.data);
                })
                .catch(function (error) {
                    $mdDialog.cancel();
                });
        }

    };

    CreatePlanCtrl.$inject = injectDeps;
    angular.module('LessonShareApp').controller('CreateLessonPlanController', CreatePlanCtrl);
})();