(function () {
  'use strict';

  var app = angular.module('mlsAggregator', []);

  app.controller('StandingsCtrl', function ($scope, $http) {
    $http.get('/standings')
      .success(function (data) {
        $scope.standings = data;
      })
      .error(function (data) {
        console.log('Error:', data)
      });
  });

  app.controller('ScheduleCtrl', function ($scope, $http) {
    var date = new Date();
    var url = '/schedule/2015/' + (date.getMonth() + 1);
    $http.get(url)
      .success(function (data) {
        $scope.schedule = data;
      })
      .error(function (data) {
        console.log(data);
      });
  });
})();