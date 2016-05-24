describe('Controller:BuildingController', function(){
  beforeEach(module('mainApp'));

  var BuildingController, scope, buildingFactory, $httpBackend;
  beforeEach(inject(function($rootScope, $controller, buildingFactory, $timeout, _$httpBackend_){
    $httpBackend = _$httpBackend_;
    $httpBackend.expectGET('buildings/').respond([
      {
        'id': 0,
        'name': 'Building 1',
        'country': 'gr',
        'address': 'Dimi',
        'tk': 1222,
        'max_evacuation_time': 12
      }, {
        'id': 1,
        'name': 'Building 2',
        'country': 'gr',
        'address': 'Dimi',
        'tk': 1222,
        'max_evacuation_time': 12
      }]);

    $scope = $rootScope.$new();
    BuildingController = $controller('BuildingController', {
      $scope: $scope,
      buildingFactory: buildingFactory,
      $timeout: $timeout
    });

     $httpBackend.flush();
  }));

  it('should create 2 buildings fetched from xhr', function(){
    expect($scope.loading).toBeFalsy();
    expect($scope.buildings).toBeDefined();
    expect($scope.buildings.length).toBe(2);
  });

  it('should have the correct data buildings in the buildings', function(){
    expect($scope.buildings[0].name).toBe('Building 1');
    expect($scope.buildings[1].name).toBe('Building 2');
  });

  it('should start with order by updated and reversed true', function(){
    expect($scope.orderText).toEqual('updated');
    expect($scope.reversed).toEqual(true);
  });
  //
  // it('should add new element when post', function(){
  //   $scope.building.name = "Test";
  //   $scope.building.country = "gr";
  //   $scope.submitBuilding();
  //   console.log($scope.buildings.length);
  //   expect($scope.buildings.length).toBe(3);
  // });

});
