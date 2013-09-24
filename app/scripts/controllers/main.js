'use strict';

angular.module('belizeorchidsApp')
    .controller('MainCtrl', function ($http, $scope) {
        $scope.orchids = [];
        $scope.orchid_counts = {}
        var db = 'http://localhost:27080/orchids';

        var config = {
            method: 'GET',
            url: db + "/orchids/_find",
            params: {
                limit: "500",
                batch_size: "500"
            }
        }

        $scope.get_counts = function(name) {
            console.log("name: ", name);
            console.log('{"name": ' + name + '}')
            var config = {
                method: 'GET',
                url: db + "/thumbs/_find",
                params: {
                    criteria: JSON.stringify({"name": name})
                }
            };
            $http(config)
                .success(function(data, status, headers, config) {
                    console.log("config: ", config);
                    console.log("data: ", data);
                    $scope.orchid_counts[name] = data.results.length
                })
                .error(function(data, status, headers, config) {
                    // do something
                })
        }

        $http(config)
            .success(function(data, status, headers, config) {
                $scope.orchids = data.results;
                data.results.forEach(function(orchid) {
                    $scope.get_counts(orchid.name);
                });
                //console.log("data: ", data);
            })
            .error(function(data, status, headers, config) {
                // do something
            })
  });
