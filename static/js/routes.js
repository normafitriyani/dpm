angular.module('app.routes', [])

.config(function($stateProvider, $urlRouterProvider) {

  // Ionic uses AngularUI Router which uses the concept of states
  // Learn more here: https://github.com/angular-ui/ui-router
  // Set up the various states which the app can be in.
  // Each state's controller can be found in controllers.js
  $stateProvider
    

      .state('diseasesPredictionApp', {
    url: '/index',
    templateUrl: 'templates/diseasesPredictionApp.html',
    controller: 'diseasesPredictionAppCtrl'
  })

  .state('diseasesPredictionApp2', {
    url: '/prediction',
    params: {
      risks: {},
      result: {}
    },
    templateUrl: 'templates/diseasesPredictionApp2.html',
    controller: 'diseasesPredictionApp2Ctrl'
  })

$urlRouterProvider.otherwise('/index')


});