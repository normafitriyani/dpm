# dpm - mobile web apps

This repository consists of web apis and mobile apps for dpm. The structure of this repository is as follows:

```
.
├── api.py <-- python web APIs
├── models <-- machine learning models
│   ├── diabetes.model
│   ├── hypertension.model
│   └── index.html
├── readme.md <-- instructions
├── requirements.txt <-- python environment
└── static
    ├── img
    ├── index.html
    ├── js
    │   ├── app.js <-- mobile apps initialization (Ionic v1 Starter App)
    │   ├── controllers.js <-- controller of the apps
    │   ├── directives.js 
    │   ├── routes.js <-- Set up the various states which the app can be in. Each state's controller can be found in controllers.js
    │   └── services.js <-- services for communication with APIs
    ├── lib <-- the library used in this repository including the CSS, Fonts, and Javascripts.
    │   ├── ionic
    │   │   ├── css
    │   │   ├── fonts
    │   │   ├── js
    │   │   ├── scss
    │   │   └── version.json
    │   └── ionicuirouter
    ├── manifest.json
    └── templates <-- Templates for data input and prediction result
        ├── diseasesPredictionApp2.html
        └── diseasesPredictionApp.html

Total: 17 directories, 87 files
```

# To run and install this repo
We assumed that you have already installed Python version 3.6 in your Operating Systems (OS) if not please install python first, if not please install python first: https://www.python.org/downloads/.
1. Download and extract this repository into your local machine/cloud server.
2. Go to the extracted folder and make sure you have already installed `pipenv`, for example: 
```
$ cd dpm
$ pip install pipenv

```
3. Install all the dependency from requirements.txt
```
$ pipenv install -r requirements.txt
```
4. Run the `api.py` file: 
```
$ python api.py
```
if success, it will show this messages:
```
.....
Successfully loaded model: hypertension.model
Successfully loaded model: diabetes.model
 * Debugger is active!
 * Debugger PIN: 136-789-363
 * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
```
5. Open the web app via web/mobile browser at port `:8080`

Voila!
