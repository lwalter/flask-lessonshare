(function () {
    'use strict';

    var injectDeps = ['$scope', '$mdDialog', 'LessonPlanService', 'ToastService'];

    var LessonPlanCtrl = function ($scope, $mdDialog, LessonPlanService, ToastService) {
        var self = this;
        self.selected = null;
        self.lessonPlans = [];
        self.isEditing = false;

        self.lessonItem = null;
        self.lessonItems = [];

        // Load initial data.
        LessonPlanService.getLessonPlans()
            .then(function (result) {
                self.lessonPlans = result.data;
                self.selected = self.lessonPlans[0];

                if (self.selected) {
                     LessonPlanService.getLessonItems(self.selected.id)
                         .then(function (result) {
                            self.lessonItems = result.data;
                        })
                        .catch(function (error) {
                            ToastService.setParamsAndDisplay(error.data.description, 'warning-toast', '#content');
                        })
                }
            })
            .catch(function (error) {
                ToastService.setParamsAndDisplay(error.data.description, 'warning-toast', '#content');
            });

        self.selectPlan = function (index) {
            if (self.isEditing) {
                // TODO(lnw) Display confirmation, if T: change selected, else: stay
                self.isEditing = false;
            }

            self.selected = angular.isNumber(index) ? self.lessonPlans[index] : null;
        };

        self.deleteLessonPlan = function (event) {
            var confirmDialog = $mdDialog.confirm()
              .title('Are you sure?')
              .textContent('All lesson items related to this plan will be deleted.')
              .ariaLabel('Delete')
              .targetEvent(event)
              .ok('Delete')
              .cancel('Cancel');

            $mdDialog.show(confirmDialog)
                .then(function () {
                    LessonPlanService.deleteLessonPlan(self.selected.id)
                        .then(function (result) {
                            self.lessonPlans = result.data;
                            self.selected = self.lessonPlans[0];
                        })
                        .catch(function (error) {
                            // TODO(lnw) parent HTML element should change
                            ToastService.setParamsAndDisplay(error.data.description, 'warning-toast', '#content');
                        });
                });
        };

        self.editLessonPlan = function () {
            self.isEditing = true;
        };

        self.submitEditLessonPlan = function () {
            LessonPlanService.editLessonPlan(self.selected)
                .then(function (result) {
                    self.selected = result.data;
                    self.isEditing = false;
                })
                .catch(function (error) {
                    ToastService.setParamsAndDisplay(error.data.description, 'warning-toast', '#editLessonPlanForm');
                });
        };

        self.insertLessonItem = function () {
            LessonPlanService.insertLessonItem(self.lessonItem, self.selected.id)
                .then(function (result) {
                    self.lessonItems = result.data;
                })
                .catch(function (error) {
                    ToastService.setParamsAndDisplay(error.data.description, 'warning-toast', '#content');
                });
        };

        self.showDialog = function (event) {
            $mdDialog.show({
                controller: 'CreateLessonPlanController',
                controllerAs: 'createCtrl',
                templateUrl: 'static/views/lesson-plans/create-lesson-plan.html',
                parent: angular.element(document.body),
                targetEvent: event,
                clickOutsideToClose: false,
                fullscreen: false
            })
                .then(function (planList) {
                    self.lessonPlans = planList;
                    self.selected = self.lessonPlans[0];
                });
        };
    };

    LessonPlanCtrl.$inject = injectDeps;

    angular.module('LessonShareApp').controller('LessonPlanController', LessonPlanCtrl);
})();
