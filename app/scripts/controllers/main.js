'use strict';

angular.module('belizeorchidsApp')
    .controller('MainCtrl', function ($http, $scope) {
        $scope.orchids = [];
        $scope.detail_images = {};
        $scope.orchid_counts = {}
        var server = 'http://localhost:27080',
            db = server + "/orchids";

        var config = {
            method: 'GET',
            url: db + "/orchids/_find",
            params: {
                limit: "500",
                batch_size: "500",
                sort: {name: 1}
                //fields: ["name, image_ids"]
            }
        }

        $scope.show_index = -1;
        $scope.show_detail = function(index) {
            console.log("index: ", index);
            $scope.show_index = index;
            var name = $scope.orchids[index].name;
            $scope.detail_images[name] = [];

            $scope.orchids[index].thumb_ids.forEach(function(thumb_id, thumb_index) {
                $scope.detail_images[name][thumb_index] = db + "/thumbs/" + thumb_id;
            });
            console.log('images: ', $scope.detail_images[name]);
        }

        $scope.get_counts = function(name) {
            console.log("name: ", name);
            console.log('{"name": ' + name + '}')
            var config = {
                method: 'GET',
                //url: db + "/gridfs/thumbs/_find",
                url: 'http://localhost:27080/orchids/fs/thumbs/_find',
                params: {
                    //criteria: JSON.stringify({"name": name})
                    criteria: {name: name}
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
                    //$scope.get_counts(orchid.name);
                });
                console.log("data: ", data);
            })
            .error(function(data, status, headers, config) {
                // do something
            })
  });
