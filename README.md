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


IMPLEMENTED: 

1. Jinja templates for user profile page and accounts pages (login, logout, edit, delete account)
2. CRUD & session created. Database schema setup, initial data inserted. 
3. Flask app setup
4. Login, logout, edit, delete functionality implemented
5. Like and delete items implemented. Comments (and their deletion) implemented
6. Change index to be a client-side process (within browser, not server hosted.) 
7. Make AJAX calls to REST API to get necessary data to render index page. 
8. All item functionalities modified. 
9. Add cart functionality 

TODO: 
1. Create checkout page 
2. Create cookie session to save logname and cart contents. (Cart contents currently only exist in React state)
3. Add payment functionality 
4. Admin application 
