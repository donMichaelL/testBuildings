angular.module('mainApp')
.filter('countryFullName', function(){
  return function(input){
    switch (input) {
      case 'gr':
        return 'Greece';
      case 'rm':
        return 'Romania';
      case 'bg':
        return 'Bulgaria';
      case 'it':
        return 'Italy';
      default:
        return 'None';
    };
  };
})
.filter('returnPhoto', function(){
  return function(input){
    if(input!=null){
      return input;
    }
    return 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/H%C3%B4telDeVille.jpg/310px-H%C3%B4telDeVille.jpg';
  };
});
