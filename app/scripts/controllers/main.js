'use strict';

angular.module('belizeorchidsApp')
    .controller('MainCtrl', function ($http, $scope) {
        $scope.orchids = [];

        var config = {
            method: 'GET',
            url: "http://localhost:27080/orchids/orchids/_find",
            params: {
                limit: "500",
                batch_size: "500"
            }
        }
        $http(config)
            .success(function(data, status, headers, config) {
                $scope.orchids = data.results;
                console.log("data: ", data);
            })
            .error(function(data, status, headers, config) {
                // do something
            })
  });
