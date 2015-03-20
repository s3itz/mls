(function() {
  'use strict';

  var app = angular.module('mlsAggregator', []);

  app.controller('StandingsCtrl', function ($scope, $http) {
    $http.get('/standings').
      success(function (data, status, headers, config) {
        $scope.standings = data
        console.log(data)
      }).
      error(function (data, status, headers, config) {
        console.log('Error:', data)
      });
  });
})();