angular.module('app.services', [])

.factory('BlankFactory', [function(){

}])

// super simple service
// each function returns a promise object 
.factory('Prediction', function($http) {
    return {
        ping : function() {
            return $http.get('https://api.diseaseprediction.me/v1/ping');
        },
        predict : function(risk_data) {
            return $http.post('https://api.diseaseprediction.me/v1/predict', risk_data);
        }
    }
})