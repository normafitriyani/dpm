# USAGE
# Start the server:
# 	python app.py

# import the necessary packages
import numpy as np
import pandas as pd
import io, os
from flask import Flask, request, jsonify
from joblib import load
import random


# create the Flask app
app = Flask(__name__, static_url_path='')
app.secret_key = os.urandom(24)

model_hypertension = None
model_diabetes = None

def load_model_hypertension():
	global model_hypertension
	model_hypertension = load("./models/hypertension.model")
	print("Successfully loaded model: hypertension.model")

def load_model_diabetes():
	global model_diabetes
	# load model from file
	model_diabetes = load("./models/diabetes.model")
	print("Successfully loaded model: diabetes.model")

@app.route('/', methods=['GET'])
def webapps():
	return app.send_static_file('index.html')

@app.route('/v1/ping')
def ping():
    return 'Pong!'

@app.route('/v1/predict', methods=['POST'])
def predict():
	data = request.get_json()
	print(data)
	obes_status, obes_YES = obesity_check(data['bmi'], data['wc'])

	obs = 1 if obes_YES=="YES" else 0
	data["obese"] = obs
	
	htn = predict_hypertension(data)
	htn_status = "YES" if htn == 1 else "NO"

	dbs = predict_diabetes(data["age"], htn)
	diabetes_status = "YES" if dbs == 1 else "NO"

	diseases = [obs, htn, dbs]
	suggestions = get_suggestions(diseases, data)

	res = {
		"success": True,
		"message": "OK",
		"obes_status": obes_status.lower(),
		"obes_YES": obes_YES.lower(),
		"htn_status": htn_status.lower(),
		"diabetes_status": diabetes_status.lower(),
		"suggestions": suggestions
	}

	return jsonify(res)

# get_suggestions
def get_suggestions(diseases, data):
	obs, htn, dbs = diseases
	obes_status, obes_YES = obesity_check(data['bmi'], data['wc'])
	suggestions = "<ul>"
		
	if dbs == 1 and htn == 1:
		suggestions += """
		<li>You have high risk of hypertension and type 2 diabetes! Please visit the nearest health care facility/hospital for further comprehensive medical evaluation. In the meantime, please proceed with lifestyle intervention which consists of """
		if obs == 1 or obes_status == "overweight":
			reduced_weight = round(int(data['weight'])*(7/100),2)
			suggestions += """7% ("""+str(reduced_weight)+"""kg) loss of initial body weight and """
		
		suggestions += """ a Dietary Approaches to Stop Hypertension <a href='https://www.nhlbi.nih.gov/health-topics/dash-eating-plan'>(DASH)</a>-style dietary pattern including reducing sodium and increasing potassium
		intake, moderation of alcohol intake <sup>[<a href='https://doi.org/10.2337/cd18-0105'>source</a>]</sup>.

		Please also increase moderate-intensity physical activity (such as brisk walking) to at least 150 min/week <sup>[<a href='https://doi.org/10.2337/cd18-0105'>source</a>]</sup> and follow the general dietary recommendations <sup>[<a href='https://applications.emro.who.int/dsaf/dsa664.pdf'>source</a>]</sup> as follows: 
		<ul>
			<li>Carbohydrates: 45%</li>
			<li>Total fat: 35%</li>
			<li>Mono-unsaturated fatty acids: 20%</li>
			<li>Poly-unsaturated fatty acids: <8%</li>
			<li>Saturated and trans-fatty acids: <7%</li>
			<li>Protein: 15%–20%</li>
			<li>Cholesterol: <200 mg/day</li>
		</ul></li>
		<li>You are encouraged to decrease both sweetened and nonnutritive-sweetened beverages and use other alternatives, with an emphasis on water intake.</li>
		<li>You are also advised not to use cigarettes and other tobacco products or e-cigarettes.</li>
		"""
	elif htn == 1:
		suggestions += """
		<li>You have a high risk of hypertension! Please visit the nearest health care facility/hospital for further comprehensive medical evaluation. In the meantime, please proceed with lifestyle intervention which consists of
		"""
		if obs == 1 or obes_status == "overweight":
			suggestions += """weight loss, """
		
		suggestions += """ a <a href='https://www.nhlbi.nih.gov/health-topics/dash-eating-plan'>Dietary Approaches to Stop Hypertension (DASH)</a>-style dietary pattern including reducing sodium and increasing potassium
		intake, moderation of alcohol intake, and increased physical activity <sup>[<a href='https://doi.org/10.2337/cd18-0105'>source</a>]</sup>.</li>"""

	elif dbs == 1:
		suggestions += """
		<li>You have a high risk of type 2 diabetes! Please visit the nearest health care facility/hospital for further comprehensive medical evaluation. In the meantime, please """
		if obs == 1 or obes_status == "overweight":
			reduced_weight = round(int(data['weight'])*(7/100),2)
			suggestions += """achieve and maintain 7% ("""+str(reduced_weight)+"""kg) loss of initial body weight and """

		suggestions += """increase moderate-intensity physical activity (such as brisk walking) to at least 150 min/week <sup>[<a href='https://doi.org/10.2337/cd18-0105'>source</a>]</sup> and follow the general dietary recommendations <sup>[<a href='https://applications.emro.who.int/dsaf/dsa664.pdf'>source</a>]</sup> as follows: 
		<ul>
			<li>Carbohydrates: 45%</li>
			<li>Total fat: 35%</li>
			<li>Mono-unsaturated fatty acids: 20%</li>
			<li>Poly-unsaturated fatty acids: <8%</li>
			<li>Saturated and trans-fatty acids: <7%</li>
			<li>Protein: 15%–20%</li>
			<li>Cholesterol: <200 mg/day</li>
		</ul></li>
		<li>You are encouraged to decrease both sweetened and nonnutritive-sweetened beverages and use other alternatives, with an emphasis on water intake.</li>
		<li>You are also advised not to use cigarettes and other tobacco products or e-cigarettes.</li>
		"""
	elif obs == 1 or obes_status == "overweight":
		reduced_weight = round(int(data['weight'])*(10/100),2)
		suggestions += """
		<li>Since your BMI category is """+obes_status+""", please reduce your weight for at least 10% ("""+str(reduced_weight)+"""kg) for over the next 6 months <sup>[<a href='https://www.nhlbi.nih.gov/files/docs/guidelines/prctgd_c.pdf'>source</a>]</sup>. 
		<ul>
			<li>The rate of weight loss should be 500 to 900 gram each week. </li>
			<li>Caloric intake should be reduced by 500 to 1,000 calories per day (kcal/day) from the current level (but should not be less than 800 kcal/day). </li>
			<li>Please stay active by maintaining at least 30 minutes or more of moderate-intensity physical activity on most, and preferably all, days of the week.</li>
			</ul> """
	else:
		suggestions += "<li>Please maintain your current weight ("+data['weight']+"kg) since your BMI category is not overweight nor obesity at this moment.</li> "
		suggestions += """
		<li>
			In addition, please always keep continue eating healthy diet food and do regular exercise. A <a href='https://www.nhs.uk/live-well/eat-well/what-is-a-mediterranean-diet/'>Mediterranean</a>, <a href='https://www.nhlbi.nih.gov/health-topics/dash-eating-plan'>Dietary Approaches to Stop Hypertension (DASH)</a>, and plant-based eating plans are examples of healthful eating patterns that have shown positive results
in research <sup>[<a href='https://doi.org/10.2337/cd18-0105'>source</a>]</sup>.
			</li>
		"""

	suggestions += """</ul>"""

	return suggestions

