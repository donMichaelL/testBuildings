angular.module('mainApp')
.factory('getCookiesFactory',[ function(){
  return {
    getCookie: function(name){
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
                  }
              }
      }
      return cookieValue;
    }
  };
}])
.factory('countryAcronyms', [ function(){
  return {
    'getAll': function(){
      return [
          {'id': 'gr', 'name': 'Greece'},
          {'id': 'rm', 'name': 'Roumania'},
          {'id': 'bg', 'name': 'Bulgaria'},
          {'id': 'it', 'name': 'Italy'}
      ];
    }
  };
}])
.factory('loginFactory', ['$http', function($http){
  return {
    'login': function(user){
      return $http.post('login', user);
    }
  };
}])
.factory('buildingFactory', ['$http', 'Upload', 'getCookiesFactory', function($http, Upload, getCookiesFactory){
  return {
  'returnBuildings': function(){
      return $http.get('buildings/');
  },
  'addNewBuildingFile': function(new_building){
      return Upload.upload({
        url: 'buildings/',
        data: new_building,
        headers: {'X-CSRFToken': getCookiesFactory.getCookie('csrftoken')}
      });
  },
  'returnSingleBuilding': function(id){
    return $http.get('buildings/'+id);
  },
  'updateBuilding': function(building){
    return Upload.upload({
      url: 'buildings/'+ building.id + '/',
      method: 'PUT',
      data: building,
      headers: {'X-CSRFToken': getCookiesFactory.getCookie('csrftoken')}
    });
  },
  'deleteBuilding': function(id){
    return $http.delete('buildings/'+ id + '/');
  }
  };
}])
.factory('floorFactory', ['$http', 'Upload', 'getCookiesFactory', function($http, Upload, getCookiesFactory){
  return {
    'returnFloors': function(id){
      return $http.get('buildings/'+ id + '/floors/');
    },
    'addNewFloorFile': function(new_floor){
      return Upload.upload({
        url: 'buildings/'+ new_floor.building + '/floors/',
        data: new_floor,
        headers: {'X-CSRFToken': getCookiesFactory.getCookie('csrftoken')}
      });
    },
    'returnSingleFloor': function(building_id, floor_id){
      return $http.get('buildings/'+ building_id + '/floors/'+ floor_id + '/');
    },
    'updateFloor': function(floor){
      return Upload.upload({
        url: 'buildings/'+ floor.building + '/floors/' + floor.id + '/',
        method: 'PUT',
        data: floor,
        headers: {'X-CSRFToken': getCookiesFactory.getCookie('csrftoken')}
      });
    },
    'deleteFloor': function(building_id, floor_id){
      return $http.delete('buildings/'+ building_id + '/floors/'+ floor_id + '/');
    },
  };
}])

;
