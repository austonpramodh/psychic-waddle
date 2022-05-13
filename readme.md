# Python Flask ecommerce project

### Starting the project

Python 3.6 would be required as flask-sqlalchemy only supports until Python3.7

1. Create a venv and activate it
  ```sh
  virtualenv venv
  source ./venv/bin/activate  
  ```

2. Install all the requirements
  ```sh
  pip install -r requirements.txt
  ```

3. Add env variables for flask
  ```sh
  MAIN_FILE=app.py
  export FLASK_APP=$MAIN_FILE
   set FLASK_APP=$MAIN_FILE
  ```

3. start the flask project
  ```sh
  flask run
  ```