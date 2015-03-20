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
    var url_root = '/schedule/2015/';
    var url = url_root + (date.getMonth() + 1); // Date() is based on 0-index.
    $http.get(url)
      .success(function (data) {
        $scope.schedule = [];
        angular.forEach(data, function(game) {
          var today = new Date();
          var gameDate = new Date(game.time);

          // games are stored in Eastern time; getUTCDate will give us that
          // value back... works...
          if (today.getDate() <= gameDate.getUTCDate()) {
            $scope.schedule.push(game);
          }
        });
      })
      .error(function (data) {
        console.log(data);
      });
    url = url_root + (date.getMonth() + 2);
    $http.get(url)
      .success(function (data) {
        $scope.schedule.push.apply($scope.schedule, data);
      })
      .error(function (data) {
        console.log(data);
      });
  });
})();