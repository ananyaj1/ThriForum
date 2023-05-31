# ThriForum

PROJECT SETUP (MAC OS DIRECTIONS): 

1. Git clone this repository on your local machine. 
2. Install Python3 and create virtual environment: ``` python3 -m venv env ``` You can activate this environment like this: ``` source env/bin/activate ```
3. Install sqlite & curl : ```brew install sqlite3 curl httpie coreutils```
4.  Make sure scripts are active. ```chmod +x {script.path} ```
5.  Make sure pip is installed: ``` which pip ``` and install the necessary requirements: ```pip install -r requirements.txt``` and ```pip install -e . ```
6.  Install Node. ``` brew install node ``` check versions: ``` node --version ``` and ``` npm -version ```
7.  Use npm to install dependencies(webpack, prettier, eslint). ``` npm ci . ```
8.  Create bundle.js with ``` npx webpack ``` 
9.  Run app with command: ``` flask run --host 0.0.0.0 --port 8000 ``` or using script: ``` ./bin/onlinestorerun ```
