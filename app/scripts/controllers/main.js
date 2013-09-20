'use strict';

angular.module('belizeorchidsApp')
    .controller('MainCtrl', function ($http, $scope) {
        $scope.orchids = [];
        // TODO: need to ad a view of the database with only the names
        var config = {
            method: 'GET',
            url: "http://brettatoms.iriscouch.com/orchids/_all_docs",
            q: "_include_docs"
        }
        $http(config)
            .success(function(data, status, headers, config) {
                var keys = [];
                data.rows.forEach(function(doc) {
                    keys.push(doc.key);
                })
                // console.log("$scope.orchids: ", $scope.orchids[0]);
                // console.log("keys: ", keys);

            })
            .error(function(data, status, headers, config) {

            })
  });
