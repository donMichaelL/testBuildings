angular.module('mainApp', ['ngRoute', 'ngFileUpload', 'wu.masonry'])
.config(['$routeProvider', function($routeProvider){
    $routeProvider.when('/', {
        template: '<h1>Homepage</h1>'
    })
    .when('/login', {
      templateUrl: 'static/partials/login.html',
      controller: 'LoginController',
      resolve : ['loginFactory', '$location', function(loginFactory, $location){
        loginFactory.returnIsLoggedInServer().then(
         function(response){
           if (response){
             $location.path('/buildings');
           }
         }, function(response){
         }
       );
      }]
    })
    .when('/buildings', {
        templateUrl: 'static/partials/building-list.html',
        controller: 'BuildingController',
        resolve:  {
          buildingsList: ['buildingFactory', function(buildingFactory){
            return buildingFactory.returnBuildings();
          }]
        }
    })
    .when('/buildings/:building_id',{
      templateUrl: 'static/partials/building-detail.html',
      controller: 'BuildingDetailController',
      resolve: {
        buildingDetails: ['buildingFactory', '$route', function(buildingFactory, $route){
          return buildingFactory.returnSingleBuilding($route.current.params.building_id);
        }],
        floorsList: ['floorFactory', '$route', function(floorFactory, $route){
          return floorFactory.returnFloors($route.current.params.building_id);
        }]
      }
    })
    .when('/buildings/:building_id/floors/:floor_id', {
      templateUrl: 'static/partials/floor-detail.html',
      controller: 'FloorDetailController',
      resolve: {
        floorDetails: ['floorFactory', '$route', function(floorFactory, $route){
          return floorFactory.returnSingleFloor($route.current.params.building_id, $route.current.params.floor_id);
        }]
      }
    })
    .otherwise({redirectTo: '/'});
}])
.run(['$http', 'getCookiesFactory', function($http, getCookiesFactory){
  getCookiesFactory.setHttpHeaders();
}])
;
