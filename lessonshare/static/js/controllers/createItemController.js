(function () {
    'use strict';

    var injectDeps = ['$mdDialog', 'LessonPlanService', 'planId'];

    var CreateItemCtrl = function ($mdDialog, LessonPlanService, planId) {
        var self = this;
        self.lessonItem = {
            title: '',
            content: ''
        };
        self.planId = planId;

        self.cancel = function () {
            $mdDialog.cancel();
        };

        self.createLessonItem = function () {
            LessonPlanService.insertLessonItem(self.lessonItem, self.planId)
                .then(function (result) {
                    $mdDialog.hide(result.data);
                })
                .catch(function (error) {
                    $mdDialog.cancel();
                });
        };
    };

    CreateItemCtrl.$inject = injectDeps;
    angular.module('LessonShareApp').controller('CreateLessonItemController', CreateItemCtrl);

})();