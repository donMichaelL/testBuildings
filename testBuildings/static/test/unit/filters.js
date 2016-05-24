describe('Filters', function(){

  beforeEach(module('mainApp'));

  describe('countryFullName', function(){
    var countryFullName;
    beforeEach(inject(function($filter){
      countryFullName = $filter('countryFullName');
    }));

    it('should return Country Full Nam or None', function(){
      expect(countryFullName('gr')).toBe('Greece');
      expect(countryFullName('it')).toBe('Italy');
      expect(countryFullName('rm')).toBe('Romania');
      expect(countryFullName('bg')).toBe('Bulgaria');
      expect(countryFullName('jfkd')).toBe('None');
    });
  });

  describe('returnPhoto', function(){
    var returnPhoto;
    beforeEach(inject(function($filter){
      returnPhoto = $filter('returnPhoto');
    }));

    it('should return actual photo if exists', function(){
      expect(returnPhoto('/static/photo1.jpg')).toBe('/static/photo1.jpg');
    });

    it('should return default photo if null', function(){
      expect(returnPhoto()).toBe('https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/H%C3%B4telDeVille.jpg/310px-H%C3%B4telDeVille.jpg');
    });
  });

});
