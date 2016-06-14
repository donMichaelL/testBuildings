angular.module('mainApp')
.controller('LoginController', ['$scope', 'loginFactory', '$location', function($scope, loginFactory, $location){
  $scope.user = {};

  $scope.login = function(){
    loginFactory.login($scope.user).then(function(response){
        $location.path('/buildings');
    },function(response){
      console.log(response.data);
    })
  }
}])
.controller('BuildingController', ['$scope', 'buildingFactory', 'countryAcronyms','$timeout', 'buildingsList',
  function($scope, buildingFactory, countryAcronyms, $timeout, buildingsList){

    $scope.building = {};
    $scope.buildings = {};
    $scope.countries = countryAcronyms.getAll();
    $scope.orderText = 'updated';
    $scope.reversed = true;

    $scope.buildings = buildingsList.data;

    $scope.submitBuilding = function(photo){
      object = angular.copy($scope.building);
      object['photo'] = $scope.building.photo;
      buildingFactory.addNewBuildingFile(object).then(function(response) {
        $timeout(function () {
          $scope.buildings.push(response.data);
          $scope.building = {};
          $scope.buildingForm.$setPristine();
          $('#insertBuilding').modal('hide');
        });
      }, function(response) {
          alert(response.statusText + ' Supported image files jpg, png');
          console.log(response.data);
          $scope.building.photo = undefined;
      }, function (evt) {
        if($scope.building.photo){
          $scope.building.photo.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
        }
      });
    };

    $scope.deleteModal = function(building){
      $scope.deletable = building;
      $('#deleteBuilding').modal('show');
    };

    $scope.deleteBuilding = function(id){
      buildingFactory.deleteBuilding(id).then(function(response){
        for(var i=0; i<$scope.buildings.length; i++){
          if($scope.buildings[i].id==id){
            $scope.buildings.splice(i,1);
          }
        }
      }, function(response){
          alert(response.statusText);
      });
    };

}])
.controller('BuildingDetailController', ['$scope', '$routeParams', 'buildingFactory', 'countryAcronyms', '$location', 'floorFactory', '$timeout', 'buildingDetails', 'floorsList',
  function($scope, $routeParams, buildingFactory, countryAcronyms, $location, floorFactory, $timeout, buildingDetails, floorsList){
    $scope.countries = countryAcronyms.getAll();
    $scope.building_id = $routeParams.building_id;
    $scope.editObject = {};
    $scope.floor = {};

    $scope.building = buildingDetails.data;
    $scope.editObject = angular.copy($scope.building);

    $scope.floors = floorsList.data;

    $scope.updateBuilding = function(photo){
      $scope.editObject['photo'] = $scope.editObject.photo;
      buildingFactory.updateBuilding($scope.editObject).then(function(response){
        $scope.building = response.data;
        $scope.editing = false;
      }, function(response){
        alert(response.statusText + ' Supported image files jpg, png');
        $scope.editObject.photo = undefined;
      });
    };

    $scope.insertFloor = function(photo){
      object = angular.copy($scope.floor);
      object['blueprint'] = $scope.floor.blueprint;
      object['building'] = $scope.building_id;
      floorFactory.addNewFloorFile(object).then(function(response){
        $timeout(function () {
          $scope.floors.push(response.data);
          $scope.floor = {};
          $scope.floorForm.$setPristine();
          $('#insertFloor').modal('hide');
        });
      }, function(response) {
          alert(response.statusText + ' Supported image files jpg, png');
          console.log(response.data);
          $scope.floor.blueprint = undefined;
        }, function(evt){
          if($scope.floor.blueprint){
            $scope.floor.blueprint.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
          }
        }
      )
    };

    $scope.deleteFloor = function(floor_id){
      floorFactory.deleteFloor($scope.building_id, floor_id).then(function(response){
        for(var i=0; i<$scope.floors.length; i++){
          if($scope.floors[i].id==floor_id){
            $scope.floors.splice(i,1);
          }
        }
        }, function(response){
          alert(response.statusText);
        })
    };

    $scope.deleteFloorModal = function(floor){
      $scope.deletableFloor = floor;
      $('#deleteFloor').modal('show');
    };

}])
.controller('FloorDetailController', ['$scope', 'floorDetails', 'floorFactory', function($scope, floorDetails, floorFactory){
  $scope.floor = floorDetails.data;
  $scope.editObject = angular.copy($scope.floor);

  $scope.updateFloor = function(photo){
    $scope.editObject['blueprint'] = $scope.editObject.blueprint;
    floorFactory.updateFloor($scope.editObject).then(function(response){
      $scope.floor = response.data;
      $scope.editing = false;
    }, function(response){
      alert(response.statusText + ' Supported image files jpg, png');
      $scope.editObject.photo = undefined;
    });

  };

}])
;
