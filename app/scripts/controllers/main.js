'use strict';

angular.module('belizeorchidsApp')
    .controller('MainCtrl', function ($http, $location, $scope) {
        $scope.orchids = [];
        $scope.detail_images = {};
        $scope.orchid_counts = {}
        $scope.searchText = "";

        var mongo_server = $location.host().indexOf("belizeorchids.com") >= 0 ?
            'http://mongodb.belizeorchids.com:27080' : 'http://localhost:27080',
            db = mongo_server + "/orchids",
            thumb_root = 'https://s3.amazonaws.com/belizeorchids.com/images/orchids/256x192/'

        $scope.show_index = -1;
        $scope.show_detail = function(index) {
            var name = $scope.orchids[index].name;
            $scope.show_index = index;
            $scope.detail_images[name] = [];
            $scope.orchids[index].thumbs.forEach(function(filename, thumb_index) {
                $scope.detail_images[name][thumb_index] = thumb_root + filename;
            });
        }

        // get the list of orchid names
        var config = {
            method: 'GET',
            url: db + "/orchids/_find",
            params: {
                limit: "500",
                batch_size: "500",
                sort: {name: 1}
            }
        }
        $http(config)
            .success(function(data, status, headers, config) {
                $scope.orchids = data.results;
            })
            .error(function(data, status, headers, config) {
                // do something
            });


        // return True/False is a name matched the search text
        $scope.searchedFor = function(name) {
            return $scope.searchText === "" || name.indexOf($scope.searchText)>=0
        }

  });