# predict hypertension
def predict_hypertension(data):
	# ['age', 'obese', 'bmi', 'wc', 'hc', 'whr', 'class']
	column_names = ['age', 'obese', 'bmi', 'wc', 'hc', 'whr']
	row_data = [[data['age'],data['obese'],data['bmi'],data['wc'],data['hc'],data['whr']]]
	dt_input = pd.DataFrame(row_data,columns = column_names)
	
	#print(dt_input)
	prediction = model_hypertension.predict(dt_input)
	if prediction[0] == 1:
		status = 'hypertension'
	else:
		status = 'normal'
	
	print("predict_hypertension", status, prediction[0])
	return prediction[0]

# predict diabetes
def predict_diabetes(age, htn):
	# ['age', 'htn']
	column_names = ['age', 'htn']
	row_data = [[age,htn]]
	dt_input = pd.DataFrame(row_data,columns = column_names)
	
	#print(dt_input)
	prediction = model_diabetes.predict(dt_input)
	if prediction[0] == 1:
		status = 'diabetes'
	else:
		status = 'normal'

	print("predict_diabetes",status, prediction[0])
	return prediction[0]

# check obesity
def obesity_check(bmi, wc):
	# source: https://www.nhlbi.nih.gov/files/docs/guidelines/prctgd_c.pdf
	# http://apps.who.int/iris/bitstream/handle/10665/44583/9789241501491_eng.pdf
	BMI = float(bmi) 
	LOW_BMI = 18.5
	NORMAL_UP = 24.9
	OVER_BOTTOM = 25.0
	OVER_UP= 29.9
	OBESITY_BOTTOM_I = 30.0
	OBESITY_UP_I = 34.9
	OBESITY_BOTTOM_II = 35.0
	OBESITY_UP_II = 39.9
	OBESITY_BOTTOM_III = 40.0

	if BMI < LOW_BMI :
		status = "underweight"
		YES_NO = "NO"
	elif BMI >= LOW_BMI and BMI <= NORMAL_UP:
		status = "normal"
		YES_NO = "NO"
	elif BMI >= OVER_BOTTOM and BMI <= OVER_UP:
		status = "overweight"
		YES_NO = "NO"
	elif BMI >= OBESITY_BOTTOM_I and BMI <= OBESITY_UP_I:
		status = "obesity (class 1)"
		YES_NO = "YES"
	elif BMI >= OBESITY_BOTTOM_II and BMI <= OBESITY_UP_II:
		status = "obesity (class 2)"
		YES_NO = "YES"
	elif BMI >= OBESITY_BOTTOM_III:
		status = "extreme obesity (class 3)"
		YES_NO = "YES"

	return status, YES_NO

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == '__main__':
	print(("* Loading the models and Flask starting server..."
		"please wait until server has fully started"))
	# load the model (hypertension)
	load_model_hypertension()
	# load the model (diabetes)
	load_model_diabetes()
	# run app in debug mode on
	app.run(debug=True, port=8080)