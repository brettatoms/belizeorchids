'use strict';

angular.module('belizeorchidsApp')
    .controller('MainCtrl', function ($http, $location, $scope) {
        $scope.orchids = [];
        $scope.detail_images = {};
        $scope.orchid_counts = {}
        $scope.searchText = "";

        var image_root = 'https://s3.amazonaws.com/belizeorchids.com/images/orchids/',
            thumb_root = image_root + '256x192/'

        $scope.show_index = -1;
        $scope.show_detail = function(name, index) {
            if(index == $scope.show_index) {
                // if we're already showing this one then collapse it
                $scope.show_index = -1;
                return;
            }
            $scope.show_index = index;
            $scope.detail_images[name] = [];
            $scope.orchids[name].images.forEach(function(filename, thumb_index) {
                $scope.detail_images[name][thumb_index] = thumb_root + filename;
            });
        }

        // get the list of orchid names
        var config = {
            method: 'GET',
            url: "/data/orchids.json",
        }
        $http(config)
            .success(function(data, status, headers, config) {
                $scope.orchids = data;
            })
            .error(function(data, status, headers, config) {
                // do something
            });


        // return True/False is a name matched the search text
        $scope.searchedFor = function(name) {
            return $scope.searchText === "" || name.search(new RegExp($scope.searchText, 'i'))>=0
        }

  });
