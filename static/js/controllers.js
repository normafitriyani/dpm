angular.module('app.controllers', [])
  
.controller('diseasesPredictionAppCtrl', ['$scope', '$stateParams', 'Prediction', '$state',// The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams, Prediction, $state) {
	$scope.predictDisease = function(){
	  var data = this.data;

	  function getAge(dateString) 
		{
		    var today = new Date();
		    var birthDate = dateString;
		    var age = today.getFullYear() - birthDate.getFullYear();
		    var m = today.getMonth() - birthDate.getMonth();
		    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) 
		    {
		        age--;
		    }
		    return age;
		}

	  var risk_factors = {
	  	pid: data.pid,
	  	dob: data.dob,
	  	age: getAge(data.dob),
	  	height: data.height,
	  	wc: data.wc,
	  	hc: data.hc,
	  	weight: data.weight,
	  	whr: (data.wc/data.hc).toFixed(2),
	  	bmi: (data.weight/((data.height/100)*(data.height/100))).toFixed(2)
	  }

	  console.log(risk_factors);

	  Prediction.predict(risk_factors)
	  	// if successful creation, call our function
		.success(function(res) {
			if(res.success){
				$state.go('diseasesPredictionApp2', {risks: risk_factors, result:res});
				this.data = res;
			} else {
				console.log("Error!!!"+res)
			}
			
			console.log(res);
		});

	 
	};

}])
   
.controller('diseasesPredictionApp2Ctrl', ['$scope', '$stateParams', '$state',// The following is the constructor function for this page's controller. See https://docs.angularjs.org/guide/controller
// You can include any angular dependencies as parameters for this function
// TIP: Access Route Parameters for your page via $stateParams.parameterName
function ($scope, $stateParams, $state) {
	console.log($state.params.risks)
	console.log($state.params.result)
	
	$scope.data = $state.params.risks;
	$scope.result = $state.params.result;

}])
 