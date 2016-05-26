angular.module('mainApp')
.directive('loadingSpin', ['$rootScope', '$location', function($rootScope, $location){
  return {
    restrict: 'E',
    template: "<img ng-src='/static/img/spin.gif' ng-if='isRouteLoading'  class='loading'/>",
    link: function(scope, elem, attrs){
      scope.isRouteLoading = false;
      $rootScope.$on('$routeChangeStart', function(){
        scope.isRouteLoading = true;
      });
      $rootScope.$on('$routeChangeSuccess', function(){
        scope.isRouteLoading = false;
      });
      $rootScope.$on('$routeChangeError', function(angularEvent, current, previous, rejection){
        scope.isRouteLoading = false;
        console.log(rejection.status);
        $location.path('login');
      });
    }
  };
}]);
